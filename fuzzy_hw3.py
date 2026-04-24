import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Initialize variables (Инициализация переменных)
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture')
light = ctrl.Antecedent(np.arange(0, 101, 1), 'light')
water = ctrl.Consequent(np.arange(0, 101, 1), 'water', defuzzify_method='centroid')

# 2. Membership functions (Функции принадлежности)
temperature['cold'] = fuzz.gaussmf(temperature.universe, 10, 6)
temperature['normal'] = fuzz.gaussmf(temperature.universe, 22, 5)
temperature['hot'] = fuzz.gaussmf(temperature.universe, 35, 6)

moisture['dry'] = fuzz.gaussmf(moisture.universe, 20, 15)
moisture['normal'] = fuzz.gaussmf(moisture.universe, 50, 15)
moisture['wet'] = fuzz.gaussmf(moisture.universe, 80, 15)

light['dark'] = fuzz.gaussmf(light.universe, 10, 20)
light['dim'] = fuzz.gaussmf(light.universe, 50, 20)
light['bright'] = fuzz.gaussmf(light.universe, 90, 20)

water['off'] = fuzz.trimf(water.universe, [0, 0, 20])
water['low'] = fuzz.trimf(water.universe, [10, 30, 50])
water['medium'] = fuzz.trimf(water.universe, [40, 60, 80])
water['high'] = fuzz.trimf(water.universe, [70, 100, 100])

# 3. Complete Rule Base - 27 Rules to satisfy Task 4 (Полная база правил)
rules = [
    # COLD TEMPERATURE RULES (Правила для холода)
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dark'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dim'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['bright'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['dark'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['dim'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['bright'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['dark'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['dim'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['bright'], water['medium']),

    # NORMAL TEMPERATURE RULES (Правила для нормы)
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['dark'], water['off']),
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['dim'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['bright'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dark'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['bright'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['dark'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['bright'], water['high']),

    # HOT TEMPERATURE RULES (Правила для жары)
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

# 4. Create the control system (Создание системы)
watering_ctrl = ctrl.ControlSystem(rules)
watering_sim = ctrl.ControlSystemSimulation(watering_ctrl)

# 5. Automated Testing for 10 Examples to satisfy Task 7 & 9 (Автоматическое тестирование)
test_cases = [
    {"T": 38, "M": 10, "L": 95, "desc": "Максимальный стресс (Max Stress)"},
    {"T": 10, "M": 85, "L": 10, "desc": "Опасность гниения (Rot Danger)"},
    {"T": 22, "M": 50, "L": 50, "desc": "Точка равновесия (Equilibrium)"},
    {"T": 35, "M": 80, "L": 90, "desc": "Влажная жара (Humid Heat)"},
    {"T": 15, "M": 20, "L": 30, "desc": "Прохладно и сухо (Cool & Dry)"},
    {"T": 40, "M": 30, "L": 100, "desc": "Крайняя жара (Extreme Heat)"},
    {"T": 5,  "M": 15, "L": 80, "desc": "Морозно, но сухо (Cold but Dry)"},
    {"T": 25, "M": 60, "L": 20, "desc": "Теплая ночь (Warm Night)"},
    {"T": 30, "M": 40, "L": 60, "desc": "Умеренная жара (Moderate Heat)"},
    {"T": 22, "M": 20, "L": 50, "desc": "Комфортно, но сухо (Comfortable but Dry)"}
]

print("-" * 60)
print(f"{'№':<3} | {'T(°C)':<6} | {'M(%)':<5} | {'L(%)':<5} | {'Выход (Output)':<15} | {'Описание (Desc)'}")
print("-" * 60)

for i, case in enumerate(test_cases, 1):
    watering_sim.input['temperature'] = case['T']
    watering_sim.input['moisture'] = case['M']
    watering_sim.input['light'] = case['L']
    
    watering_sim.compute()
    
    output_val = watering_sim.output['water']
    print(f"{i:<3} | {case['T']:<6} | {case['M']:<5} | {case['L']:<5} | {output_val:>6.2f}%         | {case['desc']}")

print("-" * 60)