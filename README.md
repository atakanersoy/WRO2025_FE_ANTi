<center><h1>WRO 2025 Future Engineers – ANTi</h1></center>

<img src="other/transparent_only_logo_WRO2025_FE_ANTi_logo_05-05-2025.png" alt="Banner" width="600">

<center>
<a href="https://www.instagram.com/anti.wro/"><img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white" alt="Instagram"></a>
<a href="https://www.youtube.com/@solipsy."><img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white" alt="YouTube"></a>
</center>

---

## 🏆 TURKISH NATIONAL CHAMPION – READY FOR SINGAPORE FINALS  

Welcome to the GitHub repository of **Team ANTi**, competing in the **World Robot Olympiad™ (WRO®) Future Engineers 2025** category. Our team is made up of Turkish students who have designed a compact, innovative, and autonomous self-driving vehicle to tackle the dynamic challenges of the WRO 2025 competition. Our team name, **ANTi**, reflects our philosophy: like an **ANT**, our robot is exceptionally small yet highly capable, pushing the boundaries of minimalism in design. The "**ANT**i" signifies our competitive spirit, standing "versus the world" in pursuit of engineering excellence.

Our mission was to create the smallest possible robot for the WRO 2025 challenge, leveraging our expertise in electrical, mechanical, and software engineering to test the limits of the 3 m x 3 m game field. After winning the Turkish National Final, we rebuilt, re-tuned, and re-documented every subsystem for the International Final in Singapore on 26–28 Nov 2025.
Current best times on the 3 m x 3 m field:
- **Open Challenge**: 16 s full score  
- **Obstacle Challenge**: 35 s full score  

Full videos are available in the [video folder](video/README.md).  

The car keeps its title of **World’s Smallest Self Driving Autonomous Vehicle** (about 1/76 scale, **69 mm x 53 mm x 57 mm**) while now carrying more intelligence and sensors than ever before. We challenged ourselves beyond the traditional competition rules by pursuing minimal size alongside advanced engineering functionality. 
Guided by our vision to **"never stop developing unless we stop learning,"** we have created a vehicle that showcases precision, adaptability, and a milestone in compact robotics design on a global scale. This documentation was last updated on **Monday, Nov 03 2025, at 08:47 AM +03**

---

