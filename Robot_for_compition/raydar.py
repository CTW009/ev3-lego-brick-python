
from pybricks.ev3devices import UltrasonicSensor
from pybricks.tools import wait
import math
from settings import Hardware, Radar


class RayDar:

    def __init__(self, motors):

        # ========================================
        # HARDWARE
        # ========================================

        self.motors = motors
        self.raydar_motor = self.motors.motor3
        self.raydar_sensor = UltrasonicSensor(Hardware.ULTRASONIC_PORT)

        # ========================================
        # RADAR CONFIGURATION
        # ========================================

        self.max_range = Radar.MAX_RANGE_MM
        self.scan_speed = Radar.SCAN_SPEED

        self.raydar_motor.reset_angle(0)

        self.scan_target = Radar.FULL_SCAN_START

        # Short scan configuration
        self.short_scan_limit = Radar.SHORT_SCAN_LIMIT_DEGREES
        self.short_scan_target = None
        self.short_scan_sample_interval = Radar.SHORT_SCAN_SAMPLE_INTERVAL_DEGREES

        self.scan_mode = None

        # ========================================
        # RAW MEASUREMENTS
        # ========================================

        self.measurements = []

        # ========================================
        # OBJECT TRACKING
        # ========================================

        self.previous_objects = {}
        self.object_counter = 0

        self.max_robot_width = Radar.MAX_ROBOT_WIDTH_MM
        self.max_robot_length = Radar.MAX_ROBOT_LENGTH_MM

        self.object_match_tolerance = Radar.OBJECT_MATCH_TOLERANCE_MM

        # ========================================
        # PUBLISHED RESULTS
        # ========================================

        self.objects = {}
        self.scan_count = 0

    # ========================================
    # INTERRUPTION CHECK
    # ========================================

    def should_interrupt(
        self,
        states=None,
        expected_state=None,
        pause_check=None
    ):

        if (
            states is not None
            and expected_state is not None
            and not states.is_state(expected_state)
        ):
            return True

        if pause_check is not None and pause_check():
            return True

        return False

    # ========================================
    # RADAR MOVEMENT
    # ========================================

    def rotate(self):

        print("Radar target:", self.scan_target)

        self.raydar_motor.run_target(
            self.scan_speed,
            self.scan_target,
            wait=False
        )

        self.scan_target = (
            0 if self.scan_target == 360 else 360
        )

    def get_angle(self):

        return self.raydar_motor.angle()

    async def move_radar(
        self,
        target,
        states=None,
        expected_state=None,
        pause_check=None
    ):

        if self.should_interrupt(
            states,
            expected_state,
            pause_check
        ):
            return False

        self.raydar_motor.run_target(
            self.scan_speed,
            target,
            wait=False
        )

        while not self.raydar_motor.done():

            if self.should_interrupt(
                states,
                expected_state,
                pause_check
            ):

                self.raydar_motor.stop()

                return False

            await wait(Radar.SCAN_LOOP_INTERVAL_MS)

        return not self.should_interrupt(
            states,
            expected_state,
            pause_check
        )

    # ========================================
    # MEASUREMENT RECORDING
    # ========================================

    def update_dict(self, angle, distance):

        self.measurements.append((
            angle,
            distance
        ))

    async def record_data(self):

        # Record approximate sensor angle.
        angle = self.raydar_motor.angle()

        # Request distance measurement.
        distance = await self.raydar_sensor.distance()

        print(
            "Angle:", angle,
            "Distance:", distance
        )

        self.update_dict(angle, distance)

    # ========================================
    # FULL 360 DEGREE SCAN
    # ========================================

    async def scan(
        self,
        states=None,
        expected_state=None
    ):

        print("Starting full scan")

        if self.scan_mode != "full":

            self.previous_objects.clear()
            self.scan_mode = "full"

        self.measurements.clear()

        # Choose the farther endpoint.
        current_angle = self.raydar_motor.angle()

        target = (
            360 if current_angle < 180 else 0
        )

        self.raydar_motor.run_target(
            self.scan_speed,
            target,
            wait=False
        )

        last_recorded_angle = None
        sample_interval = Radar.FULL_SCAN_SAMPLE_INTERVAL_DEGREES

        while not self.raydar_motor.done():

            if self.should_interrupt(
                states,
                expected_state
            ):

                print("Full scan interrupted")

                self.raydar_motor.stop()
                self.measurements.clear()

                return False

            angle = self.raydar_motor.angle()

            if (
                last_recorded_angle is None
                or abs(angle - last_recorded_angle)
                >= sample_interval
            ):

                await self.record_data()

                last_recorded_angle = (
                    self.raydar_motor.angle()
                )

                if self.should_interrupt(
                    states,
                    expected_state
                ):

                    self.raydar_motor.stop()
                    self.measurements.clear()

                    return False

            await wait(Radar.SCAN_LOOP_INTERVAL_MS)

        if self.should_interrupt(
            states,
            expected_state
        ):

            self.measurements.clear()
            return False

        await self.record_data()

        if self.should_interrupt(
            states,
            expected_state
        ):

            self.measurements.clear()
            return False

        print("Processing full scan")

        print(
            "Raw measurements:",
            len(self.measurements)
        )

        grouped_objects = self.group_objects()

        self.measurements.clear()

        print(
            "Grouped objects:",
            len(grouped_objects)
        )

        self.track_objects(grouped_objects)

        print("Full scan complete")
        print("Objects detected:", len(self.objects))
        print("Total scans:", self.scan_count)

        return True

    # ========================================
    # SHORT FORWARD SCAN
    # ========================================

    async def short_scan(
        self,
        states=None,
        expected_state=None,
        pause_check=None
    ):

        print("Starting short scan")

        # Reset tracking when changing scan modes.
        if self.scan_mode != "short":

            self.previous_objects.clear()
            self.scan_mode = "short"

        self.measurements.clear()

        # ========================================
        # POSITION AT LEFT EDGE
        # ========================================

        if self.short_scan_target is None:

            success = await self.move_radar(
                -self.short_scan_limit,
                states,
                expected_state,
                pause_check
            )

            if not success:

                self.measurements.clear()
                self.short_scan_target = None

                return False

            self.short_scan_target = (
                self.short_scan_limit
            )

        # ========================================
        # START SWEEP
        # ========================================

        target = self.short_scan_target

        if self.should_interrupt(
            states,
            expected_state,
            pause_check
        ):

            self.measurements.clear()
            self.short_scan_target = None

            return False

        self.raydar_motor.run_target(
            self.scan_speed,
            target,
            wait=False
        )

        last_recorded_angle = None

        # ========================================
        # RECORD WHILE MOVING
        # ========================================

        while not self.raydar_motor.done():

            if self.should_interrupt(
                states,
                expected_state,
                pause_check
            ):

                print("Short scan interrupted")

                self.raydar_motor.stop()

                self.measurements.clear()
                self.short_scan_target = None

                return False

            angle = self.raydar_motor.angle()

            if (
                last_recorded_angle is None
                or abs(angle - last_recorded_angle)
                >= self.short_scan_sample_interval
            ):

                await self.record_data()

                last_recorded_angle = (
                    self.raydar_motor.angle()
                )

                # Sensor reading is awaited, so check
                # for interruption again afterwards.
                if self.should_interrupt(
                    states,
                    expected_state,
                    pause_check
                ):

                    self.raydar_motor.stop()

                    self.measurements.clear()
                    self.short_scan_target = None

                    return False

            await wait(Radar.SCAN_LOOP_INTERVAL_MS)

        # ========================================
        # VERIFY BEFORE PROCESSING
        # ========================================

        if self.should_interrupt(
            states,
            expected_state,
            pause_check
        ):

            self.measurements.clear()
            self.short_scan_target = None

            return False

        # Final measurement.
        await self.record_data()

        if self.should_interrupt(
            states,
            expected_state,
            pause_check
        ):

            self.measurements.clear()
            self.short_scan_target = None

            return False

        # ========================================
        # PROCESS SCAN
        # ========================================

        print("Processing short scan")

        print(
            "Raw measurements:",
            len(self.measurements)
        )

        grouped_objects = self.group_objects()

        self.measurements.clear()

        print(
            "Grouped objects:",
            len(grouped_objects)
        )

        self.track_objects(grouped_objects)

        print("Short scan complete")
        print("Objects detected:", len(self.objects))
        print("Total scans:", self.scan_count)

        # ========================================
        # ALTERNATE SCAN DIRECTION
        # ========================================

        self.short_scan_target = (
            -self.short_scan_limit
            if target > 0
            else self.short_scan_limit
        )

        return True

    # ========================================
    # OBJECT GROUPING
    # ========================================

    def group_objects(
        self,
        max_gap=100,
        max_angle_gap=15,
        min_points=2
    ):

        points = []

        # Convert measurements into Cartesian coordinates.
        for angle, distance in self.measurements:

            if not isinstance(distance, (int, float)):
                continue

            if distance <= 0 or distance >= self.max_range:
                continue

            radians = math.radians(angle % 360)

            x = distance * math.cos(radians)
            y = distance * math.sin(radians)

            points.append({

                "angle": angle % 360,
                "distance": distance,
                "x": x,
                "y": y

            })

        # Sort measurements by angle.
        points.sort(key=lambda p: p["angle"])

        groups = []
        current_group = []

        for point in points:

            if not current_group:

                current_group.append(point)
                continue

            previous = current_group[-1]

            separation = math.sqrt(
                (point["x"] - previous["x"]) ** 2 +
                (point["y"] - previous["y"]) ** 2
            )

            angle_difference = (
                point["angle"] - previous["angle"]
            )

            if (
                separation <= max_gap
                and angle_difference <= max_angle_gap
            ):

                current_group.append(point)

            else:

                groups.append(current_group)
                current_group = [point]

        if current_group:
            groups.append(current_group)

        # Join groups crossing the 0/360 boundary.
        if len(groups) > 1:

            first_group = groups[0]
            last_group = groups[-1]

            first = first_group[0]
            last = last_group[-1]

            separation = math.sqrt(
                (first["x"] - last["x"]) ** 2 +
                (first["y"] - last["y"]) ** 2
            )

            angle_difference = (
                first["angle"] + 360 - last["angle"]
            )

            if (
                separation <= max_gap
                and angle_difference <= max_angle_gap
            ):

                merged_group = last_group + first_group

                groups = (
                    [merged_group] + groups[1:-1]
                )

        detected_objects = []

        for group in groups:

            if len(group) < min_points:
                continue

            avg_x = sum(
                p["x"] for p in group
            ) / len(group)

            avg_y = sum(
                p["y"] for p in group
            ) / len(group)

            avg_distance = math.sqrt(
                avg_x ** 2 + avg_y ** 2
            )

            avg_angle = math.degrees(
                math.atan2(avg_y, avg_x)
            ) % 360

            first = group[0]
            last = group[-1]

            width = math.sqrt(
                (last["x"] - first["x"]) ** 2 +
                (last["y"] - first["y"]) ** 2
            )

            detected_objects.append({

                "x": avg_x,
                "y": avg_y,

                "angle": avg_angle,
                "distance": avg_distance,

                "width": width,

                "presence": False,

                "points": len(group)

            })

        return detected_objects

    # ========================================
    # OBJECT CLASSIFICATION
    # ========================================

    def classify_object(self, obj):

        if obj["presence"]:
            return "maybe_robot"

        if obj["width"] > self.max_robot_width:
            return "maybe_robot"

        return "N/A"

    # ========================================
    # OBJECT TRACKING
    # ========================================

    def track_objects(self, current_objects):

        matched_previous = set()

        for obj in current_objects:

            best_match = None
            best_distance = self.object_match_tolerance

            # Find closest previous object.
            for object_id, previous in (
                self.previous_objects.items()
            ):

                if object_id in matched_previous:
                    continue

                separation = math.sqrt(
                    (obj["x"] - previous["x"]) ** 2 +
                    (obj["y"] - previous["y"]) ** 2
                )

                if separation < best_distance:

                    best_distance = separation
                    best_match = object_id

            # Existing object.
            if best_match is not None:

                previous = self.previous_objects[best_match]

                obj["id"] = best_match

                obj["moving"] = (
                    best_distance > 30
                )

                obj["movement"] = {

                    "x": obj["x"] - previous["x"],
                    "y": obj["y"] - previous["y"]

                }

                matched_previous.add(best_match)

            # New object.
            else:

                self.object_counter += 1

                obj["id"] = self.object_counter

                obj["moving"] = False

                obj["movement"] = {

                    "x": 0,
                    "y": 0

                }

            obj["classification"] = (
                self.classify_object(obj)
            )

        # Save current object positions.
        self.previous_objects = {

            obj["id"]: obj.copy()

            for obj in current_objects

        }

        # Publish latest scan results.
        self.objects = {

            obj["id"]: obj

            for obj in current_objects

        }

        self.scan_count += 1

        for object_id, obj in self.objects.items():

            print(
                "Object:", object_id,
                "Angle:", obj["angle"],
                "Distance:", obj["distance"],
                "Width:", obj["width"],
                "Points:", obj["points"],
                "Classification:", obj["classification"]
            )

    # ========================================
    # SENSOR TEST
    # ========================================

    async def test_sensor(self):

        print("Radar sensor test started")

        while True:

            distance = await self.raydar_sensor.distance()

            print("Distance:", distance)

            await wait(Radar.TEST_SENSOR_INTERVAL_MS)

    # ========================================
    # GROUP MERGING
    # ========================================

    def merge_groups(
        self,
        objects,
        max_distance=180,
        max_angle=25
    ):

        changed = True

        while changed:

            changed = False

            for i in range(len(objects)):

                if changed:
                    break

                for j in range(i + 1, len(objects)):

                    a = objects[i]
                    b = objects[j]

                    separation = math.sqrt(
                        (a["x"] - b["x"]) ** 2 +
                        (a["y"] - b["y"]) ** 2
                    )

                    angle_difference = abs(
                        (a["angle"] - b["angle"] + 180)
                        % 360 - 180
                    )

                    if (
                        separation <= max_distance
                        and angle_difference <= max_angle
                    ):

                        total_points = (
                            a["points"] + b["points"]
                        )

                        x = (
                            a["x"] * a["points"] +
                            b["x"] * b["points"]
                        ) / total_points

                        y = (
                            a["y"] * a["points"] +
                            b["y"] * b["points"]
                        ) / total_points

                        merged = {

                            "x": x,
                            "y": y,

                            "angle": math.degrees(
                                math.atan2(y, x)
                            ) % 360,

                            "distance": math.sqrt(
                                x * x + y * y
                            ),

                            "width": max(
                                a["width"],
                                b["width"],
                                separation
                            ),

                            "presence": False,
                            "points": total_points

                        }

                        objects[i] = merged
                        objects.pop(j)

                        changed = True
                        break

        return objects
