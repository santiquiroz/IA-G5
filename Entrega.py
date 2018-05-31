
# coding: utf-8

# In[23]:

#graphlab.get_dependencies()
# DASC
#Kernel > Restart


#importamos las libreias a usar
import numpy as np
import math
import matplotlib.pyplot as plt
import graphlab
# easy_install -U scikit-fuzzy #instalar por consola
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import sys

#puntos de operacion C=0.9951, T=350.4, V=13.89, FlCh=105, FlRx=82


# In[3]:

#cargamos el archivo en la misma carpeta
data = graphlab.SFrame.read_csv('file.csv')

#longitud total
len (data)
data


# In[4]:

#creacion de la tabla de relacion Variables entrada Vs salida Concentracion 
entvsC = graphlab.SFrame({'Concent':data.select_column('Concent'),'FlujoCh':data.select_column('FlujoCh'),
                          'FlujoRx':data.select_column('FlujoRx')})

entvsC


# In[5]:

#creacion de la tabla de relacion Variables entrada Vs salida Volumen 
entvsV = graphlab.SFrame({'Volumen':data.select_column('Volumen'),'FlujoCh':data.select_column('FlujoCh'),
                          'FlujoRx':data.select_column('FlujoRx')})
entvsV


# In[6]:

#creacion de la tabla de relacion Variables entrada Vs salida Temp 
entvsT = graphlab.SFrame({'Tempera':data.select_column('Tempera'),'FlujoCh':data.select_column('FlujoCh'),
                          'FlujoRx':data.select_column('FlujoRx'),'TCalificacion':data.select_column('Concent')})

#Creacion tabla Clasificadora
#Temp = rango, +1
#Temp =fuera rango,-1
entvsT['TCalificacion'] = entvsT['Tempera'].apply(lambda x: +1 if x in range(345,355) else -1)

#
#entvsT['Tempera'] = entvsT['Tempera'].astype(int)
entvsT['Tempera'] = entvsT['Tempera'].astype(str)

entvsT


# In[7]:

#Division en Entrenamento y Validation para cada net
training_dataC, validation_dataC = entvsC.random_split(0.8) #DB concentracion
training_dataT, validation_dataT = entvsT.random_split(0.8) #DB temperatura
training_dataV, validation_dataV = entvsV.random_split(0.8) #DB volumen


# In[8]:

#Comprobacion longitud Entrenamiento 80%
len(training_dataT)
training_dataT


# In[9]:

#Comprobacion longitud Validacion 20%
len(validation_dataT)
validation_dataT


# In[10]:

#Aprendizaje de Flujos de Entrada al Reactor vs Temperatura de Salida
graphlab.canvas.set_target('ipynb')
training_dataT['Tempera'].show()


# In[11]:

netT = graphlab.deeplearning.create(training_dataT, target ='Tempera')
print "layers Red del Flujo del Reactor vs Temperatura"
print "_______________________________________________"
print netT.layers
print "_______________________________________________"
print "Parametros de la Red"
print netT.params


# In[12]:

modelT = graphlab.neuralnet_classifier.create(training_dataT, target = 'Tempera', network = netT, validation_set = validation_dataT, 
                                         metric = ['accuracy','recall@2'])#, max_iterations = 3)


# In[13]:

#Construccion valores de prueba 
test_dataT=[]
test_dataCh=[]
test_dataRx=[]
test_dataCl=[]
from random import randrange
for k in range(1000): 
    test_dataT.append(randrange(345,355))
    test_dataCh.append(randrange(103,108))
    test_dataRx.append(randrange(79,85))
    test_dataCl.append('0')
    

test_data = graphlab.SFrame({'Tempera':test_dataT,
                             'FlujoCh':test_dataCh,
                             'FlujoRx':test_dataRx,
                             'TCalificacion':test_dataCl})

test_data['TCalificacion'] = test_data['Tempera'].apply(lambda x: +1 if x in range(345,355) else -1)

test_data['Tempera'] = test_data['Tempera'].astype(str)
test_data


# In[14]:

#Valores a calificar en la red de entrenamiento objetivo 350, rango(345,355)=1
training_dataT['Tempera'].show


# In[15]:

