from expyriment import design, control, stimuli
from expyriment.misc import geometry

control.set_develop_mode()

displacement_X = 400
step_size = 10


exp = design.Experiment(name = "Square")

control.initialize(exp)

triangle = stimuli.Shape(position=(-100, 0), colour=(128,0,128), vertex_list=geometry.vertices_triangle(60., 50., 50.))

hexagon = stimuli.Shape(position=(100, 0), colour=(255, 255, 0), vertex_list=geometry.vertices_regular_polygon(6, 28.87))

control.start(subject_id=1)

hexagon.present(clear=True, update=False)
triangle.present(clear=False, update=True)

exp.keyboard.wait()

control.end()