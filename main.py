import json

with open('Est_escaleras.json', 'r') as f:
  data = json.load(f)



print(data["tramos"])



es_lo="espesor de losa"
h="altura piso"
num_pel="contar numero de peldanos del diccionario"
ch=(h/num_pel)
hh="contrahuella obtenida de coordenadas del diccionario"

tr=False #Si se ingreso un numero adecuado de tramos
descanso=True #Si hay descanso o no (Asumo que si es una escalera de un solo tramo, no hay descanso)

while tr==False: 
  tramos=input("numero de tramos = ",)
  if tramos=="0":
    print("Debe haber al menos 1 tramo")

  elif tramos=="1":
    descanso=False
    tr=True

  else: tr=True

npel=False  #Si se ingreso un numero adedcuado de peldaños por tramo
while npel==False:
  n_pel=input("¡cuantos peldaos tednra cada tramo?")
  if n_pel=="0":
    print("Debe haber al menos 1 peldaño por tramo")

  elif n_pel=="1":
    npel=True

  else: npel=True


pelda=False #Si se aclaro la existencia o no de un peldaño en el descanso
if descanso==True:
  while pelda==False:
    pel=input("¿Hay peldanos en el descanso?, responda si o no",)
    if pel=="si":
      peldanos=True
      pelda=True
    
    elif pel=="no":
      peldanos=False
      pelda=True
    
    else: print("seleccione una opcion correcta")
  
nt=tramos

tram=0
def c_tram(tram,nt):
  if tram % 2 == 0:
    
  else:
    x_in=0
    y_in=0
    