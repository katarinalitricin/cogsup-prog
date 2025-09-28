from expyriment import design, control, stimuli
from expyriment.misc import geometry

control.set_develop_mode()  # dev mode: easier to test in a window
experiment = design.Experiment("Edge Display")
control.initialize(experiment)

# Get screen dimensions
width, height = experiment.screen.size
sq_len = width // 20   # this is about 5% of screen width

squares = [
    stimuli.Shape(
        vertex_list=geometry.vertices_frame([sq_len, sq_len], frame_thickness=1),
        debug_contour_colour=(255, 0, 0),
        position=(-width//2 + sq_len//2,  height//2 - sq_len//2)   # top-left
    ),
    stimuli.Shape(
        vertex_list=geometry.vertices_frame([sq_len, sq_len], frame_thickness=1),
        debug_contour_colour=(255, 0, 0),
        position=(-width//2 + sq_len//2, -height//2 + sq_len//2)   # bottom-left
    ),
    stimuli.Shape(
        vertex_list=geometry.vertices_frame([sq_len, sq_len], frame_thickness=1),
        debug_contour_colour=(255, 0, 0),
        position=( width//2 - sq_len//2,  height//2 - sq_len//2)   # top-right
    ),
    stimuli.Shape(
        vertex_list=geometry.vertices_frame([sq_len, sq_len], frame_thickness=1),
        debug_contour_colour=(255, 0, 0),
        position=( width//2 - sq_len//2, -height//2 + sq_len//2)   # bottom-right
    )
]

control.start()

# Draw all squares on the same frame
for idx, sq in enumerate(squares):
    sq.present(clear=(idx == 0), update=False)

experiment.screen.update() 

experiment.keyboard.wait()
control.end()

 