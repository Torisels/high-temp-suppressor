import uasyncio as asyncio
import machine
import dht


class DHSensor:
    def __init__(self, data_pin):
        self.d = dht.DHT11(machine.Pin(data_pin))
        self.temp = 0
        self.humid = 0
        loop = asyncio.get_event_loop()
        loop.create_task(self.loop())

    async def loop(self):
        while True:
            self.d.measure()
            self.temp = self.d.temperature()
            self.humid = self.d.humidity()
            print(self.temp)
            print(self.humid)
            await asyncio.sleep_ms(1000)