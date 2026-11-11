# SumoBot Competition Feature Checklist

This checklist turns the requested robot features into implementation and match-readiness tasks. The feature backlog comes from the project request; the rule-derived requirements are listed separately below.

Rule references refer to the supplied **Competition Rules - Robotics Competition - F2026 Update 01** PDF.

## 1. Motor load and ground-contact detection

This is a project feature, not an explicit requirement in the rules PDF.

- [ ] Confirm motor load readings for ports A and D are available in the PC telemetry.
- [ ] Record load and speed with the robot sitting on the arena, with wheels lifted, and while pushing against a safe resistance.
- [ ] Decide whether load readings reliably distinguish wheel contact from a stall or collision; do not classify ground contact from one reading alone.
- [ ] Choose and document a threshold using repeated readings from the actual robot and arena.
- [ ] Add filtering or a short debounce so brief load changes do not rapidly change the ground-contact state.
- [ ] Display or log the detected state during testing.

## 2. Color detection

The arena uses colored tape that is 3 cm wide and 12 cm long. Correctly identifying a color before its action is required for the color-action points. (PDF pages 7-8)

- [ ] Calibrate the color sensor on the arena surface and on each tape color under expected lighting.
- [ ] Reliably distinguish green, red, yellow, and blue from the black arena and white markings.
- [ ] Detect a tape crossing once, rather than repeatedly while the sensor remains over the tape.
- [ ] Verify detection while moving at match speed and at different approach angles.
- [ ] Implement and time each rule action:
  - [ ] Green: run at 100% speed for 1 second, then return to base speed.
  - [ ] Red: stop for 2 seconds, then return to base speed.
  - [ ] Yellow: run at 25% speed for 1.5 seconds, then return to base speed.
  - [ ] Blue: stop, turn right, wait 0.5 seconds, then turn left.
- [ ] Verify the robot identifies the color before starting its action.

## 3. Color events and sequence handling

- [ ] Keep checking for color tapes during search, attack, and flee behavior.
- [ ] Handle a color event at high priority so it can pause the current mode, complete the required action, and resume safely.
- [ ] Use non-blocking timing so color checks and arena safety checks continue during waits and turns.
- [ ] Track the last detected color and reject duplicate readings from one tape crossing.
- [ ] Detect green followed by red and perform one continuous 360-degree in-place spin.
- [ ] Verify the green-to-red tapes are detected as the special sequence even when placed side by side, as shown in the arena example (PDF page 10).
- [ ] Track the sequence award so it can be claimed no more than once per match; the PDF assigns 6 points to this sequence (page 7).

## 4. Attack mode

- [ ] Detect and distinguish an opponent using the robot's allowed sensors.
- [ ] Enter attack mode only after opponent recognition.
- [ ] Implement an autonomous approach or push behavior and define when to stop attacking or return to search.
- [ ] Keep speed at or below 80% except while executing a listed color action or recognized-opponent attack code (PDF page 8).
- [ ] Test attack behavior without Bluetooth, Wi-Fi, or human control during a match.

## 5. Search mode

- [ ] Implement an autonomous search pattern that covers the arena and continues looking for opponents and colored tape.
- [ ] Detect and avoid the arena edge and the central hole.
- [ ] Keep ordinary search speed at or below 80% (PDF page 8).
- [ ] Confirm color events can interrupt search and search resumes afterward.
- [ ] Test that a temporary sensor miss or motor-speed change does not leave the robot immobile for more than 5 seconds, which would eliminate it (PDF page 6).

## 6. Flee mode

- [ ] Define the condition that switches the robot from attack or search into flee mode.
- [ ] Implement an autonomous escape direction that keeps the robot inside the arena and away from the central hole.
- [ ] Keep ordinary flee speed at or below 80% (PDF page 8).
- [ ] Confirm color events still take priority during fleeing and the robot resumes fleeing afterward.
- [ ] Test that recovery behavior prevents the robot from remaining immobile for more than 5 seconds (PDF page 6).

## Competition-rule checks

- [ ] Robot operates autonomously throughout a match with no human control or interference.
- [ ] Disable the brick's Bluetooth and Wi-Fi functionality during the match (PDF page 11).
- [ ] Start within a 20 cm x 20 cm square and hold still for 5 seconds after the start command (PDF page 5).
- [ ] Keep ordinary motor speed at or below 80%; use the rule exceptions only for a listed color action or after recognizing an opponent and executing attack code (PDF page 8).
- [ ] Stay within the build limits: one brick, at most four sensors, at most three motors, no tracks, and LEGO materials only (PDF page 11).
- [ ] Test a full autonomous run within the 2-minute match limit (PDF page 5).

## Source

Competition Rules - Robotics Competition - F2026 - Update 01.pdf, especially pages 5-8, 10, and 11.
