from expyriment import design, control, stimuli

exp = design.Experiment(name="Square")

control.set_develop_mode()
control.initialize(exp)

fixation = stimuli.FixCross()
square = stimuli.Rectangle(size=(100, 100), line_width=5)

control.start(subject_id=1)

fixation.present(clear=True, update=False)
exp.screen.update()
exp.clock.wait(500)

square.present(clear=True, update=False)
fixation.present(clear=False,update=False)
exp.screen.update()
exp.keyboard.wait()

control.end()