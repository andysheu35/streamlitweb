import imp


import pandas as pd

data = pd.read_csv("冰水機sv與塗料溫度.csv")


print(data["Prediction value of prediction target"][10])

data["Prediction value of prediction target"][10]
