import numpy as np
import skfuzzy as fuzz
from skfuzzy import control

def tabela_2():
    pos_car = control.Antecedent(np.arange(-0.4, 0.5, 0.1), 'Car position')
    vel_car = control.Antecedent(np.arange(-1, 1.1, 0.1), 'Car velocite')
    force = control.Consequent(np.arange(-6, 6.2, 0.2), 'force')

    force['Z'] = fuzz.trimf(force.universe, [-1.2, 0, 1.2])
    force['P'] = fuzz.trimf(force.universe, [0, 1.2, 2.4])
    force['PB'] = fuzz.trimf(force.universe, [1.2, 2.4, 3.6])
    force['PVB'] = fuzz.trimf(force.universe, [2.4, 3.6, 4.8])
    force['PVVB'] = fuzz.trapmf(force.universe, [3.6, 4.8, 6, 6])
    force['NVVB'] = fuzz.trapmf(force.universe, [-6, -6, -4.8, -3.6])
    force['NVB'] = fuzz.trimf(force.universe, [-4.8, -3.6, -2.4])
    force['NB'] = fuzz.trimf(force.universe, [-3.6, -2.4, -1.2])
    force['N'] = fuzz.trimf(force.universe, [-2.4, -1.2, 0]) 
    force.view()

    pos_car['Z'] = fuzz.trimf(pos_car.universe, [-0.15, 0, 0.15])
    pos_car['POS'] = fuzz.trimf(pos_car.universe, [0, 0.15, 0.3])
    pos_car['PBIG'] = fuzz.trapmf(pos_car.universe, [0.15, 0.3, 0.4, 0.4])
    pos_car['NBIG'] = fuzz.trapmf(pos_car.universe, [-0.4, -0.4, -0.3, -0.15])
    pos_car['NEG'] = fuzz.trimf(pos_car.universe, [-0.3, -0.15, 0])
    pos_car.view()

    vel_car['ZERO'] = fuzz.trimf(vel_car.universe, [-0.1, 0, 0.1]) 
    vel_car['POS'] = fuzz.trapmf(vel_car.universe, [0, 0.1, 1, 1])
    vel_car['NEG'] = fuzz.trapmf(vel_car.universe, [-1, -1, -0.1, 0])
    vel_car.view()

    controler_2 = control.ControlSystem([
    control.Rule(pos_car['NBIG'] & vel_car['NEG'], force['PVVB']),
    control.Rule(pos_car['NEG'] & vel_car['NEG'], force['PVB']),
    control.Rule(pos_car['Z'] & vel_car['NEG'], force['PB']),
    control.Rule(pos_car['Z'] & vel_car['ZERO'], force['Z']),
    control.Rule(pos_car['Z'] & vel_car['POS'], force['NB']),
    control.Rule(pos_car['POS'] & vel_car['POS'], force['NVB']),
    control.Rule(pos_car['PBIG'] & vel_car['POS'], force['NVVB']),
    ])

    fuzzy_pos_carition = control.ControlSystemSimulation(controler_2)
    fuzzy_pos_carition.input['Car position'] = -0.1
    fuzzy_pos_carition.input['Car velocite'] = 0.08
    fuzzy_pos_carition.compute()

    res = fuzzy_pos_carition.output['force']
    print(f'Force: {res:.2f}', end='\n\n')
    print('Grapichs')
    pos_car.view(sim=fuzzy_pos_carition)
    vel_car.view(sim=fuzzy_pos_carition)

tabela_2()