#for learning this skfuzzy you can look at this link https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html and  this https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html . NOW ENJOY THE PROGRAM THANK YOU, PLEASE GIVE STARS IF YOU LIKED IT
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==========================================
# 1. INITIALIZE VARIABLES
# ==========================================
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature') # 0-40°C
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture') # 0-100%
light = ctrl.Antecedent(np.arange(0, 101, 1), 'light')  # 0-100%
water = ctrl.Consequent(np.arange(0, 101, 1), 'water', defuzzify_method='centroid')

# ==========================================
# 2. MEMBERSHIP FUNCTIONS for comparison 
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

# Watering Intensity (Triangular)
water['off'] = fuzz.trimf(water.universe, [0, 0, 20])
water['low'] = fuzz.trimf(water.universe, [10, 30, 50])
water['medium'] = fuzz.trimf(water.universe, [40, 60, 80])
water['high'] = fuzz.trimf(water.universe, [70, 100, 100])

# ==========================================
# 3. RULE BASE (27 Rules)  , logics like if else and then .
# ==========================================
rules = [
    # Cold 
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dark'], water['off']),         
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['dim'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['wet'] & light['bright'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['dark'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['dim'], water['off']),
    ctrl.Rule(temperature['cold'] & moisture['normal'] & light['bright'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['dark'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['dim'], water['low']),
    ctrl.Rule(temperature['cold'] & moisture['dry'] & light['bright'], water['medium']),

    # Normal
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['dark'], water['off']),
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['dim'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['wet'] & light['bright'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dark'], water['low']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['normal'] & light['bright'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['dark'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['dim'], water['medium']),
    ctrl.Rule(temperature['normal'] & moisture['dry'] & light['bright'], water['high']),

    # Hot
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
# 4. CONTROL SYSTEM for motor to run 
# ==========================================
watering_ctrl = ctrl.ControlSystem(rules)
watering_sim = ctrl.ControlSystemSimulation(watering_ctrl)

# ==========================================
# 5. AUTOMATED TESTING  for T,M, L
# ==========================================
test_cases = [
    {"T": 38, "M": 10, "L": 95, "desc": "Max Stress"},
    {"T": 10, "M": 85, "L": 10, "desc": "Rot Danger"},
    {"T": 22, "M": 50, "L": 50, "desc": "Equilibrium"},
    {"T": 35, "M": 80, "L": 90, "desc": "Humid Heat"},
    {"T": 15, "M": 20, "L": 30, "desc": "Cool & Dry"},
    {"T": 40, "M": 30, "L": 100,"desc": "Extreme Heat"},
    {"T": 5,  "M": 15, "L": 80, "desc": "Cold but Dry"},
    {"T": 25, "M": 60, "L": 20, "desc": "Warm Night"},
    {"T": 30, "M": 40, "L": 60, "desc": "Moderate Heat"},
    {"T": 22, "M": 20, "L": 50, "desc": "Comfortable but Dry"}
]

print("\n" + "=" * 80)
print(f"{'No.':<3} | {'T(°C)':<6} | {'M(%)':<5} | {'L(%)':<5} | {'Output':<8} | {'Description'}")
print("=" * 80)

# Gaussian simulation case
for i, case in enumerate(test_cases, 1):
    watering_sim.input['temperature'] = case['T']
    watering_sim.input['moisture'] = case['M']
    watering_sim.input['light'] = case['L']
    
    watering_sim.compute()
    
    output_val = watering_sim.output['water']
    case['gauss_res'] = output_val  # Saving this specific result for the comparison table later
    
    print(f"{i:<3} | {case['T']:<6} | {case['M']:<5} | {case['L']:<5} | {output_val:>6.2f}%   | {case['desc']}")

# ==========================================
# 6. VISUALIZATION  generating for graphs in new windoww 
# ==========================================
print("\nGenerating graphs... Please check the new windows that open.")
print("(for github users , who is using sonal kumar greenhouse fuzzy logic, remeber to check the new window automatically open your pc or mac and save by screnshot or by save button ,otherwise you have to run the program once again to launch the graph)")
temperature.view()
moisture.view()
light.view()
water.view(sim=watering_sim)

# =====================================================================
# 7.: COMPARISON WITH TRIANGULAR FUNCTIONS (ALL 10 CASES) , It si my homework so i took all 10 cases to practice , you can take 5 ,6 as you want.
# =====================================================================
print("\n" + "=" * 90)
print("COMPARATIVE ANALYSIS OF MEMBERSHIP FUNCTIONS (Original Gaussian vs. Triangular)")
print("=" * 90)

# Create fresh, isolated variables just for the Triangular test
t_tri = ctrl.Antecedent(np.arange(0, 41, 1), 't_tri')
m_tri = ctrl.Antecedent(np.arange(0, 101, 1), 'm_tri')
l_tri = ctrl.Antecedent(np.arange(0, 101, 1), 'l_tri')
w_tri = ctrl.Consequent(np.arange(0, 101, 1), 'w_tri', defuzzify_method='centroid')

# Adjusted boundaries to prevent absolute zero drop-offs at the extremes
t_tri['cold'] = fuzz.trimf(t_tri.universe, [0, 0, 20])
t_tri['normal'] = fuzz.trimf(t_tri.universe, [10, 22, 35])
t_tri['hot'] = fuzz.trimf(t_tri.universe, [22, 40, 40])

m_tri['dry'] = fuzz.trimf(m_tri.universe, [0, 0, 50])
m_tri['normal'] = fuzz.trimf(m_tri.universe, [20, 50, 80])
m_tri['wet'] = fuzz.trimf(m_tri.universe, [50, 100, 100])

l_tri['dark'] = fuzz.trimf(l_tri.universe, [0, 0, 50])
l_tri['dim'] = fuzz.trimf(l_tri.universe, [10, 50, 90])
l_tri['bright'] = fuzz.trimf(l_tri.universe, [50, 100, 100])

w_tri['off'] = fuzz.trimf(w_tri.universe, [0, 0, 20])
w_tri['low'] = fuzz.trimf(w_tri.universe, [10, 30, 50])
w_tri['medium'] = fuzz.trimf(w_tri.universe, [40, 60, 80])
w_tri['high'] = fuzz.trimf(w_tri.universe, [70, 100, 100])

rules_tri = [
    ctrl.Rule(t_tri['cold'] & m_tri['wet'] & l_tri['dark'], w_tri['off']),
    ctrl.Rule(t_tri['cold'] & m_tri['wet'] & l_tri['dim'], w_tri['off']),
    ctrl.Rule(t_tri['cold'] & m_tri['wet'] & l_tri['bright'], w_tri['off']),
    ctrl.Rule(t_tri['cold'] & m_tri['normal'] & l_tri['dark'], w_tri['off']),
    ctrl.Rule(t_tri['cold'] & m_tri['normal'] & l_tri['dim'], w_tri['off']),
    ctrl.Rule(t_tri['cold'] & m_tri['normal'] & l_tri['bright'], w_tri['low']),
    ctrl.Rule(t_tri['cold'] & m_tri['dry'] & l_tri['dark'], w_tri['low']),
    ctrl.Rule(t_tri['cold'] & m_tri['dry'] & l_tri['dim'], w_tri['low']),
    ctrl.Rule(t_tri['cold'] & m_tri['dry'] & l_tri['bright'], w_tri['medium']),

    ctrl.Rule(t_tri['normal'] & m_tri['wet'] & l_tri['dark'], w_tri['off']),
    ctrl.Rule(t_tri['normal'] & m_tri['wet'] & l_tri['dim'], w_tri['low']),
    ctrl.Rule(t_tri['normal'] & m_tri['wet'] & l_tri['bright'], w_tri['low']),
    ctrl.Rule(t_tri['normal'] & m_tri['normal'] & l_tri['dark'], w_tri['low']),
    ctrl.Rule(t_tri['normal'] & m_tri['normal'] & l_tri['dim'], w_tri['medium']),
    ctrl.Rule(t_tri['normal'] & m_tri['normal'] & l_tri['bright'], w_tri['medium']),
    ctrl.Rule(t_tri['normal'] & m_tri['dry'] & l_tri['dark'], w_tri['medium']),
    ctrl.Rule(t_tri['normal'] & m_tri['dry'] & l_tri['dim'], w_tri['medium']),
    ctrl.Rule(t_tri['normal'] & m_tri['dry'] & l_tri['bright'], w_tri['high']),

    ctrl.Rule(t_tri['hot'] & m_tri['wet'] & l_tri['dark'], w_tri['low']),
    ctrl.Rule(t_tri['hot'] & m_tri['wet'] & l_tri['dim'], w_tri['low']),
    ctrl.Rule(t_tri['hot'] & m_tri['wet'] & l_tri['bright'], w_tri['medium']),
    ctrl.Rule(t_tri['hot'] & m_tri['normal'] & l_tri['dark'], w_tri['medium']),
    ctrl.Rule(t_tri['hot'] & m_tri['normal'] & l_tri['dim'], w_tri['medium']),
    ctrl.Rule(t_tri['hot'] & m_tri['normal'] & l_tri['bright'], w_tri['high']),
    ctrl.Rule(t_tri['hot'] & m_tri['dry'] & l_tri['dark'], w_tri['high']),
    ctrl.Rule(t_tri['hot'] & m_tri['dry'] & l_tri['dim'], w_tri['high']),
    ctrl.Rule(t_tri['hot'] & m_tri['dry'] & l_tri['bright'], w_tri['high'])
]

watering_ctrl_tri = ctrl.ControlSystem(rules_tri)
watering_sim_tri = ctrl.ControlSystemSimulation(watering_ctrl_tri)

print(f"{'Input Data (T, M, L)':<25} | {'Gaussian (Original)':<20} | {'Triangular (Test)':<20} | {'Difference'}")
print("-" * 90)

# Loop through all 10 test cases for the final table 
for c in test_cases:
    watering_sim_tri.input['t_tri'] = c['T']
    watering_sim_tri.input['m_tri'] = c['M']
    watering_sim_tri.input['l_tri'] = c['L']
    watering_sim_tri.compute()
    
    tri_res = watering_sim_tri.output['w_tri']
    diff = abs(c['gauss_res'] - tri_res)
    
    inputs_str = f"T={c['T']}, M={c['M']}, L={c['L']}"
    print(f"{inputs_str:<25} | {c['gauss_res']:>12.2f}%         | {tri_res:>13.2f}%        | {diff:>6.2f}%")

print("=" * 90)

# Keep the windows open so you can take screenshots
plt.show()
