from expyriment import design, control, stimuli

exp = design.Experiment(name="Two Squares")
control.initialize(exp)

square1 = stimuli.Rectangle((50,50),colour=(195,0,0),position=(-100,0)) # create tstimulus
square2 = stimuli.Rectangle((50,50),colour=(0,98,255),position=(100,0))

square1.preload()
square2.preload()

control.start()

square1.present(clear=True,update=False)
square2.present(clear=False,update=True)


exp.clock.wait(5000)

control.end()