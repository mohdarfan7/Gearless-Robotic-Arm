# CAD Models

This directory contains all SolidWorks CAD models and design files for the Gearless Robotic Arm project.

## Directory Structure

- `/Assembly` - Complete assembly files of the robotic arm
- `/Components` - Individual component designs organized by subsystem
- `/Iterations` - Historical design iterations showing the evolution of the design
- `/Exports` - Exported formats (STL, STEP) for sharing and manufacturing
- `/Simulation` - SolidWorks Motion study files for kinematic simulation

## Main Assembly Files

- `GearlessArm_FinalAssembly.SLDASM` - Complete arm assembly with all components
- `GearlessArm_Exploded.SLDASM` - Exploded view for assembly documentation
- `GearlessArm_MotionStudy.SLDMOT` - Motion simulation configuration

## Component Files

### Base System
- `Base_Housing.SLDPRT` - Main structural base housing
- `Base_Mount.SLDPRT` - Mounting plate for securing to surfaces
- `Base_MotorHolder.SLDPRT` - Motor mounting bracket for base rotation

### Arm Segments
- `UpperArm_Structure.SLDPRT` - Main structural component of upper arm
- `ForeArm_Structure.SLDPRT` - Main structural component of forearm
- `Arm_Joint_Connector.SLDPRT` - Joint connection between arm segments

### Joint Mechanisms
- `DirectDrive_JointA.SLDPRT` - Primary joint mechanism (gearless design)
- `DirectDrive_JointB.SLDPRT` - Secondary joint mechanism
- `Bearing_Housing.SLDPRT` - Custom bearing housing for smooth rotation

### End Effector
- `Wrist_Mechanism.SLDPRT` - Wrist rotation and flexibility mechanism
- `Gripper_Assembly.SLDASM` - Gripper assembly for object manipulation
- `Gripper_Fingers.SLDPRT` - Customizable gripper finger design

## Design Specifications

- All dimensions are in millimeters
- Material specifications are defined in the SolidWorks files
- Assembly constraints and mates are fully defined
- Motion studies include torque and speed parameters

## Usage Notes

- SolidWorks 2020 or newer recommended for full compatibility
- Custom materials library included in `/Materials` folder
- Motion study requires SolidWorks Motion module
- For manufacturing, refer to tolerance specifications in the documentation

## Export Formats

- STL files are provided for 3D printing prototypes
- STEP files are included for CAM and manufacturing
- PDF drawings are available in the `/Drawings` folder with dimensions and tolerances

## Design Iterations

The design evolved through several key iterations:
1. Initial concept with traditional joints
2. First gearless prototype with simplified joints
3. Weight-optimized design with material reduction
4. Final design with integrated cable management and optimized stress distribution

## Support Files

- `Assembly_Guide.pdf` - Step-by-step assembly instructions
- `BOM.xlsx` - Complete bill of materials with part numbers
- `Materials_Specification.pdf` - Detailed material properties and selection justification
