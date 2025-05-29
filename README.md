<center><h1>WRO 2025 Future Engineers – ANTi</h1></center>

![Banner](other/transparent_8000x8000_WRO2025_FE_ANTi_logo_05-05-2025.png)

Welcome to the GitHub repository of **Team ANTi**, competing in the **World Robot Olympiad™ (WRO®) Future Engineers 2025** category. Our team, composed of students from Koç University, Türkiye, has designed a compact, innovative, and autonomous self-driving vehicle to tackle the dynamic challenges of the WRO 2025 competition. Our team name, **ANTi**, reflects our philosophy: like an **ANT**, our robot is exceptionally small yet highly capable, pushing the boundaries of minimalism in design. The "**ANT**i" signifies our competitive spirit, standing "versus the world" in pursuit of engineering excellence.

Our mission was to create the smallest possible robot for the WRO 2025 challenge, leveraging our expertise in electrical, mechanical, and software engineering to test the limits of the 3m x 3m game field. Guided by our vision to **"never stop developing unless we stop learning,"** we’ve crafted a vehicle that showcases precision, adaptability, and a milestone in compact robotics design on a global scale. This documentation was last updated on **Thursday, May 29, 2025, at 08:03 PM +03**.

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
- [📜 License](#license)

---

## 📂 Folder Structure <a id="folder-structure"></a>

```
📦 WRO2025_FE_ANTi
├── 📁 models                # 3D CAD models for printing and CNC
├── 📁 schemes               # Schematic diagrams and wiring
├── 📁 src                   # Source code for robot control
├── 📁 t-photos              # Team photos (official and informal)
├── 📁 v-photos              # Vehicle photos from multiple angles
├── 📁 video                 # Performance and testing videos
├── 📁 other                 # Additional resources (datasheets, protocols)
└── 📄 README.md             # Project overview and documentation
```

Detailed documentation for each folder is available in respective `.md` files:
- [Models Documentation](models/README.md)
- [Schemes Documentation](schemes/README.md)
- [Software Documentation](src/README.md)
- [Team Photos](t-photos/README.md)
- [Vehicle Photos](v-photos/README.md)
- [Performance Videos](video/README.md)
- [Other Resources](other/README.md)

---

## 👥 The Team <a id="the-team"></a>

Team ANTi comprises three passionate students from Koç University, Türkiye, guided by an experienced coach. Each member brings unique skills to the project, from electronics to computer vision.

![Team ANTi at Work](t-photos/workplace.jpg)
![Team Fun Moment](t-photos/team_fun.jpg)

### Members
- **Atakan Ersoy** (Team Leader)  
  *Role*: Electronics, Mechanical Design, Software, Strategy Integration  
  *Background*: Freshman, Electrical and Electronics Engineering, Koç University (2025)  
  *Contact*: [atakan@atakanersoy.com](mailto:atakan@atakanersoy.com), [aersoy24@ku.edu.tr](mailto:aersoy24@ku.edu.tr)  
  *Born*: 2006, Türkiye
- **Yusuf Öztürk**  
  *Role*: Mechanical Design, Strategy  
  *Background*: Freshman, Physics, Koç University (2025)  
  *Contact*: [yozturk24@ku.edu.tr](mailto:yozturk24@ku.edu.tr)  
  *Born*: 2006, Türkiye
- **Yusuf Bayram**  
  *Role*: Computer Vision Research  
  *Background*: Freshman, Computer Engineering, Koç University (2025)  
  *Contact*: [ybayram24@ku.edu.tr](mailto:ybayram24@ku.edu.tr)  
  *Born*: 2006, Türkiye

### Coach
- **Ali Aral Eren**  
  *Role*: Team Coach, Connector  
  *Background*: Senior, Electrical and Electronics Engineering, Koç University (2025)  
  *Contact*: [alieren21@ku.edu.tr](mailto:alieren21@ku.edu.tr)  
  *Born*: 2003, Türkiye

### Follow Us
<center>
[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/anti.wro/)  
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@solipsy.)  
</center>

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

![ANTi Robot Front View](v-photos/front_view.jpg)

Team ANTi’s robot is a marvel of minimalism, measuring just **72mm (L) x 57mm (W) x 58mm (H)**, making it one of the smallest vehicles ever designed for the WRO Future Engineers category. Built entirely from scratch, our robot features a **3D-printed chassis** and a **print-in-place Ackermann steering mechanism**, optimized for precision and small size. Powered by a **1500 RPM N20 motor** and controlled by an **STM32H747 dual-core microcontroller**, it leverages advanced sensors like the **GC2145 2MP camera** and **VL53L1X ToF sensor** for robust navigation. Our design philosophy, inspired by the efficiency of an ant, pushes the boundaries of compact robotics while maintaining high performance.

![Design to Life](other/design_to_life.jpg)

* [Vehicle Photos](v-photos/README.md)

