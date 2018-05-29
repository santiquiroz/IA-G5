import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import sys

# Definicion de los dominios a trabajar         
# functions
elements = sys.argv
caudalE = ctrl.Antecedent(np.arange(0, 160, 1), 'caudalE')
caudalCh = ctrl.Antecedent(np.arange(0, 200, 1), 'caudalCh')
temperatura = ctrl.Consequent(np.arange(0, 700, 1), 'temperatura')
volumen = ctrl.Consequent(np.arange(0, 120, 1), 'volumen')
concentracion = ctrl.Consequent(np.arange(0, 1.5, 1), 'concentracion')

# Definicion de los conjuntos difusos 
caudalE['Bajo'] = fuzz.trapmf(caudalE.universe,[0, 0, 77, 97])
caudalE['Ideal'] = fuzz.gaussmf(caudalE.universe,5 , 82)
caudalE['Alto'] = fuzz.trapmf(caudalE.universe,[67, 87, 160, 160])

caudalCh['Bajo'] = fuzz.trapmf(caudalCh.universe,[0, 0, 100, 120])
caudalCh['Ideal'] = fuzz.gaussmf(caudalCh.universe, 5, 105)
caudalCh['Alto'] = fuzz.trapmf(caudalCh.universe,[90, 110, 200, 200])

temperatura['MuyBajo'] = fuzz.trapmf(temperatura.universe,[0, 0, 60, 120])
temperatura['MedioBajo'] = fuzz.trapmf(temperatura.universe,[30, 90, 190, 250])
temperatura['LigeroBajo'] = fuzz.trapmf(temperatura.universe,[160, 220, 320, 380])
temperatura['Ideal'] = fuzz.trimf(temperatura.universe,[300, 350, 400])
temperatura['LigeroAlto'] = fuzz.trapmf(temperatura.universe,[320, 380, 480, 540])
temperatura['MedioAlto'] = fuzz.trapmf(temperatura.universe,[450, 510, 610, 670])
temperatura['MuyAlto'] = fuzz.trapmf(temperatura.universe,[580, 640, 700, 700])

volumen['Bajo'] = fuzz.trapmf(volumen.universe,[0, 0, 10.89, 20.89])
volumen['Ideal'] = fuzz.trimf(volumen.universe,[10.89, 13.89, 16.89])
volumen['Alto'] = fuzz.trapmf(volumen.universe,[13.89, 16.89, 120, 120])

concentracion['Ideal'] = fuzz.smf(concentracion.universe,0.92, 0.9951)



#Reglas Temperatura
rule1 = ctrl.Rule(caudalCh['Bajo'] & caudalE['Bajo'], temperatura['MuyBajo'])
rule2 = ctrl.Rule(caudalCh['Ideal'] & caudalE['Bajo'] | caudalCh['Bajo'] & caudalE['Ideal'], temperatura['MedioBajo'])
rule3 = ctrl.Rule(caudalCh['Alto'] & caudalE['Bajo'], temperatura['LigeroBajo'])
rule4 = ctrl.Rule(caudalCh['Ideal'] & caudalE['Ideal'], temperatura['Ideal'])
rule5 = ctrl.Rule(caudalCh['Bajo'] & caudalE['Alto'], temperatura['LigeroAlto'])
rule6 = ctrl.Rule(caudalCh['Alto'] & caudalE['Ideal'] | caudalCh['Ideal'] & caudalE['Alto'], temperatura['MedioAlto'])
rule7 = ctrl.Rule(caudalCh['Alto'] & caudalE['Alto'], temperatura['MuyAlto'])
#Reglas Volumen
rule8 = ctrl.Rule(caudalCh['Bajo'] & caudalE['Bajo'], volumen['Bajo'])
rule9 = ctrl.Rule(caudalCh['Bajo'] & caudalE['Ideal'] | caudalCh['Ideal'] & caudalE['Bajo'] , volumen['Ideal'])
rule10 = ctrl.Rule(caudalCh['Alto'] & caudalE['Bajo'] | caudalCh['Alto'] & caudalE['Ideal'] 
| caudalCh['Alto'] & caudalE['Alto'] | caudalCh['Ideal'] & caudalE['Ideal'] 
| caudalCh['Ideal'] & caudalE['Alto'] | caudalCh['Bajo'] & caudalE['Alto'] , volumen['Alto'])
#Reglas Concentracion 

rule12 = ctrl.Rule(caudalCh['Ideal'] & caudalE['Ideal'] | caudalCh['Ideal'] & caudalE['Alto'] 
|caudalCh['Alto'] & caudalE['Ideal'] | caudalCh['Alto'] & caudalE['Alto'], concentracion['Ideal'])
#controlador Temperatura
tempe_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
tempe = ctrl.ControlSystemSimulation(tempe_ctrl)

#Controlador Volumen
vol_ctrl = ctrl.ControlSystem([rule8, rule9, rule10])
vol = ctrl.ControlSystemSimulation(vol_ctrl)

#Controlador Concentracion
conc_ctrl = ctrl.ControlSystem(rule12)
conc = ctrl.ControlSystemSimulation(conc_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)

caudal1 = elements[1]
caudal2 = elements[2]

vol.input['caudalE'] = int(caudal1)
vol.input['caudalCh'] = int(caudal2)

vol.compute()

# Crunch the numbers
print(vol.output['volumen'])
volumen.view(sim=tempe)