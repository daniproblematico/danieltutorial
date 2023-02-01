
import json
import numpy as np
import matplotlib.pyplot as plt


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)


ziii = np.linspace(0, 2.5, 6)
#print(ziii)

p=data['tramos'].values()


for tramos in data['tramos'].values():
    print(tramos['apoyo_izq']["tipo"])
