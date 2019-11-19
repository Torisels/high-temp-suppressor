from machine import Pin
import dht
import time

def measure():
    d = dht.DHT11(Pin(14))
    for _ in range(10):
        d.measure()
        print(d.temperature())
        print(d.humidity())
        time.sleep(1)


