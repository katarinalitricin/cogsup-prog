
from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK
from expyriment.misc.constants import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_1, K_2

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)
exp.data_variable_names = ['side','final radius','final x coordinate','final y coordinate']

""" Stimuli """
def draw(circle, fixation):
    """Present two shapes on the back buffer then flips it.
    The shapes stay on-screen for time t (ms)."""
    fixation.present(clear=True, update=False)
    circle.present(clear=False, update=True)

def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

def change_circle_size(c1, by, fixation):
    c2 = stimuli.Circle(c1.radius+by, position=c1.position, anti_aliasing=10)
    draw(c2,fixation)
    return c2

def move_c(c1,key,fixation):
    if key == K_LEFT:
        c1.move([-dp,0])
    elif key == K_RIGHT:
        c1.move([dp,0])
    elif key == K_DOWN:
        c1.move([0,-dp])
    elif key == K_UP:
        c1.move([0,dp])
    draw(c1,fixation)


ds = 15
dp = 20
keys = [K_DOWN, K_UP, K_LEFT, K_RIGHT,K_SPACE, K_1, K_2]

def instructions(side='R'):
    s = 'right' if side=='R' else 'left'
    ins = stimuli.TextScreen('Instructions', f' Cover your {s} eye and focus on the cross. Use the 1 key to shrink the circle and the 2 key to enlarge it. Move the circle with the arrow keys. When the circle disappears from view, press SPACE. Press SPACE to begin the experiment.')
    ins.present()

""" Experiment """
def run_trial(side='R'):
    position=[-300,0] if side == 'L' else [300,0]
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=position)
    fixation.preload()

    radius = 75
    circle = make_circle(radius)

    fixation.present(True, False)
    circle.present(False, True)

    while True:
        key, _ = exp.keyboard.wait(keys)
        if key == K_1:
            circle = change_circle_size(circle, -ds, fixation)
            continue
        elif key == K_2:
            circle = change_circle_size(circle, ds, fixation)
            continue
        elif key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
            move_c(circle,key,fixation)
        elif key == K_SPACE:
            break

    exp.data.add([side,circle.radius,circle.position[0],circle.position[1]])


control.start(subject_id=1)

instructions()
exp.keyboard.wait(keys=[K_SPACE])

run_trial()

control.end()