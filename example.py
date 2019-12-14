
import step
from step import Stepper


stepper = Stepper(step.FULL_STEP, 2, 14 , 13, 15, delay=3)


while True:  # Infinite loop
        for x in range(10):
            stepper.step1(85, 1)
        print("stop")
        for y in range(10):
            stepper.step1(85, -1)