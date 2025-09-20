from expyriment import design, control, stimuli

# 
SIZE = (50, 50)
RED   = (195, 0, 0)
GREEN = (0, 128, 0)
SPEED_PX_S = 300          # motion speed
FRAME_MS   = 10           # frame step (≈100 Hz)
DELAY_MS   = 2000         # try other values: 0, 50, 100, 150, 200, 300...

control.set_develop_mode()       # windowed while testing
exp = design.Experiment("Launching (disrupt time)")
control.initialize(exp)

red   = stimuli.Rectangle(SIZE, colour=RED,   position=(-400, 0))
green = stimuli.Rectangle(SIZE, colour=GREEN, position=(0, 0))
red.preload(); green.preload()

control.start()

# 1) show both for 1 s
red.present(clear=True,  update=False)
green.present(clear=False, update=True)
exp.clock.wait(1000)

# 2) move RED right until edges meet
half = SIZE[0] / 2.0
elapsed_red = 0
while red.position[0] + half < green.position[0] - half:
    dx = SPEED_PX_S * (FRAME_MS / 1000.0)
    red.move((dx, 0))
    red.present(clear=True,  update=False)
    green.present(clear=False, update=True)
    exp.clock.wait(FRAME_MS)
    elapsed_red += FRAME_MS

# 3) temporal gap before GREEN starts moving
exp.clock.wait(DELAY_MS)

# 4) move GREEN right with same speed for the same duration
elapsed_green = 0
while elapsed_green < elapsed_red:
    dx = SPEED_PX_S * (FRAME_MS / 1000.0)
    green.move((dx, 0))
    red.present(clear=True,  update=False)      # red stays where it stopped
    green.present(clear=False, update=True)
    exp.clock.wait(FRAME_MS)
    elapsed_green += FRAME_MS

# 5) hold final display for 1 s
exp.clock.wait(1000)
control.end()
