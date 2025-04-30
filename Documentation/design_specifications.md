# Design Specifications

## Overview
This document outlines the technical specifications and requirements for the Gearless Robotic Arm project.

## Functional Requirements

### Degrees of Freedom
- **Number of DOF**: 4
  - Base rotation (360°)
  - Shoulder joint (180°)
  - Elbow joint (180°)
  - Wrist rotation (270°)

### Performance Requirements
- **Maximum payload**: 3 kg
- **Reach**: 700 mm fully extended
- **Precision**: ±0.5 mm positioning accuracy
- **Speed**: 90° rotation in 2 seconds (all joints)
- **Duty cycle**: 80% at rated load

### Physical Specifications
- **Weight**: Maximum 2.5 kg (excluding control electronics)
- **Materials**: Primarily aluminum 6061-T6 with strategic reinforcements
- **Mounting**: Standard base mount (100mm × 100mm bolt pattern)
- **Footprint**: 150mm diameter base
- **Dimensions**: Maximum 800mm height when folded

## Technical Specifications

### Power Requirements
- **Input voltage**: 24V DC
- **Maximum current draw**: 3A
- **Average power consumption**: 45W during operation

### Environmental Specifications
- **Operating temperature**: 5°C to 40°C
- **Storage temperature**: -10°C to 50°C
- **Humidity**: Up to 85% non-condensing
- **IP rating**: IP54 (dust and splash resistant)

### Control Interface
- **Communication**: USB and optional WiFi module
- **Control software**: Custom application with Python API
- **User interface**: Manual control pendant and software GUI

## Design Constraints

### Weight Reduction
- Minimum 25% lighter than traditional geared design of similar capability

### Performance Targets
- 30% reduction in mechanical losses compared to geared equivalents
- Noise level below 60dB during operation
- Backlash below 0.1mm at end effector

### Manufacturing Constraints
- Use of standard materials and components where possible
- Minimize custom machined parts
- Design for assembly (DFA) principles applied throughout

## Maintenance Requirements
- Regular maintenance interval: 500 hours of operation
- Major service interval: 2000 hours of operation
- Simple field-replaceable components for common wear items
