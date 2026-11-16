from pybricks.tools import multitask, wait


class ProcessManager:

    def __init__(self, states,main_pointer):
        self.states = states
        self.active_process = None
        self.main_pointer = main_pointer

    """ FOR COLOUR SENSORS WHAT THEY RETURN WHEN WE CALL DETECT FROM COLOUR CLASS
    :returns: 1 --black,2 --white, 3--green, 4--red, 5-yellow,
    -1 if no color detected
    """

    async def launching(self):
        pass

    async def searching(self):
        reading= await self.main_pointer.colour.detect_left()
        print("working!!! FINALY YAYAYAYAYA")
        print(reading)

        if reading==3:
            await self.main_pointer.wheel_odometry.turn_degree(180,1000,200)

    async def attacking(self):
        pass

    async def fleeing(self):
        pass

    async def color_objective(self):
        pass










    async def wait_for_state_change(self, old_state):

        while self.states.read_state() == old_state:
            await wait(10)

    async def run_process(self,proces, state):
        self.active_process = state
        #states process=state


        try:
            await multitask(proces(), self.wait_for_state_change(state),race=True)
            #starts the task
        finally:
            #once task has finished it clears the lock
            self.active_process = None


    async def execute(self):

        while True:
            state=self.states.read_state()

            if state == "idle":
                await wait(10)
                continue

            proces = self.get_process(state)

            if proces is not None:
                await self.run_process(proces, state)

            await wait(10)


    def get_process(self,state):
        processes = {
            "launching": self.launching,
            "searching": self.searching,
            "attacking": self.attacking,
            "fleeing": self.fleeing,
            "color_objective": self.color_objective
        }

        return processes.get(state)
    #this is where you put the routines!!! each one can cancel each other out

















class States:

    VALID_STATES = (
        "launching",
        "searching",
        "attacking",
        "fleeing",
        "color_objective",
        "idle"
    )

    def __init__(self):
        #also defult state on start up
        self.current_state = "searching"
        self.locked = False

    def set_state(self, state):

        if state not in self.VALID_STATES:
            print("Invalid state:", state)
            return False

        if self.locked:
            print("State is locked")
            return False

        self.current_state = state
        return True

    def read_state(self):
        return self.current_state

    def clear_state(self):
        self.current_state = "idle"
        self.locked = False

    def lock_state(self):
        self.locked = True

    def unlock_state(self):
        self.locked = False

    def is_state(self, state):
        return self.current_state == state

