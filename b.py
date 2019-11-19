from machine import Pin
import dht
import time

ITERATIONS = 10

def a():
    d1 = dht.DHT11(Pin(14))
    d2 = dht.DHT11(Pin(2))
    dis = [d1, d2]
    sums = {0:[],1:[]}

    for _ in range(ITERATIONS):
        for i, d in enumerate(dis):
            d.measure()
            print("Device no: {}".format(i+1))
            temp = d.temperature()
            sums[i].append(temp)
            print("Temperature: {}C".format(temp))
            print("Humidity: {}%".format(d.humidity()))

            time.sleep(1)

    for device, temps in sums.items():
        avg = sum(temps)/len(temps)
        print("Device no: {}. AVG Temp: {}C".format(device,avg))
        print()
