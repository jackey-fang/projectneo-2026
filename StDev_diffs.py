#Finding difference in impact probabilities for NASA and ESA asteroids
from astropy import QTable

nasa = QTable.read("NASA_data.csv")
esa = QTable.read("ESA_data.csv")
