#importamos las libreias a usar
import numpy as np
import math
import matplotlib.pyplot as plt
import graphlab




#cargamos la base de datos
url = 'https://github.com/santiquiroz/IA-G5/blob/PruebasRedNeuronal/file.csv'
sf = graphlab.SFrame.read_csv(url)
sf