#Mostramos la frecuencia de recurrencia de cada dato
training_dataT['Tempera'].show(view = 'Categorical')


# In[16]:

#valores validos luego de la clasificacion
training_dataT['TCalificacion'].show(view = 'Categorical')


# In[17]:

#creacion de la tabla de clasificacion
Valores_Clasificados =training_dataT[training_dataT['TCalificacion']== +1]
Valores_Rechazados   =training_dataT[training_dataT['TCalificacion']== -1]
print "Valores_Clasificados: %s" % len(Valores_Clasificados)
print "Valores_Rechazados: %s" % len(Valores_Rechazados)


# In[18]:

#visualizacion de la tabla
Valores_Clasificados


# In[33]:

#ramdom de los valores clasificados
from random import choice
print(choice([Valores_Clasificados]))

# valores aleatoreos de Flujo Ch y Flujo en el reactor, para una temperatura Valida entrada fuzzy
n  =Valores_Clasificados['FlujoCh']
m  =Valores_Clasificados['FlujoRx']
ce =choice(m)
cch=choice(n)
print('-------------------------------')
print('caudal Entrada, caudal chaqueta')
print[ce,cch] #flujo Rx, #flujo Ch


# In[35]:

#llamamos la funcion fuzzy

# Definicion de los dominios a trabajar         
# functions
elements = sys.argv

#caudalE=85
#CaudalCh=105

#de str a numero
cch=float(cch)
ce =float(ce)


caudalE = ctrl.Antecedent(np.arange(0, 160, 1), 'caudalE')
caudalCh = ctrl.Antecedent(np.arange(0, 200, 1), 'caudalCh')
temperatura = ctrl.Consequent(np.arange(0, 700, 1), 'temperatura')
volumen = ctrl.Consequent(np.arange(0, 120, 1), 'volumen')
concentracion = ctrl.Consequent(np.arange(0, 1.5, 1), 'concentracion')

# Definicion de los conjuntos difusos 
caudalE['Bajo']  = fuzz.trapmf(caudalE.universe,[0, 0, 77, 97])
caudalE['Ideal'] = fuzz.gaussmf(caudalE.universe,5 , 82)
caudalE['Alto']  = fuzz.trapmf(caudalE.universe,[67, 87, 160, 160])

caudalCh['Bajo']  = fuzz.trapmf(caudalCh.universe,[0, 0, 100, 120])
caudalCh['Ideal'] = fuzz.gaussmf(caudalCh.universe, 5, 105)
caudalCh['Alto']  = fuzz.trapmf(caudalCh.universe,[90, 110, 200, 200])

temperatura['MuyBajo']    = fuzz.trapmf(temperatura.universe,[0, 0, 60, 120])
temperatura['MedioBajo']  = fuzz.trapmf(temperatura.universe,[30, 90, 190, 250])
temperatura['LigeroBajo'] = fuzz.trapmf(temperatura.universe,[160, 220, 320, 380])
temperatura['Ideal']      = fuzz.trimf(temperatura.universe,[300, 350, 400])
temperatura['LigeroAlto'] = fuzz.trapmf(temperatura.universe,[320, 380, 480, 540])
temperatura['MedioAlto']  = fuzz.trapmf(temperatura.universe,[450, 510, 610, 670])
temperatura['MuyAlto']    = fuzz.trapmf(temperatura.universe,[580, 640, 700, 700])

volumen['Bajo']  = fuzz.trapmf(volumen.universe,[0, 0, 10.89, 20.89])
volumen['Ideal'] = fuzz.trimf(volumen.universe,[10.89, 13.89, 16.89])
volumen['Alto']  = fuzz.trapmf(volumen.universe,[13.89, 16.89, 120, 120])

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

vol.input['caudalE']  = ce #int(caudal1)
vol.input['caudalCh'] = cch #int(caudal2)
vol.compute()

conc.input['caudalE']  = ce #int(caudal1)
conc.input['caudalCh'] = cch #int(caudal2)
conc.compute()


# Crunch the numbers
print(vol.output['volumen'])
volumen.view(sim=tempe)

print(conc.output['concentracion'])
concentracion.view(sim=tempe)
plt.show()


# In[ ]:



