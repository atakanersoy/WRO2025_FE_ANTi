# Schemes Documentation

This folder contains the electrical schematics and wiring details for Team ANTi’s WRO 2025 Future Engineers robot. This documentation was last updated on **Thursday, May 29, 2025, at 08:03 PM +03**.

## Overview
Our robot’s electronics are integrated on custom **pertinax boards** (perforated PCBs), meticulously cut to minimize size. All connections and soldering were performed by the team to ensure reliability and compactness. The system operates on three power lines:
- **+3V1**: Powers the STM32H747 microcontroller.
- **+2V8A**: Powers the GC2145 camera and VL53L1X ToF sensor.
- **+1V8**: Powers the microcontroller, camera, USB transceiver, and LSM6DSOX IMU.

## Components
- **Microcontroller**: STM32H747 (dual-core, high-performance).
- **Camera**: GC2145 (2MP CMOS, 2.2mm focal length, 80° view angle, <1.0% distortion).
- **ToF Sensor**: VL53L1X (400cm range, full FoV).
- **IMU**: LSM6DSOX (6-axis accelerometer and gyroscope).
- **Servo**: Feetech FS0307 submicro servo.
- **Motor Driver**: DRV8833 (PWM motor driver).
- **Motor**: 1500 RPM N20 with quadrature encoder (2 Hall-effect sensors).
- **Battery**: Power-Xtra PX103035 3.7V 1000mAh LiPo with PCM.
- **Charger/Booster**: LiPo Rider Plus (Seeed Studio, USB-C charging, power switch).
- **Voltage Booster**: SX1308 2A DC-DC Step-Up.
- **Logic Level Converter**: BOB-12009 (3.3V–5V level shifter).
- **Button**: KLS7-TS1204 tactile switch (start action).

## Schematics
![Wiring Diagram](wiring_diagram.jpg)

![Both Uncut Pertinax Boards](both_uncut_pertinax_scheme.jpg)

### Power Distribution
- **Battery Management**: The LiPo Rider Plus manages charging (via USB-C) and provides a power switch. The SX1308 boosts voltage to stable levels for components.
- **Power Lines**:
  - +3V1: Microcontroller core and peripherals.
  - +2V8A: Camera and ToF sensor for consistent imaging and ranging.
  - +1V8: Low-power components like the IMU and USB transceiver.
- **Battery Performance**:
  - Capacity: 1000mAh.
  - Run Time: ~4–5 hours (calculated based on component current draw).
  - Charge Time: ~45 minutes (max 10W at 2A, 0.8W when fully charged).
  - Formula: Run time = Capacity (mAh) / Total Current (mA). Total current estimated at ~200–250mA based on component specs.

### Wiring
- All connections are soldered on pertinax boards, cut to fit the 72mm x 57mm chassis.
- The tactile switch initiates robot operation, interfaced with the STM32H747.
- Micro USB is used for programming, separate from the USB-C charging port.

## Design Considerations
- **Compactness**: Pertinax boards were chosen over traditional PCBs to reduce size and weight.
- **Reliability**: Hand-soldered connections ensure robust electrical performance.
- **Power Efficiency**: The 1000mAh battery was selected for extended trial time, exceeding the 3-minute competition round.

## Datasheet List
- `BOB-12009.pdf`: Logic level converter specifications.
- `drv8833.pdf`: Motor driver specifications.
- `FS0307-specs.pdf`: Servo motor specifications.
- `GC2145.pdf`: Camera sensor details.
- `kls7-ts1204.pdf`: Tactile switch specifications.
- `LiPoRiderPlus_ETA9740_V1.1.pdf`: Charger/booster ETA specifications.
- `LiPoRiderPlus_SCH.pdf`: Charger/booster schematic.
- `lsm6dsox.pdf`: IMU specifications.
- `N20_motors.pdf`: N20 motor and encoder details.
- `stm32h747.pdf`: Microcontroller specifications.
- `SX1308.pdf`: Voltage booster specifications.
- `vl53l1x.pdf`: ToF sensor specifications.
- `wiring_diagram.jpg`: Wiring diagram image.

For component datasheets, see [Other Resources](../other/README.md).