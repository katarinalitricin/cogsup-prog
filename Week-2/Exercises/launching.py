from expyriment import design, control, stimuli

control.set_develop_mode(on=True)
exp = design.Experiment(name="launching")
control.initialize(exp)

s_length = 50
half = s_length / 2.0

s  = stimuli.Rectangle((s_length, s_length), colour=(255, 0, 0), position=(-400, 0))
s2 = stimuli.Rectangle((s_length, s_length), colour=(0, 128, 0), position=(0, 0))
s.preload(); s2.preload()

control.start()

# show both for 1 s (clean first frame)
s.present(clear=True,  update=False)
s2.present(clear=False, update=True)
exp.clock.wait(1000)

#parameters for time-based motion
speed_px_s = 300          
frame_ms   = 10         

# move red right until its right edge meets green's left edge
elapsed_red = 0
while s.position[0] + half < s2.position[0] - half:
    dx = speed_px_s * (frame_ms / 1000.0)
    s.move([dx, 0])

    s.present(clear=True,  update=False)
    s2.present(clear=False, update=True)

    exp.clock.wait(frame_ms)
    elapsed_red += frame_ms

# move green right at the SAME speed for the SAME duration
elapsed_green = 0
while elapsed_green < elapsed_red:
    dx = speed_px_s * (frame_ms / 1000.0)
    s2.move([dx, 0])

    s.present(clear=True,  update=False)   # red stays where it stopped
    s2.present(clear=False, update=True)

    exp.clock.wait(frame_ms)
    elapsed_green += frame_ms

exp.clock.wait(1000)
control.end()
