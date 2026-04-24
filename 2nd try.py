import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ШАГ 6.1: Создание осей (универсумов) для переменных
# STEP 6.1: Creating axes (universes) for the variables
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature') # от 0 до 40
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture')      # от 0 до 100
light = ctrl.Antecedent(np.arange(0, 101, 1), 'light')            # от 0 до 100
water = ctrl.Consequent(np.arange(0, 101, 1), 'water', defuzzify_method='centroid')

# ШАГ 6.2: Привязка функций принадлежности (Гауссовы для входов)
# STEP 6.2: Attaching membership functions (Gaussian for inputs)
temperature['cold'] = fuzz.gaussmf(temperature.universe, 10, 6)
temperature['normal'] = fuzz.gaussmf(temperature.universe, 22, 5)
temperature['hot'] = fuzz.gaussmf(temperature.universe, 35, 6)

moisture['dry'] = fuzz.gaussmf(moisture.universe, 20, 15)
moisture['normal'] = fuzz.gaussmf(moisture.universe, 50, 15)
moisture['wet'] = fuzz.gaussmf(moisture.universe, 80, 15)

light['dark'] = fuzz.gaussmf(light.universe, 10, 20)
light['dim'] = fuzz.gaussmf(light.universe, 50, 20)
light['bright'] = fuzz.gaussmf(light.universe, 90, 20)

# Треугольные функции для выхода (для упрощения расчетов центра масс)
# Triangular functions for output (to simplify center of mass calculations)
water['off'] = fuzz.trimf(water.universe, [0, 0, 20])
water['low'] = fuzz.trimf(water.universe, [10, 30, 50])
water['medium'] = fuzz.trimf(water.universe, [40, 60, 80])
water['high'] = fuzz.trimf(water.universe, [70, 100, 100])

# ШАГ 6.3: Создание правил (пример логики)
# STEP 6.3: Creating rules (example of logic)
rule1 = ctrl.Rule(temperature['hot'] & moisture['dry'] & light['bright'], water['high'])
rule2 = ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dark'], water['off'])
rule3 = ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dim'], water['medium'])

# Создание контроллера (системы)
# Creating the controller (system)
watering_ctrl = ctrl.ControlSystem([rule1, rule2, rule3]) # В реальности здесь все 27 правил (In reality, all 27 rules go here)
watering_sim = ctrl.ControlSystemSimulation(watering_ctrl)