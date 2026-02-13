#Finding difference in impact probabilities for NASA and ESA asteroids
from astropy import QTable
import matplotlib.pyplot as pyplot
import numpy as np

#Reading the files
nasa = QTable.read("NASA_data.csv", format = 'csv')
esa = QTable.read("ESA_data.csv", format = 'csv')


