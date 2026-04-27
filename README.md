# Fuzzy Logic Watering System

A Python-based fuzzy logic system for automatic plant watering based on temperature, soil moisture, and light conditions.

## Overview

This project implements a fuzzy logic control system that determines optimal watering levels for plants by analyzing three environmental inputs:
- **Temperature** (0-40°C): Cold, Normal, or Hot
- **Soil Moisture** (0-100%): Dry, Normal, or Wet
- **Light Level** (0-100%): Dark, Dim, or Bright

The system uses 27 fuzzy logic rules to calculate the optimal watering output (0-100%) and visualizes the membership functions with interactive graphs.

## Features

- 27 fuzzy logic rules covering all temperature × moisture × light combinations
- Gaussian and triangular membership functions
- Centroid defuzzification method
- 10 pre-configured test cases with real-world scenarios
- Interactive visualization of membership functions
- Support for custom input values

## Requirements

- Python 3.x
- numpy
- scikit-fuzzy
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/fuzzy-watering-system.git
cd fuzzy-watering-system
```

2. Install dependencies:
```bash
pip install numpy scikit-fuzzy matplotlib
```

## Usage

Run the script to execute all test cases and display graphs:

```bash
python3 Fuzzy_final.py
```

The script will:
1. Display a table of 10 test cases with calculated watering percentages
2. Generate 4 interactive graphs showing membership functions
3. Wait for you to close the graph windows to complete

## Test Cases

The system includes 10 pre-configured test scenarios:
- Max Stress (Hot, Dry, Bright)
- Rot Danger (Cold, Wet, Dark)
- Equilibrium (Normal, Normal, Normal)
- Humid Heat (Hot, Wet, Bright)
- Cool & Dry (Cold, Dry, Dim)
- Extreme Heat (Hot, Dry, Bright)
- Cold but Dry (Cold, Dry, Bright)
- Warm Night (Warm, Wet, Dark)
- Moderate Heat (Hot, Normal, Normal)
- Comfortable but Dry (Normal, Dry, Normal)

## Project Structure

```
fuzzy-watering-system/
├── Fuzzy_final.py          # Main fuzzy logic system
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## How It Works

The system operates in 4 main stages:

1. Initialization**: Define input variables (temperature, moisture, light) and output (water)
2. embership Functions**: Define fuzzy sets using Gaussian and triangular functions
3. Rule Base**: 27 rules that map input combinations to watering levels
4. Defuzzification**: Calculate crisp watering output using centroid method

## License

This project is open source. Feel free to use and modify as needed.

## Author
-SONAL KUMAR 

Created for fuzzy logic demonstration and automated plant watering system design.
