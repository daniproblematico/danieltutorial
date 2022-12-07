
import json
import numpy as np
import matplotlib.pyplot as plt


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)


keys=data['tramos'].keys()

for i in keys:
    print("tramo ",data["tramos"][i]["peldanos"])
    num_pel = len(data["tramos"][i]["peldanos"]) + len(
    data["tramos"][keys[i+1]]["peldanos"]
    )
    print(num_pel)
