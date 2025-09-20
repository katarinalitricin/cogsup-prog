from expyriment import design, control, stimuli

control.set_develop_mode() 

# Parameters
max_distance = 400   # how far right the green square can travel
step_px = 10         # step size per frame
green_speedup = 3    # factor to make green faster than red

# Create experiment object
exp = design.Experiment(name="Triggering effect")
control.initialize(exp)

# Define stimuli
red_square = stimuli.Rectangle((50, 50), colour=(255, 0, 0), position=(-400, 0))
green_square = stimuli.Rectangle((50, 50), colour=(0, 255, 0), position=(0, 0))

def draw(red, green, clear=True):
    """Helper function to present both squares in the right order."""
    red.present(clear=clear, update=False)
    green.present(clear=False, update=True)

# Run experiment
control.start(subject_id=1)

# Show both at start
draw(red_square, green_square)

# Move the red square until it "collides" with the green square
while red_square.position[0] < green_square.position[0] - 50:
    red_square.move((step_px, 0))
    draw(red_square, green_square)

# Optional short pause before green starts moving
exp.clock.wait(200)

# Move the green square faster to the right
while green_square.position[0] < max_distance - 50:
    green_square.move((green_speedup * step_px, 0))
    draw(red_square, green_square)

# Wait for a keypress before ending
exp.keyboard.wait()
control.end()
