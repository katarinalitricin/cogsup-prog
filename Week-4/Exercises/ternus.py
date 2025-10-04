
from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE

def load(stims):
    for s in stims:
        s.preload()

def present_for(stims, canvas, n_frames=9):
    canvas.clear_surface()
    for s in stims:
        s.plot(canvas)
    canvas.present()
    exp.clock.wait(int(n_frames * (1000/60.0)))  # frames -> ms

def make_circles(radius=50, preload=True):

    step = 2 * radius
    slots = [-3*step/2, -step/2, step/2, 3*step/2]  # four logical positions

    c1 = stimuli.Circle(radius=radius, position=(int(slots[0]), 0), colour=(0, 0, 0))
    c2 = stimuli.Circle(radius=radius, position=(int(slots[1]), 0), colour=(0, 0, 0))
    c3 = stimuli.Circle(radius=radius, position=(int(slots[2]), 0), colour=(0, 0, 0))
    c4 = stimuli.Circle(radius=radius, position=(int(slots[3]), 0), colour=(0, 0, 0))

    A = [c1, c2, c3]
    B = [c2, c3, c4]

    if preload:
        load([c1, c2, c3, c4])

    return A, B

def add_tags(frameA, frameB, tag_radius):
    colours = [(255, 215, 0), (255, 0, 0), (0, 120, 255)]


    for idx, big in enumerate(frameA):
        tag = stimuli.Circle(radius=tag_radius, colour=colours[idx], position=(0, 0))
        tag.plot(big)
        big.preload()

    for idx, big in enumerate(frameB):
        tag = stimuli.Circle(radius=tag_radius, colour=colours[idx], position=(0, 0))
        tag.plot(big)
        big.preload()

    return frameA, frameB

def run_trial(radius=50, isi_frames=3, color_tag=False):
    A, B = make_circles(radius, preload=not color_tag)
    if color_tag:
        A, B = add_tags(A, B, tag_radius=max(4, radius//5))

    while True:
        present_for(A, canvas, n_frames=9)  # ~150 ms
        if exp.keyboard.check(K_SPACE): return
        if isi_frames > 0: exp.clock.wait(int(isi_frames * (1000/60.0)))

        present_for(B, canvas, n_frames=9)
        if exp.keyboard.check(K_SPACE): return
        if isi_frames > 0: exp.clock.wait(int(isi_frames * (1000/60.0)))

exp = design.Experiment(name="Ternus Illusion")
control.set_develop_mode()
control.initialize(exp)

canvas = stimuli.Canvas(exp.screen.size, colour=(255, 255, 255))


run_trial(radius=50, isi_frames=2, color_tag=False)
run_trial(radius=50, isi_frames=18, color_tag=False)
run_trial(radius=50, isi_frames=18, color_tag=True)

control.end()

