import numpy as np
import skfuzzy as fuzz
from skfuzzy import control


def tabela_3():
    pend_ang = control.Antecedent(np.arange(-30, 30.5, 0.5), 'pendulum angle')
    pend_ang_vel = control.Antecedent(np.arange(-6, 6.1, 0.1), 'pendulum angular velocity')
    force = control.Consequent(np.arange(-6, 6.2, 0.2), 'Force')

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

    pend_ang['Z0'] = fuzz.trimf(pend_ang.universe, [-3, 0, 3])
    pend_ang['P'] = fuzz.trimf(pend_ang.universe, [0, 4.5, 9])
    pend_ang['PB'] = fuzz.trimf(pend_ang.universe, [4.5, 10.5, 16.5])
    pend_ang['PVB'] = fuzz.trapmf(pend_ang.universe, [12, 18, 30, 30])
    pend_ang['NVB'] = fuzz.trapmf(pend_ang.universe, [-30, -30, -18, -12])
    pend_ang['NB'] = fuzz.trimf(pend_ang.universe, [-16.5, -10.5, -4.5])
    pend_ang['N'] = fuzz.trimf(pend_ang.universe, [-9, -4.5, 0])
    pend_ang.view()

    pend_ang_vel['Z0'] = fuzz.trapmf(pend_ang_vel.universe, [-1.7, -0.2, 0.2, 1.7])
    pend_ang_vel['P'] = fuzz.trimf(pend_ang_vel.universe, [0, 1.7, 3.6])
    pend_ang_vel['PB'] = fuzz.trapmf(pend_ang_vel.universe, [1.7, 4.2, 6, 6])
    pend_ang_vel['NB'] = fuzz.trapmf(pend_ang_vel.universe, [-6, -6, -4.2, -1.7])
    pend_ang_vel['N'] = fuzz.trimf(pend_ang_vel.universe, [-3.6, -1.7, 0])
    pend_ang_vel.view()

    controler_3 = control.ControlSystem([
    control.Rule(pend_ang['NVB'] & pend_ang_vel['NB'], force['NVVB']),
    control.Rule(pend_ang['NB'] & pend_ang_vel['NB'], force['NVVB']),
    control.Rule(pend_ang['N'] & pend_ang_vel['NB'], force['NVB']),
    control.Rule(pend_ang['Z0'] & pend_ang_vel['NB'], force['NB']),
    control.Rule(pend_ang['P'] & pend_ang_vel['NB'], force['N']),
    control.Rule(pend_ang['PB'] & pend_ang_vel['NB'], force['Z']),
    control.Rule(pend_ang['PVB'] & pend_ang_vel['NB'], force['P']),
    control.Rule(pend_ang['NVB'] & pend_ang_vel['N'], force['NVVB']),
    control.Rule(pend_ang['NB'] & pend_ang_vel['N'], force['NVB']),
    control.Rule(pend_ang['N'] & pend_ang_vel['N'], force['NB']),
    control.Rule(pend_ang['Z0'] & pend_ang_vel['N'], force['N']),
    control.Rule(pend_ang['P'] & pend_ang_vel['N'], force['Z']),
    control.Rule(pend_ang['PB'] & pend_ang_vel['N'], force['P']),
    control.Rule(pend_ang['PVB'] & pend_ang_vel['N'], force['PB']),
    control.Rule(pend_ang['NVB'] & pend_ang_vel['Z0'], force['NVB']),
    control.Rule(pend_ang['NB'] & pend_ang_vel['Z0'], force['NB']),
    control.Rule(pend_ang['N'] & pend_ang_vel['Z0'], force['N']),
    control.Rule(pend_ang['Z0'] & pend_ang_vel['Z0'], force['Z']),
    control.Rule(pend_ang['P'] & pend_ang_vel['Z0'], force['P']),
    control.Rule(pend_ang['PB'] & pend_ang_vel['Z0'], force['PB']),
    control.Rule(pend_ang['PVB'] & pend_ang_vel['Z0'], force['PVB']),
    control.Rule(pend_ang['NVB'] & pend_ang_vel['P'], force['NB']),
    control.Rule(pend_ang['NB'] & pend_ang_vel['P'], force['N']),
    control.Rule(pend_ang['N'] & pend_ang_vel['P'], force['Z']),
    control.Rule(pend_ang['Z0'] & pend_ang_vel['P'], force['P']),
    control.Rule(pend_ang['P'] & pend_ang_vel['P'], force['PB']),
    control.Rule(pend_ang['PB'] & pend_ang_vel['P'], force['PVB']),
    control.Rule(pend_ang['PVB'] & pend_ang_vel['P'], force['PVVB']),
    control.Rule(pend_ang['NVB'] & pend_ang_vel['PB'], force['N']),
    control.Rule(pend_ang['NB'] & pend_ang_vel['PB'], force['Z']),
    control.Rule(pend_ang['N'] & pend_ang_vel['PB'], force['P']),
    control.Rule(pend_ang['Z0'] & pend_ang_vel['PB'], force['PB']),
    control.Rule(pend_ang['P'] & pend_ang_vel['PB'], force['PVB']),
    control.Rule(pend_ang['PB'] & pend_ang_vel['PB'], force['PVVB']),
    control.Rule(pend_ang['PVB'] & pend_ang_vel['PB'], force['PVVB'])
    ])

    stabilization = control.ControlSystemSimulation(controler_3)

    stabilization.input['pendulum angle'] = -0.1
    stabilization.input['pendulum angular velocity'] = 0.08

    stabilization.compute()

    res = stabilization.output['Force']
    print(f'Force: {res:.2f}', end='\n\n')
    print('Graphics')
    pend_ang.view(sim=stabilization)
    pend_ang_vel.view(sim=stabilization)
    
tabela_3()