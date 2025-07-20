# W7ZOI Spectrum Analyzer

## KiCad Implementation with modifications by Andy McCann KA3KAF and Doug McCann KA3KAG

## Overview

This repository contains a complete KiCad implementation of the famous W7ZOI Spectrum Analyzer design, originally published in QST magazine. The W7ZOI spectrum analyzer is a well-regarded amateur radio test instrument design that provides a cost-effective solution for RF spectrum analysis.

## Project Description

The W7ZOI Spectrum Analyzer is a superheterodyne spectrum analyzer designed for amateur radio applications. It provides frequency analysis capabilities across the HF and VHF bands, making it an invaluable tool for antenna analysis, filter characterization, and general RF measurements.

### Key Features

- **Frequency Range**: Covers HF through VHF bands
- **Modular Design**: Hierarchical schematic organization for easy understanding and modification
- **Complete Implementation**: Includes all necessary subsystems:
  - VCO and 1st Mixer
  - 110 MHz / 7 MHz Filter sections
  - IF and Log Amplifier
  - 2nd Mixer and 2nd LO
  - Resolution Filters
  - Timebase circuitry
  - 15V Power Supply
  - 2dB Divider
  - 70 MHz Low-pass Filter

## Repository Structure

```text
├── hierarchical-schematic/     # Main hierarchical schematic files
├── 110mhz/                    # 110 MHz filter module
├── 15v-supply/                # Power supply module
├── 2db-div/                   # 2dB divider module
├── 2ndmixer-2ndlo/           # 2nd mixer and LO module
├── 70mhz-lpf/                # 70 MHz low-pass filter
├── 7mhz-crystal-oscillator/  # 7 MHz crystal oscillator
├── if-and-log-amp/           # IF and log amplifier
├── resolution-filters/        # Resolution filter bank
├── timebase/                 # Timebase generation
├── tracking-generator/        # Tracking generator module
├── vco-1stmixer/             # VCO and 1st mixer
├── literature/               # Reference documentation and articles
├── images/                   # Project images and diagrams
└── experimental-data/        # Test data and measurements
```

## Hardware Modules

### Core RF Path

- **VCO and 1st Mixer**: Frequency conversion front-end
- **110 MHz Filter**: First IF filtering
- **7 MHz Crystal Oscillator**: Local oscillator reference
- **2nd Mixer and LO**: Second frequency conversion
- **IF and Log Amplifier**: Signal conditioning and logarithmic response

### Support Circuits

- **15V Power Supply**: Clean, regulated power for all modules
- **Resolution Filters**: Selectable bandwidth filters
- **70 MHz Low-pass Filter**: Anti-aliasing and spurious suppression
- **2dB Divider**: Signal distribution
- **Timebase**: Sweep generation and timing

### Optional Modules

- **Tracking Generator**: Signal source for swept measurements
- **Two-tone Test**: Distortion analysis capability

## Documentation

The `literature/` directory contains extensive reference material including:

- Original QST articles (September 1998, November 1999, June 2001)
- Construction notes and updates
- Filter design references
- Technical papers on spectrum analysis
- Modification and improvement documentation

## Getting Started

### Prerequisites

- KiCad 6.0 or later
- Basic understanding of RF circuit design
- Amateur radio license (for legal operation)

### Opening the Project

1. Clone this repository
2. Open KiCad
3. Load the main project file: `hierarchical-schematic/W7ZOI Spectrum Analyzer.kicad_pro`

### Project Files

- **Schematic**: Hierarchical design with individual module schematics
- **PCB Layout**: Complete board layout for professional fabrication
- **3D Models**: Custom component models for visualization
- **BOM**: Bill of materials with part specifications

## Modifications and Improvements

This implementation includes several improvements over the original design:

- Updated component selections for current availability
- Improved PCB layout with better ground planes
- Enhanced power supply regulation
- Modernized connector choices
- Detailed silkscreen labeling

## Building the Analyzer

Refer to the documentation in the `literature/` directory for detailed construction information. The original QST articles provide comprehensive building instructions, alignment procedures, and performance specifications.

## Contributing

Contributions are welcome! Please feel free to submit issues, improvements, or additional documentation. When contributing:

1. Follow KiCad best practices for schematic and PCB design
2. Document any changes thoroughly
3. Test modifications before submitting
4. Update relevant documentation

## License

This project is based on the original W7ZOI design published in QST magazine. Please respect copyright and amateur radio regulations in your use of these designs.

## Authors and Acknowledgments

- **Original Design**: Wes Hayward (W7ZOI) and Terry White (VE3DTE)
- **KiCad Implementation**: Andy McCann (KA3KAF) and Doug McCann (KA3KAG)
- **Published in**: QST Magazine, September 1998 and subsequent articles

## References

- QST Magazine, September 1998: "A Spectrum Analyzer for the Radio Amateur"
- QST Magazine, November 1999: Part 2 and updates
- QST Magazine, June 2001: Additional modifications and tracking generator
- Various technical papers in the `literature/` directory

---

*This is an amateur radio project intended for educational and experimental use. Please ensure compliance with your local amateur radio regulations.*
