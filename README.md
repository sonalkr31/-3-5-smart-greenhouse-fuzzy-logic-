# Fuzzy Logic Watering System

A Python-based fuzzy logic system for automatic plant watering based on temperature, soil moisture, and light conditions.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-Open%20Source-green.svg)

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

Clone the repository:
   ```bash
   git clone https://github.com/sonalkr31/-3-5-smart-greenhouse-fuzzy-logic-.git
   cd -3-5-smart-greenhouse-fuzzy-logic-
```

## Usage
Install the required dependencies:-
pip install -r requirements.txt

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

1. Initialization**: Define input variables (temperature, moisture, light) and output (water).
2. Membership Functions**: Define fuzzy sets using Gaussian and triangular functions.
3. Rule Base**: 27 rules that map input combinations to watering levels.
4. Defuzzification**: Calculate crisp watering output using the centroid method.


## System Output
!Terminal Output   with  Membership Functions .
<img width="468" height="316" alt="image" src="https://github.com/user-attachments/assets/056d58a5-c491-4dfb-8064-c730b4b05866" />

Mathematical Comparative Analysis:** Automatically compares and calculates the percentage difference between Gaussian and Triangular membership outputs.

## License

This project is open source. Feel free to use and modify as needed.

## Author
-SONAL KUMAR 

Created for fuzzy logic demonstration and automated plant watering system design.
