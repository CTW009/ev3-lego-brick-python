from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.ev3devices import Motor, UltrasonicSensor


MAX_DISTANCE_MM = 500
MOTOR_SPEED_DEG_PER_SEC = 100
MOTOR_ACCELERATION_UP_DEG_PER_SEC2 = 500
MOTOR_ACCELERATION_DOWN_DEG_PER_SEC2 = 250
SAMPLE_INTERVAL_MS = 1
MAX_ANGLE_GAP_DEG = 5
MAX_DISTANCE_JUMP_MM = 100
MIN_OBJECT_SAMPLES = 4
MIN_OBJECT_WIDTH_DEG = 6


def identify_objects(readings):
    """Group neighboring valid sonar readings into object detections."""
    by_angle = {}
    for angle, distance in readings.items():
        if distance is not None and 0 < distance <= MAX_DISTANCE_MM:
            by_angle[angle % 360] = distance

    samples = sorted(by_angle.items())
    if not samples:
        return []

    clusters = [[samples[0]]]
    for sample in samples[1:]:
        previous = clusters[-1][-1]
        angle_gap = sample[0] - previous[0]
        distance_jump = abs(sample[1] - previous[1])
        if angle_gap <= MAX_ANGLE_GAP_DEG and distance_jump <= MAX_DISTANCE_JUMP_MM:
            clusters[-1].append(sample)
        else:
            clusters.append([sample])

    # Join a cluster that crosses the 0/360 degree boundary.
    if len(clusters) > 1:
        first = clusters[0]
        last = clusters[-1]
        wrap_gap = 360 - last[-1][0] + first[0][0]
        if (
            wrap_gap <= MAX_ANGLE_GAP_DEG
            and abs(last[-1][1] - first[0][1]) <= MAX_DISTANCE_JUMP_MM
        ):
            clusters[0] = last + first
            clusters.pop()

    detections = []
    for cluster in clusters:
        if len(cluster) < MIN_OBJECT_SAMPLES:
            continue

        angles = [sample[0] for sample in cluster]
        if max(angles) - min(angles) > 180:
            angles = [angle + 360 if angle < 180 else angle for angle in angles]

        center_angle = int(sum(angles) / len(angles)) % 360
        average_distance = int(sum(sample[1] for sample in cluster) / len(cluster))
        angular_width = max(angles) - min(angles)
        if angular_width < MIN_OBJECT_WIDTH_DEG:
            continue
        detections.append((center_angle, average_distance, angular_width, len(cluster)))

    detections.sort()
    objects = []
    for index, detection in enumerate(detections):
        objects.append(
            {
                "id": index + 1,
                "angle": detection[0],
                "distance": detection[1],
                "width": detection[2],
                "samples": detection[3],
            }
        )
    return objects


class RayDar:
    def __init__(self):
        self.raydar_motor = Motor(port=Port.B, gears=[12, 20], reset_angle=False)
        _, _, torque_limit = self.raydar_motor.control.limits()
        self.raydar_motor.control.limits(
            speed=MOTOR_SPEED_DEG_PER_SEC,
            acceleration=(
                MOTOR_ACCELERATION_UP_DEG_PER_SEC2,
                MOTOR_ACCELERATION_DOWN_DEG_PER_SEC2,
            ),
            torque=torque_limit,
        )
        self.distance_sensor = UltrasonicSensor(Port.S4)
        self.current_angle = self.raydar_motor.angle()
        self.current_distance = 0
        self.angle_distance = {}  # angle: distance in mm
        self.objects = {}  # scan-local object id: detection details
        self.set_angle = 360

    def rotate(self):
        self.raydar_motor.run_target(
            speed=MOTOR_SPEED_DEG_PER_SEC,
            target_angle=self.set_angle,
            wait=False,
        )

    def measure_distance(self):
        return self.distance_sensor.distance()

    def identify_objects(self):
        return identify_objects(self.angle_distance)


ray = RayDar()
ray.rotate()

while True:
    angle = ray.raydar_motor.angle()
    distance = ray.measure_distance()
    ray.current_angle = angle
    ray.current_distance = distance
    if distance is not None and 0 < distance <= MAX_DISTANCE_MM:
        ray.angle_distance[angle] = distance
    else:
        ray.angle_distance.pop(angle, None)

    # The desktop test viewer listens for these telemetry lines.
    print("RADAR|{0}|{1}".format(angle, distance))

    if ray.raydar_motor.done():
        detections = ray.identify_objects()
        ray.objects = {item["id"]: item for item in detections}
        for item in detections:
            print(
                "Object {0}: {1} mm away at {2} degrees; width about {3} degrees".format(
                    item["id"],
                    item["distance"],
                    item["angle"],
                    item["width"],
                )
            )
            print(
                "OBJECT|{0}|{1}|{2}|{3}|{4}".format(
                    item["id"],
                    item["angle"],
                    item["distance"],
                    item["width"],
                    item["samples"],
                )
            )
        print("Identified {0} object(s) in this scan.".format(len(detections)))
        print("SCAN|COMPLETE|{0}".format(len(detections)))
        wait(800)
        print("SCAN|CLEAR")
        ray.angle_distance.clear()
        ray.objects.clear()
        ray.set_angle = 0 if ray.set_angle != 0 else 370
        ray.rotate()

    wait(SAMPLE_INTERVAL_MS)
