import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt  # Added to keep graph windows open

# ==========================================
# 1. INITIALIZE VARIABLES (Инициализация)
# ==========================================
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature') # 0-40°C , 0 is freezing, 40 is extreme heat
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture') # 0-100% , 0 is completely dry, 100 is fully saturated
light = ctrl.Antecedent(np.arange(0, 101, 1), 'light')  # 0-100% , 0 is complete darkness, 100 is full brightness
water = ctrl.Consequent(np.arange(0, 101, 1), 'water', defuzzify_method='centroid') # 0-100% , 0 is no watering, 100 is maximum watering

# ==========================================
# 2. MEMBERSHIP FUNCTIONS (Функции принадлежности)
# ==========================================
# Temperature (Gaussian)
temperature['cold'] = fuzz.gaussmf(temperature.universe, 10, 6) # Centered at 10°C, spread of 6 (covers roughly 0-20°C)
temperature['normal'] = fuzz.gaussmf(temperature.universe, 22, 5)   # Centered at 22°C, spread of 5 (covers roughly 15-30°C)
temperature['hot'] = fuzz.gaussmf(temperature.universe, 35, 6)  # Centered at 35°C, spread of 6 (covers roughly 25-40°C)

# Soil Moisture (Gaussian)
moisture['dry'] = fuzz.gaussmf(moisture.universe, 20, 15)   # Centered at 20%, spread of 15 (covers roughly 0-50%)
moisture['normal'] = fuzz.gaussmf(moisture.universe, 50, 15)    # Centered at 50%, spread of 15 (covers roughly 30-70%)
moisture['wet'] = fuzz.gaussmf(moisture.universe, 80, 15)   # Centered at 80%, spread of 15 (covers roughly 60-100%)

# Light Level (Gaussian)
light['dark'] = fuzz.gaussmf(light.universe, 10, 20) # Centered at 10%, spread of 20 (covers roughly 0-50%)
light['dim'] = fuzz.gaussmf(light.universe, 50, 20)     # Centered at 50%, spread of 20 (covers roughly 30-70%)
light['bright'] = fuzz.gaussmf(light.universe, 90, 20)          # Centered at 90%, spread of 20 (covers roughly 70-100%)

# Watering Intensity (Triangular - for easier center-of-mass calculation)
water['off'] = fuzz.trimf(water.universe, [0, 0, 20])       # 0-20% watering, with 0 being fully off
water['low'] = fuzz.trimf(water.universe, [10, 30, 50])      # 10-50% watering, with 30% being the peak of "low" watering
water['medium'] = fuzz.trimf(water.universe, [40, 60, 80])    # 40-80% watering, with 60% being the peak of "medium" watering
water['high'] = fuzz.trimf(water.universe, [70, 100, 100])  # 70-100% watering, with 100% being the peak of "high" watering

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


# ==========================================
# 6. VISUALIZATION FOR REPORT (Генерация графиков для отчета)
# ==========================================
print("\n" + "=" * 80)
print("GRAPH DESCRIPTIONS:")
print("=" * 80)
print("\n📊 GRAPH 1: TEMPERATURE Membership Functions")
print("   - Shows how temperature values (0-40°C) are classified")
print("   - 3 categories: COLD (blue), NORMAL (green), HOT (red)")
print("   - X-axis: Temperature in °C | Y-axis: Membership level (0-1)")

print("\n📊 GRAPH 2: SOIL MOISTURE Membership Functions")
print("   - Shows how soil moisture (0-100%) is classified")
print("   - 3 categories: DRY (blue), NORMAL (green), WET (red)")
print("   - X-axis: Moisture in % | Y-axis: Membership level (0-1)")

print("\n📊 GRAPH 3: LIGHT LEVEL Membership Functions")
print("   - Shows how light intensity (0-100%) is classified")
print("   - 3 categories: DARK (blue), DIM (green), BRIGHT (red)")
print("   - X-axis: Light in % | Y-axis: Membership level (0-1)")

print("\n📊 GRAPH 4: WATERING OUTPUT (Defuzzification)")
print("   - Shows the fuzzy logic output calculation")
print("   - Combines all 3 input graphs to determine watering needed")
print("   - Red shaded area = output membership functions")
print("   - Blue line = final defuzzified watering percentage")
print("   - For last test case: T=22°C, M=20%, L=50% → Output=55.25%")

print("\n" + "=" * 80)
print("Generating graphs... Please check the new windows that open.")
print("(Close the graph windows to finish the script)")
print("=" * 80 + "\n")

# Show the membership functions (Функции принадлежности)
temperature.view()
moisture.view()
light.view()

# Show the defuzzification graph for the LAST test case (График дефаззификации)
# This visually shows exactly how the system calculated the final percentage
water.view(sim=watering_sim)

# Keep the windows open so you can take screenshots
plt.show()
print("\n✓ All fuzzy logic tests completed successfully!")