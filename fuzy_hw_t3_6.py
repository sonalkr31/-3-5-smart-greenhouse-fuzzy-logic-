import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt  # Added to keep graph windows open

# ==========================================
# 1. INITIALIZE VARIABLES (Инициализация)
# ==========================================
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture')
light = ctrl.Antecedent(np.arange(0, 101, 1), 'light')
water = ctrl.Consequent(np.arange(0, 101, 1), 'water', defuzzify_method='centroid')

# ==========================================
# 2. MEMBERSHIP FUNCTIONS (Функции принадлежности)
# ==========================================
# Temperature (Gaussian)
temperature['cold'] = fuzz.gaussmf(temperature.universe, 10, 6)
temperature['normal'] = fuzz.gaussmf(temperature.universe, 22, 5)
temperature['hot'] = fuzz.gaussmf(temperature.universe, 35, 6)

# Soil Moisture (Gaussian)
moisture['dry'] = fuzz.gaussmf(moisture.universe, 20, 15)
moisture['normal'] = fuzz.gaussmf(moisture.universe, 50, 15)
moisture['wet'] = fuzz.gaussmf(moisture.universe, 80, 15)

# Light Level (Gaussian)
light['dark'] = fuzz.gaussmf(light.universe, 10, 20)
light['dim'] = fuzz.gaussmf(light.universe, 50, 20)
light['bright'] = fuzz.gaussmf(light.universe, 90, 20)

# Watering Intensity (Triangular - for easier center-of-mass calculation)
water['off'] = fuzz.trimf(water.universe, [0, 0, 20])
water['low'] = fuzz.trimf(water.universe, [10, 30, 50])
water['medium'] = fuzz.trimf(water.universe, [40, 60, 80])
water['high'] = fuzz.trimf(water.universe, [70, 100, 100])

# ==========================================
# 3. RULE BASE (База правил - 27 Rules)
# ==========================================
rules = [
    # Cold Temperature
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dark'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dim'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['bright'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['dark'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['dim'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['bright'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['dark'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['dim'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['bright'], water['medium']),

    # Normal Temperature
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['dark'], water['off']),
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['dim'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['bright'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dark'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['bright'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['dark'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['bright'], water['high']),

    # Hot Temperature
    ctrl.Rule(temperature['hot'] & moisture['wet'] & light['dark'], water['low']),
    ctrl.Rule(temperature['hot'] & moisture['wet'] & light['dim'], water['low']),
    ctrl.Rule(temperature['hot'] & moisture['wet'] & light['bright'], water['medium']),
    ctrl.Rule(temperature['hot'] & moisture['normal'] & light['dark'], water['medium']),
    ctrl.Rule(temperature['hot'] & moisture['normal'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['hot'] & moisture['normal'] & light['bright'], water['high']),
    ctrl.Rule(temperature['hot'] & moisture['dry'] & light['dark'], water['high']),
    ctrl.Rule(temperature['hot'] & moisture['dry'] & light['dim'], water['high']),
    ctrl.Rule(temperature['hot'] & moisture['dry'] & light['bright'], water['high'])
]

# ==========================================
# 4. CONTROL SYSTEM (Создание системы)
# ==========================================
watering_ctrl = ctrl.ControlSystem(rules)
watering_sim = ctrl.ControlSystemSimulation(watering_ctrl)

# ==========================================
# 5. AUTOMATED TESTING (Автоматическое тестирование)
# ==========================================
test_cases = [
    {"T": 38, "M": 10, "L": 95, "desc": "Max Stress (Максимальный стресс)"},
    {"T": 10, "M": 85, "L": 10, "desc": "Rot Danger (Опасность гниения)"},
    {"T": 22, "M": 50, "L": 50, "desc": "Equilibrium (Точка равновесия)"},
    {"T": 35, "M": 80, "L": 90, "desc": "Humid Heat (Влажная жара)"},
    {"T": 15, "M": 20, "L": 30, "desc": "Cool & Dry (Прохладно и сухо)"},
    {"T": 40, "M": 30, "L": 100,"desc": "Extreme Heat (Крайняя жара)"},
    {"T": 5,  "M": 15, "L": 80, "desc": "Cold but Dry (Морозно, но сухо)"},
    {"T": 25, "M": 60, "L": 20, "desc": "Warm Night (Теплая ночь)"},
    {"T": 30, "M": 40, "L": 60, "desc": "Moderate Heat (Умеренная жара)"},
    {"T": 22, "M": 20, "L": 50, "desc": "Comfortable but Dry (Комфортно, но сухо)"}
]

print("\n" + "=" * 80)
print(f"{'№':<3} | {'T(°C)':<6} | {'M(%)':<5} | {'L(%)':<5} | {'Output':<8} | {'Description'}")
print("=" * 80)

for i, case in enumerate(test_cases, 1):
    watering_sim.input['temperature'] = case['T']
    watering_sim.input['moisture'] = case['M']
    watering_sim.input['light'] = case['L']
    
    watering_sim.compute()
    
    output_val = watering_sim.output['water']
    print(f"{i:<3} | {case['T']:<6} | {case['M']:<5} | {case['L']:<5} | {output_val:>6.2f}%   | {case['desc']}")

print("=" * 80 + "\n")

# ==========================================
# 6. VISUALIZATION FOR REPORT (Генерация графиков для отчета)
# ==========================================
print("Generating graphs... Please check the new windows that open.")
print("(Close the graph windows to finish the script)")

# Show the membership functions (Функции принадлежности)
temperature.view()
moisture.view()
light.view()

# Show the defuzzification graph for the LAST test case (График дефаззификации)
# This visually shows exactly how the system calculated the final percentage
water.view(sim=watering_sim)

# Keep the windows open so you can take screenshots
plt.show()