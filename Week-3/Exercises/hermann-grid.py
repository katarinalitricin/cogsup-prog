
from expyriment import design, control, stimuli, misc

control.set_develop_mode()

def hermann_grid(square_len=60, space=12, rows=8, cols=10,
                 square_colour=misc.constants.C_BLACK,
                 background_colour=misc.constants.C_WHITE):

    exp = design.Experiment("Hermann Grid", background_colour=background_colour)
    control.initialize(exp)

    # total grid size
    total_w = cols * square_len + (cols - 1) * space
    total_h = rows * square_len + (rows - 1) * space

    # top-left square center
    start_x = -total_w // 2 + square_len // 2
    start_y =  total_h // 2 - square_len // 2

    control.start()

    first = True
    for i in range(rows):
        for j in range(cols):
            x = start_x + j * (square_len + space)
            y = start_y - i * (square_len + space)
            sq = stimuli.Rectangle(size=(square_len, square_len),
                                   colour=square_colour,
                                   position=(x, y))
            sq.present(clear=first, update=False)
            first = False

    exp.screen.update()
    exp.keyboard.wait()
    control.end()

hermann_grid(square_len=80, space=20, rows=6, cols=6,
             square_colour=misc.constants.C_BLACK,
             background_colour=misc.constants.C_WHITE)