---

## 🔧 Hardware Documentation <a id="hardware-documentation"></a>

Our hardware is meticulously selected and integrated using custom **pertinax boards** for minimal size and weight. Key components include:

- **Microcontroller**: STM32H747 (dual-core, high-performance).  
  ![STM32H747](other/STM32H747.jpg)
- **Camera**: GC2145 (2MP CMOS, 80° view angle, <1.0% distortion).  
  ![GC2145 Camera](other/GC2145.jpg)
- **ToF Sensor**: VL53L1X (400cm range, full FoV).  
  ![VL53L1X](other/VL53L1X.jpg)
- **Motor**: 1500 RPM N20 with encoder, selected for its small size and fast speed. Speed was determined by calculating and comparing different wheel/tires sizes and motor speeds for the 3m x 3m game field, using minimum and maximum optimal voltages to set the maximum speed (see [motor_speed_calculations.jpg](other/motor_speed_calculations.jpg)).  
  ![N20 Motor](other/1500rpm_N20_dc_motor_encoder.jpg)
- **Servo**: Feetech FS0307 submicro servo motor, chosen for its minimal size after testing MG90S and SG90 servos.  
  ![FS0307 Servo](other/FS0307.jpg)
- **Battery**: Power-Xtra PX103035 (30x35x10mm, 1000mAh), selected for its minimal size and capacity, lasting far more than the 3-minute round time, with 1000mAh chosen for long trial time. Run time calculated as Run Time = Capacity (mAh) / Total Current (mA), with approximate run time of 4-5 hours and full charge time of ~45 minutes (max 10W at 2A, min 0.8W when fully charged, total current estimated at ~200–250mA).  
  ![Battery](other/PX103035.jpg)
- **Tires**: LEGO 87697, chosen for their small size, suitability, good performance, and traction, with a diameter of 21mm, width of 12mm, and a circumferential center ridge compared to similar parts.

![Soldering Setup](other/soldering_setup.jpg)  
*Our soldering setup for assembling the pertinax boards.*

![Wiring Diagram](schemes/wiring_diagram.jpg)

Detailed hardware specifications and schematics are available in [Schemes Documentation](schemes/README.md).

---

## 💻 Software Documentation <a id="software-documentation"></a>

Our software is written in **MicroPython** and runs on the STM32H747. It uses the **CIELAB color space** for robust computer vision, enabling precise differentiation of track elements and traffic signs. The software integrates sensor data (camera, ToF, IMU) for navigation and control, with algorithms optimized for the dynamic WRO racetrack.

![Image Processing Setup](other/image_processing_setup.jpg)

See [Software Documentation](src/README.md) for details on algorithms, libraries, and code structure.

---

## ⚙ Mechanical Characteristics <a id="mechanical-characteristics"></a>

Our robot’s mechanical design prioritizes compactness and durability:
- **Dimensions**: 72mm (L) x 57mm (W) x 58mm (H).
- **Chassis**: 3D-printed ABS+ with print-in-place Ackermann steering.
- **Differential**: Custom 4-gear mechanical differential.
- **Tires**: LEGO 87697 (21mm diameter, 12mm width), selected for their small size, suitability, good performance, and traction, featuring a circumferential center ridge compared to similar parts.

![CAD Fusion Right View](other/CAD_fusion_right_view.jpg)

Detailed mechanical specifications are in [Models Documentation](models/README.md).

---

## 📹 Performance Videos <a id="performance-videos"></a>

Videos showcasing our robot’s performance in testing and competition scenarios are available in [Performance Videos](video/README.md).

- **Open Challenge**  
  [![Open Challenge Video](https://img.youtube.com/vi/-YdvKO5ceRc/0.jpg)](https://youtu.be/-YdvKO5ceRc)

- **Obstacle Challenge**  
  [![Obstacle Challenge Video](https://img.youtube.com/vi/v3pcT7mglxo/0.jpg)](https://youtu.be/v3pcT7mglxo)

---

## 📸 Team Photos <a id="team-photos"></a>

Official and informal photos of Team ANTi are available in [Team Photos](t-photos/README.md).

![Team ANTi Official Photo](t-photos/team_official.jpg)

---

## 🚗 Vehicle Photos <a id="vehicle-photos"></a>

Detailed photos of our robot from all angles (top, bottom, front, back, left, right) are in [Vehicle Photos](v-photos/README.md).

![ANTi Robot Top View](v-photos/top_view.jpg)

---

## 🛠 Other Resources <a id="other-resources"></a>

Additional resources, including datasheets, communication protocols, and custom PCB details, are in [Other Resources](other/README.md).

---

## 📜 License <a id="license"></a>

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)** to ensure all developments remain publicly accessible, fostering open collaboration and innovation.

```
GNU Affero General Public License v3.0

Copyright (C) 2025 Team ANTi

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