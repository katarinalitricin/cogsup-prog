from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_f, K_RETURN, K_SPACE
import random

# Create experiment
exp = design.Experiment(name="Stroop", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(["trial_block", "trial_number", "trial_type", "word_meaning", "text_color", "response_time", "accuracy"]) 

control.set_develop_mode(on=True)
control.initialize(exp)

def text(color, word):
    stim = stimuli.TextLine(text=word, text_colour=color)
    stim.preload()
    return stim

def instructions():
    text = ("Press ENTER if the word and its color are the same.\n"
            "Press F if they do not match."
            "When you’re ready to start, press SPACE.")
    heading = "Stroop Effect - Instructions"
    scr = stimuli.TextScreen(heading=heading, text=text)
    scr.preload()
    return scr

def run_trial():
    colors = [(255,0,0), (0,0,255), (0,255,0), (255,165,0)]
    words = ["red", "blue", "green", "orange"]

    fixation = stimuli.FixCross()
    fixation.preload()

    instruction = instructions()
    instruction.present()
    exp.keyboard.wait(keys=[K_SPACE])

    for i in range(20):
        fixation.present()
        exp.clock.wait(500)

        match = random.choice([True, False])
        r1 = random.randint(0, 3)

        if match:
            color = colors[r1]
            word = words[r1]
        else:
            r2 = random.randint(0, 3)
            while r2 == r1:
                r2 = random.randint(0, 3)
            color = colors[r1]
            word = words[r2]

        trial = text(color, word)
        trial.present()

        key, rt = exp.keyboard.wait(keys=[K_f, K_RETURN])

        accuracy = ((key == K_RETURN and match) or (key == K_f and not match))

        exp.data.add([(i>=10)+1, i+1, "match" if match else "mismatch", word, color, rt, accuracy])

# Run experiment
control.start(subject_id=1)
run_trial()
control.end()