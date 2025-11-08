# Other Resources

This folder contains supplementary materials for Team ANTi's WRO 2025 Future Engineers robot, including component images, technical documentation, development photos, and design resources. This documentation was last updated on **Saturday, November 08, 2025, at 08:23 AM +03**.

## Resource Categories

### Electronic Components
| Component | Image | Description |
|-----------|-------|-------------|
| STM32H747 | <img src="STM32H747.jpg" alt="Camera Microcontroller" width="200"> | Dual-core camera microcontroller |
| nRF52832 | <img src="nRF52832.jpg" alt="Sensor Microcontroller" width="200"> | Sensor microcontroller for sensor computations |
| GC2145 Camera | <img src="GC2145.jpg" alt="Camera" width="200"> | 2MP CMOS camera with 80° view angle |
| VL53L1X ToF | <img src="VL53L1X.jpg" alt="ToF Sensor" width="200"> | ToF sensor with 400cm range, full FoV |
| VL53L3CX ToF | <img src="VL53L3CX.jpg" alt="ToF Sensor" width="200"> | ToF sensor with 700cm range, narrow FoV window lens |
| LSM6DSOX IMU | <img src="LSM6DSOX.jpg" alt="IMU" width="200"> | 6-axis accelerometer and gyroscope IMU |
| DRV8833 | <img src="DRV8833.jpg" alt="Motor Driver" width="200"> | PWM motor driver |
| BOB-12009 | <img src="BOB12009.jpg" alt="Logic Level Converter" width="200"> | 3.3V–5V logic level converter |
| SX1308 | <img src="SX1308.jpg" alt="Voltage Booster" width="200"> | 2A DC-DC Step-Up voltage booster |

### Movement & Power Components
| Component | Image | Description |
|-----------|-------|-------------|
| N20 Motor | <img src="1500rpm_N20_dc_motor_encoder.jpg" alt="N20 Motor" width="200"> | 1500 RPM DC motor with Hall effect magnetic encoder |
| FS0307 Servo | <img src="FS0307.jpg" alt="Servo Motor" width="200"> | Feetech submicro servo motor |
| LEGO 87697 | <img src="lego87697_wheel_comparison.jpg" alt="Wheel Comparison" width="200"> | Tire selection comparison showing advantages |
| PX103035 Battery | <img src="PX103035.jpg" alt="Battery" width="200"> | Power-Xtra 1000mAh LiPo battery with PCM |
| LiPo Rider Plus | <img src="LiPo_Rider_Plus.jpg" alt="Charger/Booster" width="200"> | USB-C charger/booster with power switch |
| KLS7-TS1204 | <img src="KLS7-TS1204.jpg" alt="Tactile Switch" width="200"> | Tactile switch for start action |

### Design & Development
| Resource | Image | Description |
|----------|-------|-------------|
| Ackermann Steering | <img src="ackermann_steering_path.png" alt="Ackermann Steering" width="300"> | Simulation of steering path for 90-degree turn |
| Motor Calculations | <img src="motor_speed_calculations.jpg" alt="Motor Calculations" width="300"> | Calculations for motor selection based on requirements |
| ToF Window Lens | <img src="CAD_tof_measure_window.jpg" alt="ToF Measure Window" width="300"> | Dimensions and specifications of the ToF window lens used for narrower FoV |
| Webots Simulation | <img src="ANTi_wro_sim.png" alt="Webots Simulation" width="300"> | Simulation concept (converted to physical implementation) |

### Branding & Achievements
| Resource | Image | Description |
|----------|-------|-------------|
| Team Logo | <img src="transparent_only_logo_WRO2025_FE_ANTi_logo_05-05-2025.png" alt="Team Logo" width="200"> | Official Team ANTi competition logo |
| Champion Trophy | <img src="turkey_champion_trophy.jpg" alt="Champion Trophy" width="200"> | Turkish National Champion achievement |

## Experienced Problems and Implemented Solutions
During the development of the WRO 2025 robot, we encountered several challenges, including:

1. **Integration Issues**: Difficulty in integrating various electronic components due to compatibility issues was resolved by selecting standardized components that are widely supported.

2. **Power Management**: A critical issue was discovered where the 3.3V rail remained active even when the system was off, risking battery drain. This was resolved by performing a hardware modification to the LiPo Rider Plus, rewiring its LDO regulator to the switched 5V rail.

3. **Sensor Calibration**: Initial sensor readings were inconsistent. We implemented a systematic calibration routine to ensure accuracy across all sensors.

4. **Mobility Constraints**: The robot experienced mobility issues on uneven terrain. We redesigned the chassis to improve stability and traction.

## Notes
- All component specifications are sourced from official manufacturer datasheets.
- Development photos showcase our hands-on manufacturing and testing processes.
- Simulation assets demonstrate our comprehensive design validation approach.
- Custom calculations and comparisons guide our engineering decisions.

## Technical Documentation
For detailed documentation, please refer to the following resources:
- **[Schemes Documentation](../schemes/README.md)**: Contains component datasheets, custom pertinax board manufacturing docs, thermal analysis, and power distribution schematics.
- **[Models Documentation](../models/README.md)**: Includes hardware specifications and mechanical design files.
- **[Software Documentation](../src/README.md)**: Features communication protocols (including optimized UART) and software implementation details.

Follow our competition journey: 📸 [Instagram](https://www.instagram.com/anti.wro/) • 🎥 [YouTube](https://www.youtube.com/@solipsy.)