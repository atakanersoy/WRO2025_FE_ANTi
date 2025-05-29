# Software Documentation

This folder contains the source code for Team ANTi’s WRO 2025 Future Engineers robot, written in **MicroPython** and running on the **STM32H747 dual-core microcontroller**. This documentation was last updated on **Thursday, May 29, 2025, at 08:17 PM +03**.

## Software Overview
Our software is designed to handle the WRO 2025 challenges: navigating dynamic racetracks, respecting traffic signs, and performing parallel parking. Key features include:
- **Computer Vision**: Uses the **GC2145 2MP camera** and **CIELAB color space** for robust detection of track elements and traffic signs.
- **Sensor Fusion**: Integrates data from the **VL53L1X ToF sensor**, **LSM6DSOX IMU**, and camera for precise navigation.
- **Control System**: Manages the **Feetech FS0307 servo** for steering and **1500 RPM N20 motor** for propulsion.

![Example Detection](other/example_detection.jpg)

## Programming Environment
- **Language**: MicroPython (chosen for rapid development and compatibility with STM32H747).
- **Interface**: Programming via micro USB cable.
- **Libraries**:
  - `machine`: For hardware control (PWM, GPIO).
  - `pyb`: For STM32-specific functions.
- **Development Tools**: VS Code.

## Algorithms
- **Track Navigation**:
  - Uses CIELAB color space to differentiate track elements (lanes, walls, signs).
  - Lane-following algorithm adjusts steering based on camera input.
  - ToF sensor provides distance data for obstacle avoidance.
- **Traffic Sign Detection**:
  - Red signs: Steer to the right of the lane.
  - Green signs: Steer to the left of the lane.
  - CIELAB’s linear color space simplifies calibration and detection.
- **Parallel Parking**:
  - Combines camera and ToF data to locate the parking zone.
  - Executes a trajectory using Ackermann steering geometry to avoid it.

![Parallel Parking Setup](parallel_park_setup.jpg)

- **Sensor Fusion**:
  - Adaptive low-pass filter, Adaptive Moving Average (AMA) filter, and PID control algorithms integrate IMU and ToF data for stable navigation.
  - Camera data is prioritized for visual feedback, with ToF as a fallback for distance validation.

![Obstacle Challenge Strategy 1](other/obstacle_challenge_strategy_1.jpg)

![Obstacle Challenge Strategy 2](other/obstacle_challenge_strategy_2.jpg)

## File List
- `main.py`: Main control loop for autonomous operation.
- `vision.py`: Computer vision processing (CIELAB color space).
- `control.py`: Steering and motor control algorithms.
- `sensors.py`: Sensor data acquisition and fusion.
- `parking.py`: Parallel parking routine.

* [Placeholder: Include code snippets or link to specific files]*

## Coding Practices
- **Modularity**: Code is organized into separate modules for vision, control, and sensor handling to test each system separately.
- **Documentation**: Inline comments and function docstrings ensure clarity.
- **Testing**: Iterative testing on a test WRO track to validate algorithms.

## Setup Instructions
1. Connect the robot to a computer via micro USB.
2. Copy the contents of the `src` folder to the microcontroller.
3. Switch on the LiPo Rider Plus to power the robot.
4. Press the KLS7-TS1204 tactile switch to start the robot.

For hardware details, see [Schemes Documentation](../schemes/README.md).