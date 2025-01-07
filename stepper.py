import time
import digitalio    # <-- Comment out in testing

# ==============================
#         Stepper class
# ==============================

class Stepper:
    def __init__(self, pins, steps_per_rot):
        self.steps_per_rot = steps_per_rot
        self.pins = []

        for i in range(4):
#            self.pins.append([i, 0])   # <-- Comment out in production

            pin = digitalio.DigitalInOut(pins[i])    # <-- Comment out in testing
            pin.direction = digitalio.Direction.OUTPUT    # <-- Comment out in testing
            self.pins.append(pin)    # <-- Comment out in testing

        self.steps_taken = 0
        self.step_angle = round(360 / self.steps_per_rot, 2)

    def release_pins(self):
        for i in range(4):
#          self.pins[i].value = False    # <-- Comment out in testing
            self.pins[i][1] = 0   # <-- Comment out in production

    def state_from_step_pin(self, pin, step):
        #   step 1 2 3 4
        # pin 1  1 1 0 0
        # pin 2  0 1 1 0
        # pin 3  0 0 1 1
        # pin 4  1 0 0 1
        #
        Offset = [1, 0, 3, 2]
        Timing = [0, 1, 1, 0]
        TPOS = ((step - 1) % 4 + Offset[pin]) % 4
        if Timing[TPOS] == 1:
            return True
        else:
            return False

    def fire_pins(self, nextstep):
#        prt_str = f"Step: {nextstep} - ["   # <-- Comment out in production
        for i in range(4):
            self.pins[i].value = self.state_from_step_pin(i, nextstep)    # <-- Comment out in testing
#            self.pins[i][1] = self.state_from_step_pin(self.pins[i][0], nextstep)   # <-- Comment out in production
#            prt_str += f"{int(self.pins[i][1])},"   # <-- Comment out in production
#        print(prt_str + "]")   # <-- Comment out in production

    def rotate_steps_at_rpm(self, steps, rpm):
        if steps >= 1:
            for i in range(steps):
                self.fire_pins(i)
                time.sleep(60 / (rpm * self.steps_per_rot))
                self.steps_taken += steps
        if steps <= 1:
            for i in range(steps, -1):
                self.fire_pins(i)
                time.sleep(60 / (rpm * self.steps_per_rot))
                self.steps_taken += steps
        self.release_pins()

# ==============================
#   Test to create+run stepper
# ==============================

# step_test = Stepper((1,2,3,4), 4096)   # <-- Comment out in production
# step_test.rotate_steps_at_rpm(10, 1)   # <-- Comment out in production
