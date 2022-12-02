import json
import numpy as np
import matplotlib.pyplot as plt


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)



#if len(data["tramos"]) >=2:
#  if len(data["tramos"])%2==0:
#    niveles=(len(data["tramos"])/2)
#  else:
#    niveles=((len(data["tramos"])+1)/2)
#else:
#  niveles=1
decimales=1
niveles=1

num_tram = len(data["tramos"])
print("Numero de tramos = ", num_tram)

es_lo = data["generales"]["espesor_losa"]
print("Espesor de losa es = ", es_lo)

h = data["generales"]["altura_piso"]
print("Altura de piso es = ", h)






for i in range (niveles):

  if num_tram >= 2:
    num_pel = len(data["tramos"][str(i)]["peldanos"]) + len(data["tramos"][str(i+1)]["peldanos"])
    num_pel_0 = len(data["tramos"][str(i)]["peldanos"])
    num_pel_1 = len(data["tramos"][str(i+1)]["peldanos"])
  else:
    num_pel = len(data["tramos"]["0"]["peldanos"])
    num_pel_0 = num_pel
    num_pel_1 = 0
  print("Numero de peldanos = ", num_pel)
  print("Numero de peldanos tramo 0 = ",num_pel_0)
  print("Numero de peldanos tramo 1 = ",num_pel_1)

  l_desc = (data["tramos"][str(i)]["descanso"]["vertices"][1][0]) - (
      data["tramos"][str(i)]["descanso"]["vertices"][0][0]
  )
  print("Longitud del descanso es= ", l_desc)

  ch = h / (num_pel)
  print("Contrahuella es = ", ch)

  hh = (data["tramos"][str(i)]["peldanos"]["0"]["vertices"][1][0]) - (
      data["tramos"][str(i)]["peldanos"]["0"]["vertices"][0][0])
  print("Huella es = ", hh)

  # Si hay descanso o no (Asumo que si es una escalera de un solo tramo, no hay descanso)
  descanso = True
  if num_tram == 1:
      descanso = False
  des_pel = True
  if (data["generales"]["descanso_con_peldanos"]) == False:
      des_pel = False
  print("¿Hay peldano en el descanso?", des_pel)

# aqui lo que intentare sera que me cree las coordenadas de cada vertice en una vista frontal de las escaleras en diccionarios
  tram = 0
  x_in = 0
  z_in = 0
  for i in range(num_tram):
      print("tramo actual = ", tram)
      if tram % 2 == 0:
          x = x_in
          z = z_in
          tramo_0=[]
          tramo_1=[]
          for i in range(num_pel_0):
              pel = [[round(x, 1), round(z, 1)], [round(x, 1), round(z + ch, 1)]]
              tramo_0.extend(pel)
              x = x + hh
              z = z + ch
          
          x=x-hh
          if des_pel == False:
              des = [[round(x + l_desc, 1), round(z, 1)],[round(x + l_desc, 1), round(z-ch, 1)]]
              
          else:
              des = [
                  [round(x, 1), round(z+ch, 1)],
                  [round(x + l_desc, 1), round(z+ch, 1)],
                  [round(x+l_desc, 1), round(z, 1)]
              ]
          tramo_0.extend(des)
          

          inclinacion=((tramo_0[2][0])-(tramo_0[0][0]))/((tramo_0[2][1])-(tramo_0[0][1]))
          print("inclinacion ", np.arctan(inclinacion))

          ver_losa_0=[[tramo_0[2*(num_pel_0)-1][0]+round((es_lo/(np.cos(np.arctan(inclinacion)))),2),tramo_0[2*(num_pel_0)-2][1]]]
          tramo_0.extend(ver_losa_0)
          ver_losa_1=[[round(tramo_0[0][0]+(es_lo/(np.cos(np.arctan(inclinacion)))),2),tramo_0[0][1]]]
          tramo_0.extend(ver_losa_1)
          print(tramo_0)
          

          
blabla=0
xx=[]
zz=[]

f#or i,cord in enumerate(tramo_0):
  


for i in range (len(tramo_0)):
   tramox=tramo_0[blabla][0]
   xx.append(tramox)

   tramoz=tramo_0[blabla][1]
   zz.append(tramoz)
   

   
   blabla=blabla+1
print(xx,zz)
plt.plot(xx,zz)
plt.show()

#           plt.scatter(tramo_0)
#           plt.show()

#           #ver_apoyo=ver_losa_1[1][0]-data["generales"][]
          
        

#       else:
#           if des_pel == False:
#               x = x_in + (hh * num_pel)
#               z = z_in
#           else:
#               x = x_in + (hh * num_pel)
#       #         z = z_in + ch
#       #     for i in range(num_pel_1):
#       #         pel = [[round(x, 1), round(z, 1)], [round(x, 1), round(z + ch, 1)]]
#       #         tramo_1.extend(pel)
#       #         #print("tramo1 ", tramo_1)
#       #         x = x - hh
#       #         z = z + ch
#       # tram = tram + 1
#       # z_in = z_in + (h / 2)
#       # #print("tramo siguiente = ", tram)
#       # for tramo in data['tramos'].keys():
# # num_pel = sum([len(tramo['peldanos']) for tramo in data['tramos'].values()])

# # if data["generales"]["descanso_con_peldanos"]:
# #   num_pel += 1