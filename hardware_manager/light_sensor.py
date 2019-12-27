import utime
class LightSensor:
    """
    Micropython BH1750 ambient light sensor driver.
    Adapted from https://github.com/PinkInk/upylib/tree/master/bh1750 by Gustaw Daczkowski
    """

    PWR_OFF = 0x00
    PWR_ON = 0x01
    RESET = 0x07

    # modes
    CONT_LOWRES = 0x13
    CONT_HIRES_1 = 0x10
    CONT_HIRES_2 = 0x11
    ONCE_HIRES_1 = 0x20
    ONCE_HIRES_2 = 0x21
    ONCE_LOWRES = 0x23

    # default addr=0x23 if addr pin floating or pulled to ground
    # addr=0x5c if addr pin pulled high
    def __init__(self, bus, mode = CONT_HIRES_1,  addr=0x23):
        self.mode = mode
        self.bus = bus
        self.addr = addr
        self.off()
        self.reset()
        self._luminance = 0
        self.set_mode(mode)
		t1 = threading.Thread(target=self.loop)
        t1.start()

    async def measure_luminance(self):
        while True:
            await self.get_luminance(self.mode)

    @property
    def luminance(self):
        return self._luminance


    def off(self):
        """Turn sensor off."""
        self.set_mode(self.PWR_OFF)

    def on(self):
        """Turn sensor on."""
        self.set_mode(self.PWR_ON)

    def reset(self):
        """Reset sensor, turn on first if required."""
        self.on()
        self.set_mode(self.RESET)

    def set_mode(self, mode):
        """Set sensor mode."""
        self.bus.writeto(self.addr, bytes([self.mode]))

    async def get_luminance(self, mode):
        """Sample luminance (in lux), using specified sensor mode."""
        if mode & 0x10 and mode != self.mode:
            self.set_mode(mode)
        if mode & 0x20:
            self.set_mode(mode)
        await asyncio.sleep_ms(24 if mode in (0x13, 0x23) else 180)
        data = self.bus.readfrom(self.addr, 2)
        factor = 2.0 if mode in (0x11, 0x21) else 1.0
        self._luminance = (data[0]<<8 | data[1]) / (1.2 * factor)
