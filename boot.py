# # from machine import Pin
# # import dht
# # import time
# #
# # ITERATIONS = 10
# #
# # def a():
# #     d1 = dht.DHT11(Pin(14))
# #     d2 = dht.DHT11(Pin(2))
# #     dis = [d1, d2]
# #     sums = {0:[],1:[]}
# #
# #     for _ in range(ITERATIONS):
# #         for i, d in enumerate(dis):
# #             d.measure()
# #             print("Device no: {}".format(i+1))
# #             temp = d.temperature()
# #             sums[i].append(temp)
# #             print("Temperature: {}C".format(temp))
# #             print("Humidity: {}%".format(d.humidity()))
# #
# #             time.sleep(1)
# #
# #     for device, temps in sums.items():
# #         avg = sum(temps)/len(temps)
# #         print("Device no: {}. AVG Temp: {}C".format(device,avg))
# #         print()
# import time
# import utime
# from rotary_irq_esp import RotaryIRQ
#
# r = RotaryIRQ(pin_num_clk=13,
#               pin_num_dt=12,
#               min_val=0,
#               max_val=10000,
#               reverse=False,
#               range_mode=RotaryIRQ.RANGE_UNBOUNDED)
#
# lastval = r.value()
# while True:
#     val = r.value()
#
#     if lastval != val:
#         lastval = val
#         print('result =', val)
#
#     utime.sleep_ms(50)
# import time
# # time.sleep(1)
# from machine import UART
# time.sleep(0.1)
# uart = UART(1, 9600)                         # init with given baudrate
# uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters
# string = "1"
#
# # string with encoding 'utf-8'
# arr = bytearray(string, 'ascii')
# uart.write(arr)