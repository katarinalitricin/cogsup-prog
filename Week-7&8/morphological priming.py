
#morphological priming with opaque and transparent words

#Is morphological priming stronger for transparent than opaque words?
#It depends on individual differences in spelling and vocabulary (by Sally Andrews , Steson Lo)



### This is our demo version (2 blocks of 7 trials)

### GLOBAL SEETINGS OF THE EXPERIMENT

from expyriment import design, control, stimuli, misc
from expyriment.misc.constants import K_x, K_y
import random, math

FPS  = 60
MSPF = 1000 / FPS

def to_frames(t_ms): return max(0, math.ceil(t_ms / MSPF))
def to_time(fr):     return fr * MSPF

def load(stims):
    for s in stims: s.preload()

def timed_draw(exp, stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for s in stims:
        s.present(clear=False, update=False)
    exp.screen.update()
    return exp.clock.time - t0

def present_for(exp, stims, num_frames):
    if num_frames <= 0: return
    dt = timed_draw(exp, stims)
    t_needed = to_time(num_frames)
    if dt < t_needed:
        exp.clock.wait(t_needed - dt)

# keys
KEY_WORD, KEY_NONWORD = K_x, K_y
KEYS = [KEY_WORD, KEY_NONWORD]
LABELS = {KEY_WORD: "word", KEY_NONWORD: "nonword"}

#STIMULI (only demo -> replace/extend later)
WORD_TRIALS = [
    ("teacher", "garden", "TEACH", "transparent"),
    ("worker",  "planet", "WORK",  "transparent"),
    ("corner",  "muffler","CORN",  "opaque"),
    ("coaster", "finally","COAST", "opaque"),
    ("pulpit",  "gifted", "PULP",  "form"),
    ("turnip",  "pilot",  "TURN",  "form"),
]
NONWORD_TRIALS = [
    ("ploner", "flajed", "PLONE", "nonword_form_related"),
    ("blenker","fradom", "BLENK", "nonword_form_unrel"),
]
#For each word target, create two trials:
#related prime (label related=1)
#unrelated control (label related=0)


### COUNTERBALANCING (within-subject counterbalancing)

def build_trials():
    trials = []  # make an empty list to collect all the trials


    # make TWO versions (related & unrelated)
    for prime_rel, prime_unrel, target, cond in WORD_TRIALS:
        trials += [
            {"is_word": True, "prime": prime_rel,  "target": target, "condition": cond, "related": 1},
            {"is_word": True, "prime": prime_unrel,"target": target, "condition": cond, "related": 0},
        ]
    # Nonwords only need one version each
    for prime, _, target, cond in NONWORD_TRIALS:
        trials.append({"is_word": False, "prime": prime, "target": target, "condition": cond, "related": 1})

    return trials

### TRIAL STRUCTURE

#mask 500 ms, prime 50 ms, target 500 ms (then we wait for a key)
MASK_TEXT = "#######"
T_MASK_MS, T_PRIME_MS, T_TARG_MS = 500, 50, 500


def make_textline(txt, size=52):
    return stimuli.TextLine(txt, text_size=size)


#A single trial: mask → prime → target → response → log
def run_trial(exp, trial):
    # Build 3 stimuli per trial:
    mask   = make_textline(MASK_TEXT) #Mask is hashes
    prime  = make_textline(trial["prime"].lower()) #Prime lowercase (as in masked priming)
    target = make_textline(trial["target"].upper()) #Target uppercase
    load([mask, prime, target]) #Preload them before timing.

    

    present_for(exp, [mask],   to_frames(T_MASK_MS))
    present_for(exp, [prime],  to_frames(T_PRIME_MS))
    present_for(exp, [target], to_frames(T_TARG_MS))

    key, rt = exp.keyboard.wait(keys=KEYS) #After the fixed 500 ms target display, we now wait for the key (self-paced).
    #Returns the key code and the RT in ms since target onset.

    expected = "word" if trial["is_word"] else "nonword"
    given    = LABELS.get(key, "other")
    correct  = int(expected == given) # Determine if the response matches the trial type.


#Log one row to Expyriment’s data buffer (the .xpd file is written at the end).
    exp.data.add([
        exp.subject, trial["condition"], trial["target"], trial["prime"],
        trial["related"], int(trial["is_word"]), key, given, rt, correct

    ])
    if key == misc.constants.K_ESCAPE:
          control.end(); return


# flow 
N_BLOCKS = 2 #Simple split so we can show a mid-break (optional).

#Create the experiment and initialize it:
def main():
    exp = design.Experiment(
        name="Morphological Priming",
        background_colour=misc.constants.C_BLACK,
        foreground_colour=misc.constants.C_WHITE
    )
    control.initialize(exp)

    # uncomment while developing 
    control.set_develop_mode()

### DATA ORGANIZATION

    #Define column headers for the .xpd file
    exp.add_data_variable_names([
        "subject_id","condition","target","prime","related",
        "is_word","key_code","key_label","rt_ms","correct"
    ])


### PRESENTATION

    # create TextScreens **after** initialize()
    INSTR_START = stimuli.TextScreen(
        heading="Morphological Priming",
        heading_size=50,  # makes the heading larger
        text=("Press X if TARGET is a WORD. Press Y if NONWORD.\n"
              "Be fast and accurate.\n\nPress any key to begin."),
        text_size=35      # makes the body text larger
    )

    #Insturction screens:
    INSTR_MID = stimuli.TextScreen(heading="Break", heading_size=45, text="Press any key to continue.", text_size=35)  
    INSTR_END = stimuli.TextScreen(heading="Done", heading_size=45, text="Thank you! Press any key to end.", text_size=35)
    INSTR_START.preload(); INSTR_MID.preload(); INSTR_END.preload()

    # Build the trial list, shuffle, then split into N_BLOCKS by round-robin (keeps counts even).
    # We’ll shuffle each block again before running

    all_trials = build_trials()
    random.shuffle(all_trials)
    blocks = [[] for _ in range(N_BLOCKS)]
    for i, t in enumerate(all_trials): blocks[i % N_BLOCKS].append(t) 

    control.start()  # or control.start(subject_id=1)  

    
    INSTR_START.present(); exp.keyboard.wait()   #Show start instructions → wait for any key

    #For each block:
        ## Shuffle that block’s trials, run them one by one.
        ## Between blocks, show a break screen.
    for b_ix, block in enumerate(blocks, 1):
        random.shuffle(block)
        for trial in block: run_trial(exp, trial)
        if b_ix != N_BLOCKS:
            INSTR_MID.present(); exp.keyboard.wait()
    INSTR_END.present(); exp.keyboard.wait()
    control.end()  #finalizes and writes the .xpd data file.

if __name__ == "__main__":
    main()
