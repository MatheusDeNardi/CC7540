import numpy as np
import skfuzzy as fuzz
from skfuzzy import control

def tabela_1():
  ang = control.Antecedent(np.arange(30, 340, 10), 'angle')
  ang_vel = control.Antecedent(np.arange(-10, 10.1, 0.1), 'angular velocity')
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

  ang['Z'] = fuzz.trimf(ang.universe, [180, 180, 180])
  ang['PBS'] = fuzz.trimf(ang.universe, [190, 210, 330])
  ang['PLS'] = fuzz.trimf(ang.universe, [190, 230, 270])
  ang['NLS'] = fuzz.trimf(ang.universe, [90, 130, 170])
  ang['NBS'] = fuzz.trimf(ang.universe, [30, 150, 170])
  ang['SALN'] = fuzz.trimf(ang.universe, [170, 175, 180])
  ang['SALP'] = fuzz.trimf(ang.universe, [180, 185, 190])
  ang.view()

  ang_vel['ZS'] = fuzz.trapmf(ang_vel.universe, [-0.1, -0.001, 0.001, 0.1])
  ang_vel['POS'] = fuzz.trapmf(ang_vel.universe, [0, 1, 10, 10])
  ang_vel['NEG'] = fuzz.trapmf(ang_vel.universe, [-10, -10, -1, 0])
  ang_vel.view()

  controler_1 = control.ControlSystem([
    control.Rule(ang['SALP'] & ang_vel['NEG'], force['P']),
    control.Rule(ang['PBS'] & ang_vel['NEG'], force['Z']),
    control.Rule(ang['PLS'] & ang_vel['NEG'], force['PB']),
    control.Rule(ang['Z'] & ang_vel['ZS'], force['P']),
    control.Rule(ang['NLS'] & ang_vel['POS'], force['NB']),
    control.Rule(ang['NBS'] & ang_vel['POS'], force['Z']),
    control.Rule(ang['SALN'] & ang_vel['POS'], force['N']),
  ])

  swing_up = control.ControlSystemSimulation(controler_1)

  swing_up.input['angle'] = 180
  swing_up.input['angular velocity'] = -0.002

  swing_up.compute()

  res = swing_up.output['force']
  print(f'Force: {res:.2f}', end='\n\n')
  print('Graphics')
  ang.view(sim=swing_up)
  ang_vel.view(sim=swing_up)

tabela_1()