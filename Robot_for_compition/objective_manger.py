
from pybricks.tools import multitask, wait, StopWatch
from settings import Movement, Strain, Objectives, Radar


class ProcessManager:

    def __init__(self, states, main_pointer):

        self.states = states
        self.active_process = None
        self.main_pointer = main_pointer

        self.motors = self.main_pointer.motor

        self.right_motor = self.motors.motor1
        self.left_motor = self.motors.motor2

        # Movement configuration
        self.diffrence_indicator = 100
        self.moving_speed = Movement.MOVING_SPEED
        self.attack_speed = Movement.ATTACK_SPEED
        self.avoid_speed = Movement.AVOID_SPEED
        self.flee_speed = Movement.FLEE_SPEED

        # Attack configuration
        self.attack_turn_threshold = 8
        self.attack_stop_distance = 120
        self.turn_speed = Movement.TURN_SPEED
        self.turn_acceleration = Movement.TURN_ACCELERATION

        # Radar tracking
        self.last_search_scan = -1
        self.last_pursuit_scan = -1
        self.radar_paused = False

        # Physical target contact
        self.contact_speed_threshold = Strain.CONTACT_SPEED_RATIO_THRESHOLD
        self.contact_load_threshold = Strain.CONTACT_LOAD_THRESHOLD
        self.contact_required_samples = Strain.CONTACT_REQUIRED_SAMPLES
        self.contact_samples = 0
        self.target_contact = False
        self.target_object_id = None
        self.ignored_object_id = None
        self.ignore_target_timer = StopWatch()
        self.ignore_target_duration = Strain.IGNORE_TARGET_DURATION_MS

        # Continuous motor strain detection
        self.flee_speed_threshold = Strain.SPEED_RATIO_THRESHOLD
        self.flee_load_threshold = Strain.LOAD_THRESHOLD

        self.strain_duration = Strain.OTHER_STATE_DURATION_MS
        self.searching_strain_duration = Strain.SEARCH_DURATION_MS
        self.major_strain_load = Strain.MAJOR_LOAD_THRESHOLD
        self.major_strain_speed = Strain.MAJOR_SPEED_RATIO_THRESHOLD
        self.strain_timer = StopWatch()
        self.strain_active = False

        # Avoidance
        self.avoid_correction = Movement.AVOID_CORRECTION_MAX
        self.avoid_distance = Movement.AVOID_DISTANCE_MM

        self.target_distance = None
        self.target_angle = None

        # Colour objectives
        self.last_objective_color = None
        self.color_cooldown = StopWatch()
        self.color_cooldown_duration = Objectives.COLOUR_COOLDOWN_MS
        self.sequence_scored = False
        self.pending_objective_color = None

    # ========================================
    # MOTOR HELPERS
    # ========================================

    def stop_motors(self):
        # State changes must not stop the drive wheels. The next movement
        # command takes over immediately, while the current command remains
        # active during sensor and state transitions.
        return

    def visible_objects(self, objects):
        if (
            self.ignored_object_id is not None
            and self.ignore_target_timer.time()
            < self.ignore_target_duration
        ):
            return {
                object_id: obj
                for object_id, obj in objects.items()
                if object_id != self.ignored_object_id
            }

        self.ignored_object_id = None
        return objects

    def radar_danger(self, distance=None):
        radar = self.main_pointer.raydar

        if distance is None:
            distance = self.avoid_distance

        for obj in self.visible_objects(radar.objects).values():
            if obj["distance"] <= distance:
                return True

        return False

    # ========================================
    # SEARCHING
    # ========================================

    async def searching(self):

        self.main_pointer.wheel_odometry.reset_relative_rotation()

        print("SEARCHING STATE STARTED")

        self.motors.speed_LR(
            self.moving_speed,
            self.moving_speed
        )

        while self.states.is_state("searching"):

            result = await self.check_search_objects()

            if result == "attacking":
                return

            if result == "avoiding":
                return

            if not self.states.is_state("searching"):
                return

            await self.determine_how_to_rotate()
            self.motors.speed_LR(
                self.moving_speed,
                self.moving_speed
            )

            await wait(Movement.LOOP_INTERVAL_MS)

    # ========================================
    # SEARCH OBJECT DECISION
    # ========================================

    async def check_search_objects(self):

        radar = self.main_pointer.raydar

        if radar.scan_count == self.last_search_scan:
            return None

        self.last_search_scan = radar.scan_count

        objects = self.visible_objects(radar.objects)

        if not objects:
            return None

        object_count = len(objects)

        print("Objects detected:", object_count)

        # One object: attack
        if object_count == 1:

            print("SINGLE TARGET IDENTIFIED")

            self.stop_motors()
            self.radar_paused = True

            self.states.set_state("attacking")

            return "attacking"

        # Multiple objects: avoid
        elif object_count > 1:

            print("MULTIPLE OBJECTS - AVOIDING")

            self.states.set_state("avoiding")

            return "avoiding"

        return None

    # ========================================
    # ATTACKING
    # ========================================

    async def attacking(self):

        print("ATTACKING STATE STARTED")

        radar = self.main_pointer.raydar

        objects = self.visible_objects(radar.objects)

        if not objects:

            self.states.set_state("searching")
            return

        target = min(
            objects.values(),
            key=lambda obj: obj["distance"]
        )

        self.target_object_id = target["id"]
        angle = target["angle"]

        if angle > 180:
            angle -= 360

        print("Initial target angle:", angle)

        self.stop_motors()
        self.radar_paused = True

        await self.main_pointer.wheel_odometry.turn_degree(
            angle,
            self.turn_speed,
            self.turn_acceleration
        )

        self.last_pursuit_scan = radar.scan_count

        print("Initial turn complete")

        self.radar_paused = False

        target_angle = None
        target_distance = None

        while self.states.is_state("attacking"):

            # Process fresh radar data
            if radar.scan_count != self.last_pursuit_scan:

                self.last_pursuit_scan = radar.scan_count

                objects = self.visible_objects(radar.objects)

                if not objects:

                    print("TARGET LOST")

                    self.stop_motors()
                    self.states.set_state("searching")
                    return

                target = min(
                    objects.values(),
                    key=lambda obj: abs(
                        obj["angle"] - 360
                        if obj["angle"] > 180
                        else obj["angle"]
                    )
                )

                self.target_object_id = target["id"]
                target_angle = target["angle"]
                target_distance = target["distance"]

                if target_angle > 180:
                    target_angle -= 360

                print("ATTACK TARGET")
                print("Angle:", target_angle)
                print("Distance:", target_distance)

            if target_angle is None:

                await wait(Movement.LOOP_INTERVAL_MS)
                continue

            # Steering correction
            correction = (
                target_angle * Movement.ATTACK_CORRECTION_GAIN
            )

            correction = max(
                -Movement.ATTACK_CORRECTION_MAX,
                min(Movement.ATTACK_CORRECTION_MAX, correction)
            )

            forward_speed = self.attack_speed

            if abs(target_angle) > 25:
                forward_speed *= 0.5

            left_speed = forward_speed - correction
            right_speed = forward_speed + correction

            left_speed = max(
                Movement.ATTACK_MIN_SPEED,
                min(Movement.ATTACK_MAX_SPEED, left_speed)
            )
            right_speed = max(
                Movement.ATTACK_MIN_SPEED,
                min(Movement.ATTACK_MAX_SPEED, right_speed)
            )

            self.motors.speed_LR(
                left_speed,
                right_speed
            )

            await wait(Strain.MONITOR_INTERVAL_MS)

    # ========================================
    # AVOIDING
    # ========================================

    async def avoiding(self):

        print("AVOIDING STATE STARTED")

        radar = self.main_pointer.raydar

        last_scan = radar.scan_count

        self.motors.speed_LR(
            self.avoid_speed,
            self.avoid_speed
        )

        while self.states.is_state("avoiding"):

            if radar.scan_count != last_scan:

                last_scan = radar.scan_count

                objects = self.visible_objects(radar.objects)

                if not objects:

                    self.states.set_state("searching")
                    return

                left_pressure = 0
                right_pressure = 0

                for obj in objects.values():

                    distance = obj["distance"]
                    angle = obj["angle"]

                    if angle > 180:
                        angle -= 360

                    if distance > self.avoid_distance:
                        continue

                    pressure = (
                        self.avoid_distance - distance
                    ) / self.avoid_distance

                    if angle < 0:
                        left_pressure += pressure
                    else:
                        right_pressure += pressure

                correction = (
                    right_pressure - left_pressure
                ) * self.avoid_correction

                correction = max(
                    -self.avoid_correction,
                    min(self.avoid_correction, correction)
                )

                left_speed = self.avoid_speed - correction
                right_speed = self.avoid_speed + correction

                left_speed = max(
                    Movement.AVOID_MIN_SPEED,
                    min(Movement.AVOID_MAX_SPEED, left_speed)
                )
                right_speed = max(
                    Movement.AVOID_MIN_SPEED,
                    min(Movement.AVOID_MAX_SPEED, right_speed)
                )

                self.motors.speed_LR(
                    left_speed,
                    right_speed
                )

                print("AVOIDANCE")
                print("Left speed:", left_speed)
                print("Right speed:", right_speed)

                # If only one object remains, attack it
                if len(objects) == 1:

                    print("ONE OBJECT REMAINING")

                    self.radar_paused = True
                    self.states.set_state("attacking")
                    return

            await wait(Strain.MONITOR_INTERVAL_MS)

    # ========================================
    # FLEEING
    # ========================================

    async def fleeing(self):

        print("FLEEING STATE STARTED")

        self.radar_paused = True

        # Reverse for 2 seconds
        print("REVERSING FOR 2 SECONDS")

        self.motors.speed_LR(
            -self.flee_speed,
            -self.flee_speed
        )

        await wait(Movement.FLEE_REVERSE_MS)

        # Turn 90 degrees
        print("TURNING 90 DEGREES")

        await self.main_pointer.wheel_odometry.turn_degree(
            Movement.FLEE_TURN_DEGREES,
            self.turn_speed,
            self.turn_acceleration
        )

        self.strain_active = False
        self.strain_timer.reset()

        self.radar_paused = False
        self.motors.speed_LR(
            self.moving_speed,
            self.moving_speed
        )

        print("FLEE COMPLETE - RESUMING SEARCH")

        self.states.set_state("searching")

    # ========================================
    # CONTINUOUS MOTOR STRAIN DETECTION
    # ========================================

    def detect_searching_strain(self, state):

        feedback = self.motors.get_motor_feedback()

        left = feedback["left"]
        right = feedback["right"]

        # Only monitor when both wheels are commanded to move
        if (
            left["commanded_speed"] < 100
            or right["commanded_speed"] < 100
        ):

            self.strain_active = False
            self.strain_timer.reset()

            return False

        left_ratio = (
            left["actual_speed"] / left["commanded_speed"]
        ) * 100

        right_ratio = (
            right["actual_speed"] / right["commanded_speed"]
        ) * 100

        # Motor.load() is already reported as a percentage (-100 to 100).
        required_load = self.flee_load_threshold
        major_strain = (
            left["load"] >= self.major_strain_load
            and left_ratio < self.major_strain_speed
        ) or (
            right["load"] >= self.major_strain_load
            and right_ratio < self.major_strain_speed
        )

        left_strain = (
            left_ratio < self.flee_speed_threshold
            and left["load"] > required_load
        )

        right_strain = (
            right_ratio < self.flee_speed_threshold
            and right["load"] > required_load
        )

        strain_detected = left_strain or right_strain

        if strain_detected:

            if not self.strain_active:

                print("PHYSICAL RESISTANCE STARTED")

                self.strain_active = True
                self.strain_timer.reset()

            elapsed = self.strain_timer.time()

            duration = (
                self.searching_strain_duration
                if state == "searching"
                else self.strain_duration
            )

            if major_strain:
                print("MAJOR MOTOR STRAIN - RECOVERY IMMEDIATE")
                return True

            if elapsed >= duration:

                print("CONTINUOUS STRAIN - RECOVERY TRIGGERED")
                return True

        else:

            if self.strain_active:
                print("RESISTANCE CLEARED - TIMER RESET")

            self.strain_active = False
            self.strain_timer.reset()

        return False

    # ========================================
    # PHYSICAL CONTACT MONITOR
    # ========================================

    async def monitor_physical_contact(self):

        print("PHYSICAL CONTACT MONITOR STARTED")

        while True:

            state = self.states.read_state()

            # Physical target contact during attacking
            if state == "attacking" and not self.target_contact:

                if self.detect_physical_target():

                    self.target_contact = True

                    print("TARGET PHYSICALLY REACHED")

            elif state != "attacking":

                self.contact_samples = 0
                self.target_contact = False

            # Continuous resistance monitoring
            if state in ("searching", "avoiding", "attacking"):

                if self.detect_searching_strain(state):

                    print("FLEEING - CONTINUOUS PHYSICAL RESISTANCE")

                    if self.target_object_id is not None:
                        self.ignored_object_id = self.target_object_id
                        self.ignore_target_timer.reset()

                    self.states.set_state("fleeing")

            else:

                self.strain_active = False
                self.strain_timer.reset()

            await wait(Strain.MONITOR_INTERVAL_MS)

    # ========================================
    # PHYSICAL TARGET DETECTION
    # ========================================

    def detect_physical_target(self):

        feedback = self.motors.get_motor_feedback()

        left = feedback["left"]
        right = feedback["right"]

        if (
            left["commanded_speed"] < 100
            or right["commanded_speed"] < 100
        ):

            self.contact_samples = 0
            return False

        left_ratio = (
            left["actual_speed"] / left["commanded_speed"]
        ) * 100

        right_ratio = (
            right["actual_speed"] / right["commanded_speed"]
        ) * 100

        required_load = self.contact_load_threshold

        left_contact = (
            left_ratio < self.contact_speed_threshold
            and left["load"] > required_load
        )

        right_contact = (
            right_ratio < self.contact_speed_threshold
            and right["load"] > required_load
        )

        if left_contact or right_contact:
            self.contact_samples += 1
        else:
            self.contact_samples = 0

        if self.contact_samples >= self.contact_required_samples:

            print("PHYSICAL TARGET CONTACT DETECTED")

            print("Left speed:", left_ratio)
            print("Right speed:", right_ratio)

            return True

        return False

    # ========================================
    # RADAR PROCESS
    # ========================================

    async def raydar(self):

        print("RADAR PROCESS STARTED")

        radar = self.main_pointer.raydar

        while True:

            if self.radar_paused:

                await wait(Movement.LOOP_INTERVAL_MS)
                continue

            state = self.states.read_state()

            if state == "searching":

                await radar.scan(
                    self.states,
                    "searching"
                )

            elif state == "attacking":

                await radar.short_scan(
                    self.states,
                    "attacking"
                )

            elif state == "avoiding":

                await radar.scan(
                    self.states,
                    "avoiding"
                )

            elif state == "color_objective":

                await radar.scan(
                    self.states,
                    "color_objective"
                )

            else:

                await wait(Movement.LOOP_INTERVAL_MS)

    # ========================================
    # EDGE DETECTION
    # ========================================

    async def determine_how_to_rotate(self):

        readings_left, reading_right, reading_back = (
            await self.main_pointer.colour.detect_all()
        )

        if not self.states.is_state("searching"):
            return

        objective_color = None

        for reading in (
            readings_left,
            reading_right,
            reading_back
        ):
            if reading in (2, 3, 4, 5):
                objective_color = reading
                break

        if (
            objective_color is not None
            and self.color_cooldown.time()
            >= self.color_cooldown_duration
        ):
            print("COLOUR OBJECTIVE DETECTED:", objective_color)
            self.color_cooldown.reset()
            self.states.set_state("color_objective")
            self.pending_objective_color = objective_color
            return

        left = readings_left == 0
        right = reading_right == 0
        back = reading_back == 0

        if left and right:

            self.stop_motors()

            await self.main_pointer.wheel_odometry.turn_degree(
                Movement.EDGE_TURN_DEGREES,
                Movement.TURN_SPEED,
                Movement.TURN_ACCELERATION
            )

        elif right:

            self.stop_motors()

            await self.main_pointer.wheel_odometry.turn_degree(
                -Movement.EDGE_TURN_DEGREES,
                Movement.TURN_SPEED,
                Movement.TURN_ACCELERATION
            )

        elif left:

            self.stop_motors()

            await self.main_pointer.wheel_odometry.turn_degree(
                Movement.EDGE_TURN_DEGREES,
                Movement.TURN_SPEED,
                Movement.TURN_ACCELERATION
            )

        if back:
            print("Edge detected at back")

    # ========================================
    # STATE MANAGEMENT
    # ========================================

    async def wait_for_state_change(self, old_state):

        while self.states.read_state() == old_state:
            await wait(Movement.LOOP_INTERVAL_MS)

    async def run_process(self, proces, state):

        self.active_process = state

        try:

            await multitask(
                proces(),
                self.wait_for_state_change(state),
                race=True
            )

        finally:

            self.stop_motors()
            self.active_process = None

    async def execute(self):

        print("Process manager starting")

        await multitask(
            self.state_process(),
            self.raydar(),
            self.monitor_physical_contact()
        )

    async def state_process(self):

        while True:

            state = self.states.read_state()

            if state == "idle":

                self.stop_motors()
                await wait(Movement.LOOP_INTERVAL_MS)
                continue

            proces = self.get_process(state)

            if proces is not None:

                print("STARTING PROCESS:", state)

                await self.run_process(proces, state)

            await wait(Movement.LOOP_INTERVAL_MS)

    def get_process(self, state):

        processes = {
            "launching": self.launching,
            "searching": self.searching,
            "attacking": self.attacking,
            "avoiding": self.avoiding,
            "fleeing": self.fleeing,
            "color_objective": self.color_objective
        }

        return processes.get(state)

    async def launching(self):
        pass

    async def color_objective(self):
        color = self.pending_objective_color
        if color is None:
            self.states.set_state("searching")
            return

        sequence_spin = (
            color == 3
            and self.last_objective_color == 2
            and not self.sequence_scored
        )

        print("EXECUTING COLOUR OBJECTIVE:", color)

        if sequence_spin:
            print("GREEN TO RED SEQUENCE CONFIRMED")

            for _ in range(Objectives.SEQUENCE_TURNS):
                if self.radar_danger():
                    print("RADAR DANGER - INTERRUPTING SEQUENCE SPIN")
                    self.states.set_state("fleeing")
                    return

                await self.main_pointer.wheel_odometry.turn_degree(
                    Objectives.SEQUENCE_TURN_DEGREES,
                    self.turn_speed,
                    self.turn_acceleration
                )

            self.sequence_scored = True

        elif color == 2:
            self.motors.speed_LR(
                Objectives.GREEN_SPEED,
                Objectives.GREEN_SPEED
            )
            await wait(Objectives.GREEN_DURATION_MS)

        elif color == 3:
            self.motors.speed_LR(0, 0)
            red_timer = StopWatch()

            while red_timer.time() < Objectives.RED_DURATION_MS:
                if self.radar_danger(
                    Objectives.RED_RADAR_DISTANCE_MM
                ):
                    print("RADAR DANGER - INTERRUPTING RED OBJECTIVE")
                    self.states.set_state("fleeing")
                    return

                await wait(Strain.MONITOR_INTERVAL_MS)

        elif color == 4:
            yellow_speed = int(
                self.moving_speed * Objectives.YELLOW_SPEED_RATIO
            )
            self.motors.speed_LR(yellow_speed, yellow_speed)
            await wait(Objectives.YELLOW_DURATION_MS)

        elif color == 5:
            self.motors.speed_LR(0, 0)
            await self.main_pointer.wheel_odometry.turn_degree(
                Objectives.BLUE_RIGHT_TURN_DEGREES,
                self.turn_speed,
                self.turn_acceleration
            )
            await wait(Objectives.BLUE_WAIT_MS)
            await self.main_pointer.wheel_odometry.turn_degree(
                Objectives.BLUE_LEFT_TURN_DEGREES,
                self.turn_speed,
                self.turn_acceleration
            )

        self.last_objective_color = color
        self.pending_objective_color = None
        self.motors.speed_LR(self.moving_speed, self.moving_speed)
        self.states.set_state("searching")


# ========================================
# STATES
# ========================================

class States:

    VALID_STATES = (
        "launching",
        "searching",
        "attacking",
        "avoiding",
        "fleeing",
        "color_objective",
        "idle"
    )

    def __init__(self):

        self.current_state = "searching"
        self.locked = False

    def set_state(self, state):

        if state not in self.VALID_STATES:

            print("Invalid state:", state)
            return False

        if self.locked:

            print("State is locked")
            return False

        if self.current_state != state:

            print(
                "State changing:",
                self.current_state,
                "->",
                state
            )

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
