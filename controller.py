import time
from c import Encoder1  # or from pyb_encoder import Encoder
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=13,
              pin_num_dt=12,
              min_val=0,
              max_val=100,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_UNBOUNDED)

lastval = r.value()
while True:
    val = r.value()
    print(val)
    if lastval != val:
        lastval = val
        print('result =', val)

    time.sleep(0.1)