## 📚 Table of Contents
- [📂 Folder Structure](#folder-structure)
- [👥 The Team](#the-team)
- [🎯 Challenge Overview](#challenge-overview)
- [🤖 Our Robot](#our-robot)
- [🔧 Hardware Documentation](#hardware-documentation)
- [💻 Software Documentation](#software-documentation)
- [⚙ Mechanical Characteristics](#mechanical-characteristics)
- [📹 Performance Videos](#performance-videos)
- [📸 Team Photos](#team-photos)
- [🚗 Vehicle Photos](#vehicle-photos)
- [🛠 Other Resources](#other-resources)
- [🌐 GitHub Utilization](#github-utilization)
- [📜 License](#license)

---

## 📂 Folder Structure <a id="folder-structure"></a>
```
📦 WRO2025_FE_ANTi
├── 📁 matlab                # MATLAB tools and simulations for virtual tests and verification
├── 📁 models                # 3D CAD models for printing and mechanical design characteristics
├── 📁 schemes               # Schematic diagrams, wiring and electronics information
├── 📁 src                   # Source code for robot control and strategy explanations
├── 📁 t-photos              # Team photos (official and fun)
├── 📁 v-photos              # Vehicle photos from multiple angles
├── 📁 video                 # Performance and testing videos
├── 📁 other                 # Additional resources (components, images, engineering details)
└── 📄 README.md             # Project overview and documentation
```

Detailed documentation for each folder is available in respective `.md` files:
- [MATLAB Documentation](matlab/README.md)
- [Models Documentation](models/README.md)
- [Schemes Documentation](schemes/README.md)
- [Software Documentation](src/README.md)
- [Team Photos](t-photos/README.md)
- [Vehicle Photos](v-photos/README.md)
- [Performance Videos](video/README.md)
- [Other Resources](other/README.md)

---

## 👥 The Team <a id="the-team"></a>
Team ANTi includes passionate students from Türkiye, guided by a coach. Each member brings unique skills to the project, from electronics to computer vision.

<img src="t-photos/team_official.jpg" alt="Official Team Moment" width="600">
<img src="t-photos/workplace.jpg" alt="Team ANTi at Work" width="600">

### Members
- **Atakan Ersoy** (Team Leader)  
  *Role*: Electronics, Mechanical Design, Software, Strategy Integration  
  *Background*: Sophomore, Electrical and Electronics Engineering, Koç University (2025)  
  *Contact*: [atakan@atakanersoy.com](mailto:atakan@atakanersoy.com), [aersoy24@ku.edu.tr](mailto:aersoy24@ku.edu.tr)  
  *Born*: 2006, Türkiye
- **Ege Özokan**  
  *Role*: Computer Vision Research, Strategy  
  *Background*: Freshman, Computer Engineering, Politecnico di Torino (2025)  
  *Born*: 2006, Türkiye

### Coach
- **Ali Aral Eren**  
  *Role*: Team Coach, Connector  
  *Background*: Alumni, Electrical and Electronics Engineering, Koç University (2025)  
  *Born*: 2003, Türkiye

---

## 🎯 Challenge Overview <a id="challenge-overview"></a>
The **WRO 2025 Future Engineers** category challenges teams to build an autonomous self-driving vehicle capable of navigating dynamic racetracks. The competition consists of two rounds:

### Open Challenge
- **Objective**: Complete three laps autonomously.
- **Track Conditions**: Randomly positioned internal walls create varied layouts and lane widths, testing adaptability and precision.

### Obstacle Challenge
- **Objective**: Complete three laps while respecting traffic signs and performing parallel parking.
- **Traffic Signs**:
  - *Red Signs*: Stay to the right of the lane.
  - *Green Signs*: Stay to the left of the lane.
- **Parking**: After three laps, locate and execute a precise parallel parking maneuver in a designated zone.

### Key Evaluation Areas
- Performance and adaptability in randomized conditions.
- Precision in maneuvers, especially parallel parking.
- Comprehensive, public engineering documentation on GitHub.

### Educational Emphasis
- Advanced *computer vision* and *sensor fusion*.
- Control systems for steering-based kinematics.
- Problem-solving, project management, teamwork, and creativity.
- Clear and detailed documentation of engineering processes.

This challenge fosters innovation in STEM and robotics, encouraging students to develop practical solutions to complex problems.

---

## 🤖 Our Robot <a id="our-robot"></a>
<img src="v-photos/front_view.jpg" alt="ANTi Robot Front View" width="600">

Team ANTi’s robot is a marvel of minimalism, measuring just **69mm (L) x 53mm (W) x 57mm (H)**, making it the publicly known world's smallest autonomous vehicle ever designed for the WRO Future Engineers category. Built entirely from scratch, our robot features a **3D-printed chassis** and a custom built **Ackermann steering mechanism**, optimized for precision and small size. The processing is split between two microcontrollers for maximum efficiency. An **STM32H747 dual-core microcontroller** is dedicated to camera operations, processing data from the **GC2145 2MP camera**. A separate **nRF52832 microcontroller** handles all other sensor computations and data processing.

For navigation, the robot uses a front-mounted **VL53L1X ToF sensor** for general obstacle avoidance. For the specific challenge of detecting the obstacle parking start direction, it employs left and right **VL53L3CX ToF sensors**, which use a window lens for a narrow FoV to achieve long-range detection. Powered by a **1500 RPM N20 motor**, our design philosophy, inspired by the efficiency of an ant, pushes the boundaries of compact robotics while maintaining high performance.

Detailed vehicle photos with labels showing aspects of mobility, power systems, sensing, and obstacle management can be found at [Vehicle Photos](v-photos/README.md).

<img src="models/design_to_life.jpg" alt="Design to Life" width="600">

---

## 🔧 Hardware Documentation <a id="hardware-documentation"></a>
Our hardware is meticulously selected and integrated using custom **pertinax boards** for minimal size and weight. Below is a summary of all key components with images, followed by the complete Bill of Materials (BOM) for the wiring diagram.

### Key Components
| Component            | Description                                      | Image                                      |
|----------------------|--------------------------------------------------|--------------------------------------------|
| STM32H747            | Dual-core, high-performance camera microcontroller| <img src="other/STM32H747.jpg" alt="STM32H747" width="600"> |
| GC2145               | 2MP CMOS camera, 80° view angle, <1.0% distortion | <img src="other/GC2145.jpg" alt="GC2145 Camera" width="600"> |
| nRF52832             | Sensor microcontroller dedicated to handling sensor computations and data processing      | <img src="other/nRF52832.jpg" alt="nRF52832" width="600"> |
| VL53L3CX             | ToF sensor with 700cm range using window lens for narrow FoV       | <img src="other/VL53L3CX.jpg" alt="VL53L3CX" width="600"> |
| VL53L1X              | ToF sensor, 400cm range, full FoV                | <img src="other/VL53L1X.jpg" alt="VL53L1X" width="600"> |
| LSM6DSOX             | 6-axis accelerometer and gyroscope IMU           | <img src="other/LSM6DSOX.jpg" alt="LSM6DSOX" width="600"> |
| Feetech FS0307       | Submicro servo motor, chosen for minimal size    | <img src="other/FS0307.jpg" alt="FS0307 Servo" width="600"> |
| DRV8833              | PWM motor driver                                 | <img src="other/DRV8833.jpg" alt="DRV8833" width="600"> |
| 1500 RPM N20         | Brushed DC Motor with Hall effect magnetic encoder, selected for small size and speed | <img src="other/1500rpm_N20_dc_motor_encoder.jpg" alt="N20 Motor" width="600"> |
| Power-Xtra PX103035  | 30x35x10mm, 1000mAh LiPo battery with PCM        | <img src="other/PX103035.jpg" alt="Battery" width="600"> |
| LiPo Rider Plus      | USB-C charger/booster with power switch          | <img src="other/LiPo_Rider_Plus.jpg" alt="LiPo Rider Plus" width="600"> |
| SX1308               | 2A DC-DC Step-Up voltage booster                 | <img src="other/SX1308.jpg" alt="SX1308" width="600"> |
| BOB-12009            | 3.3V–5V logic level converter                    | <img src="other/BOB12009.jpg" alt="BOB-12009" width="600"> |
| LEGO 87697           | Tire, 21mm diameter, 12mm width, good traction   | <img src="other/lego87697_wheel_comparison.jpg" alt="LEGO 87697 Wheel Comparison" width="600"> |

### Additional Hardware Details
- **Motor Speed**: Selected based on calculations comparing wheel/tire sizes and motor speeds for the 3m x 3m game field. You can see one of our comparisons with different wheels during the development process from [motor_speed_calculations.jpg](other/motor_speed_calculations.jpg). The final configuration achieves a theoretical maximum speed of **1.72 m/s**, calculated from the 1500 RPM N20 motor through a 26:25 gear reduction driving the 21mm diameter wheels. The Calculation is as Follows:

  - The wheel RPM is calculated as:

  $$
  \text{RPM}_{\text{wheel}} = \text{RPM}_{\text{motor}} \times \text{Gear Ratio} = 1500 \times \frac{26}{25} = 1560 \, \text{RPM}
  $$

  - The speed is calculated using:

  $$
  \text{Speed} = (2 \times \pi \times r) \times \frac{\text{RPM}_{\text{wheel}}}{60}
  $$

  - Where the radius in meters is:

  $$
  r = \frac{21 \, \text{mm}}{2} = 10.5 \, \text{mm} = 0.0105 \, \text{m}
  $$

  - Thus, the speed can be calculated as:

  $$
  \text{Speed} = (2 \times \pi \times 0.0105) \times \frac{1560}{60} \approx 1.72 \, \text{m/s}
  $$

- **Battery Performance**: 
  - **Run Time:** The battery is capable of operating for approximately 4 to 5 hours under typical usage conditions. This duration can vary based on the load and the efficiency of the connected components.
  
  - **Charge Time:** The battery requires about 45 minutes to reach a full charge when connected to a USB-C port at 5V. This charging process utilizes a maximum input power of 10W at 2A, ensuring efficient energy transfer.

  - **Power Specifications:** The minimum power draw during operation is around 0.8W, while the total current consumption fluctuates between 200 to 250 mA, depending on the specific demands of the device while regulating the voltage levels.

  All calculations related to these performance metrics were performed using watt-voltage relationships, ensuring accurate assessments of the battery's capabilities.

- **3D Printing**: Used for prototyping (see [models/3d_printer.jpg](models/3d_printer.jpg)).

<img src="other/soldering_setup.jpg" alt="Soldering Setup" width="600">
<p><em>Our soldering setup for assembling the pertinax boards.</em></p>

<img src="schemes/wiring_diagram.jpg" alt="Wiring Diagram" width="600">
<p><em>Complete wiring diagram.</em></p>

### Bill of Materials (BOM) for Wiring Diagram
The following BOM details all components used in the robot’s electrical system, as documented in the [Schemes Documentation](schemes/README.md):

| Component           | Quantity | Type                      | Description                                   |
|---------------------|----------|---------------------------|-----------------------------------------------|
| STM32H747           | 1        | Camera Microcontroller    | Dual-core, high-performance microcontroller   |
| GC2145              | 1        | 2MP Camera                | 2MP CMOS camera, 2.2mm focal length, 80° view |
| nRF52832            | 1        | Sensor Microcontroller    | Handling sensor computations and data processing   |
| VL53L3CX            | 2        | ToF Sensor                | ToF sensor, 700cm range, narrow FoV window lens    |
| VL53L1X             | 1        | ToF Sensor                | ToF sensor, 400cm range, full FoV             |
| LSM6DSOX            | 1        | 6-axis IMU                | 6-axis accelerometer and gyroscope IMU        |
| Feetech FS0307      | 1        | Servo Motor               | Submicro servo motor                          |
| DRV8833             | 1        | Motor Driver              | PWM motor driver                              |
| 1500 RPM N20        | 1        | DC Motor with Encoder     | Motor with quadrature encoder (2 Hall-effect) |
| Power-Xtra PX103035 | 1        | 3.7V 1000mAh LiPo Battery | 3.7V 1000mAh LiPo battery with PCM            |
| LiPo Rider Plus     | 1        | Charger/Booster           | USB-C charger/booster with power switch       |
| SX1308              | 1        | Voltage Booster           | 2A DC-DC Step-Up voltage booster              |
| BOB-12009           | 1        | Logic Level Converter     | 3.3V–5V logic level converter                 |
| KLS7-TS1204         | 1        | Tactile Switch            | Tactile switch (start action)                 |
| LEGO 87697          | 4        | Tire                      | Tire, 21mm diameter, 12mm width               |

For detailed schematics, power distribution, and wiring information, refer to the [Schemes Documentation](schemes/README.md).

---

## 💻 Software Documentation <a id="software-documentation"></a>
Our camera software is written in **MicroPython** and runs on the STM32H747. It uses the **CIELAB color space** for robust computer vision, enabling precise differentiation of track elements and traffic signs. The software integrates sensor data (camera, ToF, IMU) for navigation and control, with algorithms optimized for the dynamic WRO racetrack. Our side sensor software is written in **Arduino IDE** and runs on the nRF52832. These two microcontrollers constantly maintain a stable and bidirectional communication using the UART protocol.

<img src="other/image_processing_setup.jpg" alt="Image Processing Setup" width="600">

### Obstacle Navigation Strategy
Our robot navigates the obstacle course using a combination of sensor fusion and computer vision:
- **Traffic Sign Detection**: The GC2145 camera detects red/green signs using CIELAB color space. Red signs trigger a right-lane adjustment, green signs a left-lane adjustment. The amount of this adjustment is calculated based on the colored objects position on the camera window.
<img src="src/example_detection.jpg" alt="Example Detection" width="600">
<img src="src/example_all_detection.jpg" alt="Example All Detection" width="600">

- **Obstacle Avoidance**: The VL53L1X ToF sensor provides distance data to detect obstacles, adjusting the robot’s path.

- **Parallel Parking**: After three laps, the robot uses ToF and camera data to locate the parking zone and execute a precomputed trajectory (see [parallel_park_setup.jpg](src/parallel_park_setup.jpg)).

#### Navigation Flow Diagram
1. Start → Initialize sensors (Camera, ToF, IMU).
2. Leave the parking zone
3. Loop:
   - Capture camera frame → Detect track and signs using CIELAB.
   - If sign detected:
     - Red → Adjust steering to right based on sign position.
     - Green → Adjust steering to left based on sign position.
   - Read ToF distance → If obstacle or wall < 10cm, adjust path.
   - Update steering and speed via PID control.
4. After 3 laps → Locate parking zone → Execute parking maneuver.

#### Pseudocode for Obstacle Challenge
```
  updating...

WHILE True:
    frame = camera.capture()
    signs = detect_signs(frame, color_space="CIELAB")
    distance = tof.read_distance()
    ...
```

See [Software Documentation](src/README.md) for details on algorithms, libraries, and code structure.

---

## ⚙ Mechanical Characteristics <a id="mechanical-characteristics"></a>
Our robot’s mechanical design prioritizes compactness and durability:
- **Dimensions**: 69mm (L) x 53mm (W) x 57mm (H).
- **Total Weight**: ~130g.
- **Chassis**: 3D-printed ABS chassis.
- **Mechanical Parts**: All mechanical parts were designed in Autodesk Fusion and 3D printed with ABS material using FDM printers.
- **Differential**: Custom 4-gear mechanical differential.
- **Tires**: LEGO 87697 (21mm diameter, 12mm width), selected for the small size, suitability, good performance, and traction, featuring a circumferential center ridge compared to similar alternative parts.
- **Wheel Rotation Limits**: Mechanically limited to -50° to +32° per wheel, an asymmetry derived from Ackermann steering design, ensuring each wheel points toward the same circular center point for smooth turns.
- **Engineering Principles**:
  - **Speed**: The 1500 RPM N20 motor was chosen to achieve a target speed of ~1.4 m/s on the 3m x 3m track. Although the maximum speed is calculated as ~1.72 m/s, the operation speed is reduced to 1.4 m/s via PWM control for stability during high momentum turns.
  - **Torque**: Estimated at ~0.25 Nm for the N20 motor at 6V based on the datasheets, sufficient for the lightweight ~130g robot on a flat track (Force = mass × acceleration, Torque = Force × wheel radius).
- **Assembly Instructions**:
  1. 3D print the chassis using ABS (files in [models/design_base.3mf](models/design_base.3mf)).
  2. Mount the N20 motor to the rear differential using M2 screws.
  3. Attach the Feetech FS0307 servo to the front steering mechanism.
  4. Secure pertinax boards with electronics to the chassis by sliding.
  5. Install LEGO 87697 tires and bearings on all four wheels.

  ![Building Steps](models/building_steps.jpg)

- **CAD Files**: Available at [models/design_base.3mf](models/design_base.3mf) and [models/4_gear_design_mini_differential.3mf](models/4_gear_design_mini_differential.3mf) for replication or modification.

<img src="other/CAD_fusion_right_view.jpg" alt="CAD Fusion Right View" width="600">

Detailed mechanical specifications are in [Models Documentation](models/README.md).

---

## 📹 Performance Videos <a id="performance-videos"></a>
Videos showcasing our robot’s performance in testing and competition scenarios are available in [Performance Videos](video/README.md). Both videos include autonomous robot movements doing key maneuvers, referencing [Hardware](#hardware-documentation), [Software](#software-documentation), and [Mechanical Characteristics](#mechanical-characteristics) in live action.

- **Open Challenge**  
  [![Open Challenge Video](https://img.youtube.com/vi/tvqgwusap9M/0.jpg)](https://youtu.be/tvqgwusap9M)  
  *Demonstrates autonomous navigation and speed control on a dynamic track.*

- **Obstacle Challenge**  
  [![Obstacle Challenge Video](https://img.youtube.com/vi/fQPjyJrE8p8/0.jpg)](https://youtu.be/fQPjyJrE8p8)  
  *Shows traffic sign detection, obstacle avoidance, optimal path planning and parallel parking.*

---

## 📸 Team Photos <a id="team-photos"></a>
Official and informal photos of Team ANTi are available in [Team Photos](t-photos/README.md).

<img src="t-photos/team_official.jpg" alt="Team ANTi Official Photo" width="300">
<img src="t-photos/team_fun.jpg" alt="Team ANTi Fun Photo" width="300">

---

## 🚗 Vehicle Photos <a id="vehicle-photos"></a>
Detailed photos of our robot from all angles (top, bottom, front, back, left, right) are in [Vehicle Photos](v-photos/README.md).

<img src="v-photos/top_view.jpg" alt="ANTi Robot Top View" width="600">

---

## 🛠 Other Resources <a id="other-resources"></a>
Additional resources, including datasheets, communication protocols, and custom pertinax PCB details, are in [Other Resources](other/README.md).

- `ackermann_steering_path.png`: Simulation of our own Ackermann steering design path for a 90-degree turn.  
  <img src="other/ackermann_steering_path.png" alt="Ackermann Steering Path" width="600">

---

## 🌐 GitHub Utilization <a id="github-utilization"></a>
We leveraged GitHub as our central platform for version control, project management, and public sharing, while maintaining a clean and professional repository history:
- **Development Workflow**: We worked on local computers directly connected to our GitHub repository. To keep our repository history clean and avoid overcommitting, we committed changes only at significant milestones (e.g., completing the chassis design, integrating the vision system, finalizing obstacle navigation). Locally, we used sub-folders like `vision` and `steering` to develop features, when committing merging them into our local main branch before pushing polished updates to the public repository.
- **Commit Frequency**: From March to May 2025, we achieved 10 major milestones, resulting in 10 commits to the public repository, averaging ~1 commits per week. Each commit represents a significant, well-documented update, such as "Completed sensor tests" or "Updated README docs".
- **File Sharing and Public Updates**: All project assets—CAD files (`models/`), schematics (`schemes/`), source code (`src/`), and documentation—are shared publicly at each milestone. Before pushing updates, we cleaned up our progress, data, and results to ensure the public repository reflects a safer and smoother development process than our local workflow, making it easier for others to understand and replicate. Additionally, we record the date and time of the last updates in the README documents, providing easy access to the commit date and version.
- **Supporting Others and Future Development**: While we do not want others to simply copy our work for private or closed-source use, we intentionally chose the AGPL-3.0 license to ensure that any future developments based on our code, robot design, hardware system, or overall architecture remain open-source. This strong copyleft license guarantees that improvements or adaptations — whether for competition, education, or research — must also be shared with the community. We are inviting others to replicate, modify, or build upon our work. The modular design of our system and detailed documentation make it easy to adapt the robot for different challenges. Contributions and suggestions — such as adding multi-robot coordination or advanced path-planning — are welcome via GitHub issues.

---

## 📜 License <a id="license"></a>
This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)** to ensure all developments remain publicly accessible, fostering open collaboration and innovation.

```
GNU Affero General Public License v3.0

Copyright (C) 2025 Atakan Ersoy (atakanersoy)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```