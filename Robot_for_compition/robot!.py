from pybricks.tools import run_task, wait

from Motors import Motors, Wheel_Odometry
from raydar import RayDar
import objective_manger
from pybricks.hubs import EV3Brick
import colour

ev3 = EV3Brick()

class Controller:
    def __init__(self,main_pointer):
        self.states=objective_manger.States()
        self.manager=objective_manger.ProcessManager(self.states,main_pointer)


    async def main(self):

        await self.manager.execute()





class Robot:
    def __init__(self):
        self.motor = Motors() #put in varibles that we need to be global
        self.wheel_odometry = Wheel_Odometry(self.motor)
        self.raydar = RayDar(self.motor)
        self.colour=colour.colour()
        self.controller = Controller(self)

    """async def test_states(self):
        from pybricks.tools import wait

        self.controller.states.set_state("searching")

        await wait(3000)

        self.controller.states.set_state("attacking")

        await wait(3000)

        self.controller.states.set_state("idle")"""




#starts up ROBOTTTTTTT
robot = Robot()

#starts the controller!!!!!
wait(5000)
run_task(robot.controller.main())