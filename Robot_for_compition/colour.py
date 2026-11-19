
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Color
from settings import Hardware


class colour:

    def __init__(self):

        self.sensor_1 = ColorSensor(Hardware.LEFT_COLOUR_PORT)
        self.sensor_2 = ColorSensor(Hardware.RIGHT_COLOUR_PORT)
        self.sensor_3 = ColorSensor(Hardware.BACK_COLOUR_PORT)

    async def detect_left(self):
        return await self.detect_color(self.sensor_1)

    async def detect_right(self):
        return await self.detect_color(self.sensor_2)

    async def detect_back(self):
        return await self.detect_color(self.sensor_3)

    async def detect_all(self):
        return (
            await self.detect_left(),
            await self.detect_right(),
            await self.detect_back()
        )

    async def detect_color(self, sensor):
        detected = await sensor.color()

        if detected == Color.BLACK:
            return 1
        elif detected == Color.WHITE:
            return 0
        elif detected == Color.GREEN:
            return 2
        elif detected == Color.RED:
            return 3
        elif detected == Color.YELLOW:
            return 4
        elif detected == Color.BLUE:
            return 5

        return -1
