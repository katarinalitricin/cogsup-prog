from expyriment import design, control, stimuli, misc

control.set_develop_mode()
exp = design.Experiment("Kanizsa Rectangle", background_colour=misc.constants.C_GREY)
control.initialize(exp)

def kanizsa_rectangle(aspect_ratio=1.5, rect_factor=0.25, circle_factor=0.05):
    width, height = exp.screen.size
    rect_width = int(rect_factor * width)
    rect_height = int(rect_width / aspect_ratio)

    circle_r = int(circle_factor * width)

    x_half = rect_width // 2
    y_half = rect_height // 2

    c1 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_BLACK,
                        position=( x_half,  y_half))
    c2 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_BLACK,
                        position=(-x_half,  y_half))
    c3 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_WHITE,
                        position=( x_half, -y_half))
    c4 = stimuli.Circle(radius=circle_r, colour=misc.constants.C_WHITE,
                        position=(-x_half, -y_half))

    mask = stimuli.Rectangle(size=(rect_width, rect_height), colour=misc.constants.C_GREY)

    c1.present(clear=True, update=False)
    c2.present(clear=False, update=False)
    c3.present(clear=False, update=False)
    c4.present(clear=False, update=False)
    mask.present(clear=False, update=True)

control.start()
kanizsa_rectangle(aspect_ratio=1.8, rect_factor=0.3, circle_factor=0.06)
exp.keyboard.wait()
control.end()
