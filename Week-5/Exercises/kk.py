from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_1, K_2

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)

# Pass in a list of string variable names: This will give the names of your columns 
exp.add_data_variable_names(["eye", "radius", "x_coord", "y_cord"]) 

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

def make_text(left):
    if left: 
        text = "1) cover your rigth eye\n 2) fixate the cross\n 3) press 1 to make the circle bigger and 2 to make it smaller\n 4) use the arrows to make the circle move\n 5) press space when your are finished.\n"
    else:
        text = "1) cover your left eye\n 2) fixate the cross\n 3) press 1 to make the circle bigger and 2 to make it smaller\n 4) use the arrows to make the circle move\n 5) press space when your are finished.\n"    
    
    t = stimuli.TextScreen(text=text, heading="Blindspot")
    return(t)

""" Experiment """
def run_trial(left):
    if left :
        fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=[300, 0])
    else :
        fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=[-300, 0])
    
    fixation.preload()

    text = make_text(left)
    text.present(True,True)

    key, _ = exp.keyboard.wait(keys=[32])

    radius = 75
    circle = make_circle(radius)
    fixation.present(True, False)
    circle.present(False, True)
        
    key = 0
    x, y = (0,0)
    width, height = exp.screen.size
    if left: side = "left" 
    else : side = "right" 
 
    while key != 32 :
        key, _ = exp.keyboard.wait(keys=[K_1,K_2,K_UP,K_DOWN, K_LEFT,K_RIGHT,32])
        if key == K_1 and radius>5 :
            radius -= 5
        elif key == K_2 and radius<200 :
            radius += 5
        elif key == K_UP and y<height//2 :
            y += 15
        elif key == K_DOWN and y>-height//2:
            y -= 15
        elif key == K_LEFT and y >-width//2:
            x -= 15
        elif key == K_RIGHT and y<width//2:
            x += 15

        # At the end of your run_trial function, store any data you want in exp.data 
        exp.data.add([side, radius, x, y])

        circle = make_circle(radius, pos=(x,y))
        fixation.present(True, False)
        circle.present(False, True)


control.start(subject_id=1)

# oeil gauche
left = True
run_trial(left)

# oeil droit
left = False
run_trial(False)

control.end()