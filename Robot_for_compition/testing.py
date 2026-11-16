from pygments.lexers.yang import YangLexer

from examples.sensors import distance_mm


class states:

    def __init__(self):

        self.Launching = False
        self.searching = False
        self.attack = False
        self.fleeing = False
        self.color_objective = False
        self.locked = False
        self.locked_process = None

    def set_state(self, state):
        if self.locked:
            print("state is already set")
            pass
        else:
            self.locked = True
            self.locked_process = state

            if state == "launching":
                self.Launching = True
            if state == "searching":
                self.searching = True
            if state == "attacking":
                self.attack = True
            if state == "fleeing":
                self.fleeing = True
            if state == "color_objective":
                self.color_objective = True

    def read_state(self):
        return self.locked_process

    def clear_state(self):
        self.locked = False
        self.locked_process = None

    def is_launching(self):
        return self.Launching

    def is_searching(self):
        return self.searching

    def is_attacking(self):
        return self.attack

    def is_fleeing(self):
        return self.fleeing

    def is_color_objective(self):
        return self.color_objective


robot_states = states()
print(robot_states.read_state())
robot_states.set_state("launching")
print(robot_states.read_state())
robot_states.set_state("searching")
print(robot_states.read_state())
