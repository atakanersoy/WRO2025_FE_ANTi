# Models Documentation

This folder contains the 3D CAD models used for designing and manufacturing Team ANTi’s robot for the WRO 2025 Future Engineers category. This documentation was last updated on **Thursday, May 29, 2025, at 08:03 PM +03**.

## Design Overview
All components of our robot, including the chassis, wheel axles, rims, motor mounts, and differential gears, were designed using **Autodesk Fusion 360**. This professional CAD software allowed us to create precise models optimized for **Fused Filament Fabrication (FFF/FDM)** 3D printing, with some exploration into other techniques like **Stereolithography (SLA)** and **Continuous Fiber Reinforcement (CFR)**.

### Key Design Features
- **Print-in-Place Ackermann Steering**: The steering mechanism uses a shorter linkage connecting the two front wheels, designed to be printed as a single unit for small size and precision.
- **Compact Chassis**: Dimensions of 72mm (L) x 57mm (W) x 58mm (H), with sliders and holders for all components (pertinax board, servo, motor, battery).
- **Differential**: A custom 4-gear mechanical differential distributes power from the motor to the rear wheels.
- **Bearings**: Four bearings, one for each wheel, ensure smooth rotation and reduced friction.

## Materials and Printing Techniques
We tested multiple materials and printing methods to optimize durability and performance:
- **ABS+ (Final Choice)**: Selected for its strength and suitability for print-in-place steering. Printed using FDM technology.
- **Other Materials Tested**:
  - **PLA**: Good for prototyping but lacked durability.
  - **PETG**: Hard to print and less precise for steering components.
  - **ABS**: Similar to ABS+ only lightly less robust than ABS+.
  - **SLA (Rigid10K Resin)**: High precision and stiffness but fragile and expensive.
  - **CFR (Nylon PA12 with Carbon Fiber/Onyx, Glass Fiber)**: Excellent strength and durability but complex to print.
- **Printing Parameters**:
  - Layer Height: 0.08mm–0.1mm (FDM).
  - Infill: 30–40% for structural components, 100% for gears and axles.
  - Nozzle: 0.4mm.
  - Printer: Ender 3v3, Zaxe Z3S.

![3D Printer Setup](3d_printer.jpg)

## File List
- `3d_printer.jpg`: Image of the 3D printer setup.
- `4_gear_design_mini_differential.3mf`: Design file for the 4-gear mini differential.
- `design_ackermann_servo_arm.stl`: STL file for the Ackermann servo arm.
- `design_back_rim_long.3mf`: 3MF file for the long back rim.
- `design_back_rim_short.3mf`: 3MF file for the short back rim.
- `design_base.3mf`: 3MF file for the base design.
- `design_front_rim_bearing.3mf`: 3MF file for the front rim with bearing.
- `design_motor_lid.stl`: STL file for the motor lid.
- `design_spur_25_gear.stl`: STL file for the 25-tooth spur gear.
- `design_spur_26_gear.stl`: STL file for the 26-tooth spur gear.
- `long_design_bevel_12_gear.stl`: STL file for the long 12-tooth bevel gear.
- `short_design_bevel_12_gear.stl`: STL file for the short 12-tooth bevel gear.

## Design Process
1. **Conceptual Design**: Sketched initial ideas focusing on minimal size and Ackermann geometry.
2. **CAD Modeling**: Used Fusion 360 to create precise models, simulating stress and motion for steering and differential.
3. **Prototyping**: Printed multiple iterations, adjusting tolerances for print-in-place components.
4. **Testing**: Validated designs on the WRO track, ensuring stability and maneuverability.

For detailed mechanical specifications, see [Mechanical Characteristics](../README.md#mechanical-characteristics).