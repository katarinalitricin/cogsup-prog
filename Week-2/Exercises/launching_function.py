
from expyriment import design, control, stimuli

def launching_function(temporal_gap=80, spatial_gap=100, speed=4.0):
    
    control.set_develop_mode()  # windowed while testing
    exp = design.Experiment(name="Launching – combined")
    control.initialize(exp)

    
    SIZE = 50
    HALF = SIZE / 2.0
    START_RED_X = -400
    START_GREEN_X = 0

    step_px  = 10     
    frame_ms = 10    
    iti_ms   = 800    

    def draw(r, g, clear_first=True):
        r.present(clear=clear_first, update=False)
        g.present(clear=False,   update=True)

    def one_variant(delay_ms=0, gap_px=0, speed_ratio=1.0):
        
        # fresh stimuli each time
        red   = stimuli.Rectangle((SIZE, SIZE), colour=(255, 0, 0), position=(START_RED_X, 0))
        green = stimuli.Rectangle((SIZE, SIZE), colour=(0, 255, 0), position=(START_GREEN_X, 0))
        red.preload(); green.preload()

        # show both at their starting positions for 1 s
        draw(red, green)
        exp.clock.wait(1000)

        # move RED right until true contact: red_right >= green_left
        steps_red = 0
        while red.position[0] + HALF < green.position[0] - HALF:
            red.move((step_px, 0))
            steps_red += 1
            draw(red, green)
            exp.clock.wait(frame_ms)

        if gap_px:
            gx, gy = green.position
            green.position = (gx + gap_px, gy)
            draw(red, green) 


        if delay_ms:
            exp.clock.wait(delay_ms)

        steps_green = 0
        while steps_green < steps_red:
            green.move((speed_ratio * step_px, 0))
            draw(red, green)          # red stays where it stopped
            exp.clock.wait(frame_ms)
            steps_green += 1

        # hold the final frame briefly
        exp.clock.wait(1000)

    control.start(subject_id=1)

    # 1) Baseline (Michotte)
    one_variant(delay_ms=0, gap_px=0, speed_ratio=1.0)
    exp.clock.wait(iti_ms)

    # 2) Temporal gap
    one_variant(delay_ms=temporal_gap, gap_px=0, speed_ratio=1.0)
    exp.clock.wait(iti_ms)

    # 3) Spatial gap 
    one_variant(delay_ms=0, gap_px=spatial_gap, speed_ratio=1.0)
    exp.clock.wait(iti_ms)

    # 4) Triggering 
    one_variant(delay_ms=0, gap_px=0, speed_ratio=float(speed))

    control.end()


# Example call
if __name__ == "__main__":
    launching_function(temporal_gap=80, spatial_gap=100, speed=4)
