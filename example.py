import rotary_encoder
import step
from step import Stepper

encoder = rotary_encoder.Encoder(12, 16)
stepper = Stepper(step.FULL_STEP, 15, 13, 14, 2, 5, delay=3)


def s(x, y):
    global stepper
    stepper.step(x, y)

# while True:  # Infinite loop
#     if stepper.allowed:
#         if encoder.diff > 0:
#             print(encoder.diff)
#             stepper.step(85, 1)
#             encoder.diff -= 1
#         elif encoder.diff < 0:
#             print(encoder.diff)
#             stepper.step(85, -1)
#             encoder.diff += 1
