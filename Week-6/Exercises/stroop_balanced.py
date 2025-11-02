from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_SPACE, K_1, K_2, K_3, K_4
import random
import itertools

""" Constants """

TRIAL_TYPES = ["match", "mismatch"]
COLORS = ["RED", "GREEN", "BLUE", "ORANGE"]
KEYS = dict(zip(COLORS, [K_1, K_2, K_3, K_4]))
N_BLOCKS = 8
N_TRIALS_IN_BLOCK = 16

INSTR_START = """
In this task, you have to indicate the color of each word.
Press 1,2,3, or 4 to indicate whether the word is red, green, blue, or orange.\n
Press SPACE to continue.
"""
INSTR_MID = """You have finished a block. Your task will be the same.\nTake a break then press SPACE to move on to the next block."""
INSTR_END = """Well done!\nPress SPACE to quit the experiment."""

FEEDBACK_CORRECT = """CORRECT"""
FEEDBACK_INCORRECT = """INCORRECT"""

""" Helper functions """
def load(stims):
    for stim in stims:
        stim.preload()

def timed_draw(*stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    dt = timed_draw(*stims)
    exp.clock.wait(t - dt)

def present_instructions(text):
    instructions = stimuli.TextScreen(text=text, text_justification=0, heading="Instructions")
    instructions.present()
    exp.keyboard.wait(K_SPACE)

""" Counterbalancing """
def derangements(lst):
    ders = []
    for perm in itertools.permutations(lst):
        if all(original != perm[idx] for idx, original in enumerate(lst)):
            ders.append(perm)
    return ders

PERMS = derangements(COLORS)  

def subject_trials(subject_id):
    """Generate counterbalanced trials for a subject"""
    perm = PERMS[(subject_id - 1) % len(PERMS)]
    base = [{"word": w, "color": w} for w in COLORS] + [{"word": w, "color": c} for w, c in zip(COLORS, perm)]
    block_reps = N_TRIALS_IN_BLOCK // len(base)
    trials = []
    for b_index in range(1, N_BLOCKS + 1):
        block = base * block_reps
        random.shuffle(block)
        for t_index, trial in enumerate(block, 1):
            trials.append({
                "subject_id": subject_id,
                "block_id": b_index,
                "trial_id": t_index,
                "trial_type": "match" if trial["word"] == trial["color"] else "mismatch",
                "word": trial["word"],
                "color": trial["color"]
            })
    return trials

""" Global settings """
exp = design.Experiment(name="Stroop", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS} for w in COLORS}
load([stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([feedback_correct, feedback_incorrect])

spread = 180
positions = [*range(-300, 520, spread)]
p_dict = dict(zip(COLORS, positions))
options = {c: stimuli.TextBox(f'{c} - {chr(KEYS[c])}', size=(100, 50), position=(p_dict[c], -80),
                               background_colour=C_WHITE, text_colour=C_BLACK, text_size=15) for c in COLORS}

""" Experiment """
def run_trial(block_id, trial_id, trial_type, word, color):
    """Run a single trial"""
    stim = stims[word][color]
    present_for(fixation, t=500)
    exp.screen.clear()
    for option in options.values():
        option.present(clear=False, update=False)
    stim.present(clear=False, update=True)
    key, rt = exp.keyboard.wait(KEYS.values())
    correct = key == KEYS[color]
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    present_for(feedback, t=1000)

control.start(subject_id=1)


trials = subject_trials(exp.subject)

present_instructions(INSTR_START)

current_block = 1
for trial in trials:
    if trial["block_id"] != current_block:
        present_instructions(INSTR_MID)
        current_block = trial["block_id"]
    run_trial(trial["block_id"], trial["trial_id"], trial["trial_type"], trial["word"], trial["color"])

present_instructions(INSTR_END)

control.end()