import rotary_encoder
import step
from step import Stepper

encoder = rotary_encoder.Encoder(12, 16)
stepper = Stepper(step.FULL_STEP, 15, 13, 14, 2, delay=2)


while True:  # Infinite loop
    if encoder.diff > 0:
        print(encoder.diff)
        stepper.step(85, 1)
        encoder.diff -= 1
    elif encoder.diff < 0:
        print(encoder.diff)
        stepper.step(85, -1)
        encoder.diff += 1
