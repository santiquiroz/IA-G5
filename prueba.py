#importamos las libreias a usar
import numpy as np
import math
import matplotlib.pyplot as plt
import graphlab

#debemos hacer login a github, si no debemos descara


# Si descargamos la base de datos directo
url = 'https://github.com/santiquiroz/IA-G5/blob/PruebasRedNeuronal/file.csv'
training_data = graphlab.SFrame.read_csv(url)
#training_data #mostramos toda la base de datos
training_data, validation_data = data.random_split(0.8) #80% Aprendizaje, 20% Validacion

# Cargamos la base de datos del pc, archivo file "50.000 datos"      
data = graphlab.SFrame.read_csv('file.csv')
data

#tamaño datos
len (data)
training_data, validation_data = data.random_split(0.8) #division datos entrenamiento y validacion 

len(training_data)
len(validation_data)

#RED Neuronal,
#objetivos ????
graphlab.canvas.set_target('ipynb')
training_data['image'].show()

net = graphlab.deeplearning.create(training_data, target ='label')
