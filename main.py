import json


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)


niveles=1
for i in range (niveles):
  l_desc = (data["tramos"]["0"]["descanso"]["vertices"][1][0]) - (
      data["tramos"]["0"]["descanso"]["vertices"][0][0]
  )
  print("Longitud del descanso es= ", l_desc)

  num_tram = len(data["tramos"])
  print("Numero de tramos = ", num_tram)

  if num_tram >= 2:
    num_pel = len(data["tramos"]["0"]["peldanos"]) + len(data["tramos"]["1"]["peldanos"])
    print("Numero de peldanos = ", num_pel)
  else:
    num_pel = len(data["tramos"]["0"]["peldanos"])


  es_lo = data["generales"]["espesor_losa"]
  print("Espesor de losa es = ", es_lo)

  h = data["generales"]["altura_piso"]
  print("Altura de piso es = ", h)

  ch = h / (num_pel)
  print("Contrahuella es = ", ch)

  hh = (data["tramos"]["0"]["peldanos"]["0"]["vertices"][1][0]) - (
      data["tramos"]["0"]["peldanos"]["0"]["vertices"][0][0]
  )
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
          for i in range(num_pel):
              pel = [[round(x, 1), round(z, 1)], [round(x, 1), round(z + ch, 1)]]
              print(pel)
              x = x + hh
              z = z + ch

          if des_pel == False:
              des = [[round(x, 1), round(z, 1)], [round(x + l_desc, 1), round(z, 1)]]
          else:
              des = [
                  [round(x, 1), round(z, 1)],
                  [round(x + l_desc, 1), round(z, 1)],
                  [round(x, 1), round(z + ch, 1)],
                  [round(x + l_desc, 1), round(z + ch, 1)],
              ]
          print("descanso ")
          print(des)

      else:
          if des_pel == False:
              x = x_in + (hh * num_pel)
              z = z_in
          else:
              x = x_in + (hh * num_pel)
              z = z_in + ch

          for i in range(num_pel):
              pel = [[round(x, 1), round(z, 1)], [round(x, 1), round(z + ch, 1)]]
              print(pel)
              x = x - hh
              z = z + ch
      tram = tram + 1
      z_in = z_in + (h / 2)

      print("tramo siguiente = ", tram)
