#importamos las libreias a usar
import numpy as np
import math
import matplotlib.pyplot as plt
import graphlab




#cargamos la base de datos
url = 'https://github.com/santiquiroz/IA-G5/blob/PruebasRedNeuronal/file.csv'
training_data = graphlab.SFrame.read_csv(url)
training_data, validation_data = data.random_split(0.8) #80% Aprendizaje, 20% Validacion

