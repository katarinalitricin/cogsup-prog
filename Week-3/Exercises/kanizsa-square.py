from expyriment import design, control, stimuli, misc

control.set_develop_mode()
exp = design.Experiment("Kanizsa Square", background_colour=misc.constants.C_GREY)
control.initialize(exp)

width, height = exp.screen.size
square_len = int(0.25 * width)     
circle_r = int(0.05 * width)       

c1 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_BLACK,
                    position=( square_len//2,  square_len//2))
c2 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_WHITE,
                    position=(-square_len//2, -square_len//2))
c3 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_WHITE,
                    position=( square_len//2, -square_len//2))
c4 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_BLACK,
                    position=(-square_len//2,  square_len//2))


mask = stimuli.Rectangle(size=(square_len, square_len), colour=misc.constants.C_GREY)

control.start()

c1.present(clear=True, update=False)
c4.present(clear=False, update=False)
c2.present(clear=False, update=False)
c3.present(clear=False, update=False)

mask.present(clear=False, update=True)

exp.keyboard.wait()
control.end()
