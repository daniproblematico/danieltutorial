import json
import numpy as np
import matplotlib.pyplot as plt


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)


def Graficar_tramo(tramo):
    blabla = 0
    xx = []
    zz = []

    for i in range(len(tramo)):
        tramox = tramo[blabla][0]
        xx.append(tramox)

        tramoz = tramo[blabla][1]
        zz.append(tramoz)

        blabla = blabla + 1
    # print(xx, zz)
    plt.plot(xx, zz)
    plt.show()



keys = list(data["tramos"].keys())

# calular contrahuella
ch = data["generales"]["altura_piso"] / (
    len(data["tramos"][keys[0]]["peldanos"]) + len(data["tramos"][keys[1]]["peldanos"])
)
print(ch)


z_inicial = 0
tramo = [[0, 0]]
z = z_inicial

# el rango es el numero de tramos
for i in range(len(data["tramos"])):

    peldanos = list(data["tramos"][keys[i]]["peldanos"].keys())
    print(peldanos)
    escalera_derecha = True
    long_des=data['tramos'][keys[i]]['descanso']['vertices'][1][0]-data['tramos'][keys[i]]['descanso']['vertices'][0][0]


    #veo si los escalones van hacia la derecha o izquierda
    if (
        data["tramos"][keys[i]]["peldanos"][peldanos[1]]["vertices"][0][0]
        < data["tramos"][keys[i]]["peldanos"][peldanos[0]]["vertices"][0][0]
    ):
        escalera_derecha = False

    # el rango es el numero de peldanos del tramo
    for n in range(len(data["tramos"][keys[i]]["peldanos"])):
        z = z + ch
        k = data["tramos"][keys[i]]["peldanos"][peldanos[n]]["vertices"]

        
        #si la escalera sube hacia la derecha
        if escalera_derecha == True:

            xxzz = [[k[0][0], z], [k[1][0], z]]


        #si la escalera sube hacia la izquierda
        else:
            xxzz = [[k[1][0], z], [k[0][0], z]]

        tramo.extend(xxzz)

    if escalera_derecha==True:
        des=[
            [tramo[2*(n+1)][0],tramo[2*(n+1)][1]+ch],
            [tramo[2*(n+1)][0]+long_des,tramo[2*(n+1)][1]+ch],
            [tramo[2*(n+1)][0]+long_des,tramo[2*(n+1)][1]]
        ]
        tramo.extend(des)

        apoyo_der1=[
            [tramo[2*(n+1)][0]+long_des,tramo[0][1]]
            ]
        tramo.extend(apoyo_der1)
            
        viga_der=[[apoyo_der1[0][0]+data['tramos'][keys[i]]['apoyo_der']['seccion_viga'][0]-data['tramos'][keys[i]]['apoyo_der']['espesor_muro'],tramo[0][1]],
            [apoyo_der1[0][0]+data['tramos'][keys[i]]['apoyo_der']['seccion_viga'][0]-data['tramos'][keys[i]]['apoyo_der']['espesor_muro'],tramo[0][1]-data['tramos'][keys[i]]['apoyo_der']['seccion_viga'][1]],
            [apoyo_der1[0][0]-data['tramos'][keys[i]]['apoyo_der']['espesor_muro'],tramo[0][1]-data['tramos'][keys[i]]['apoyo_der']['seccion_viga'][1]]


        ]
        tramo.extend(viga_der)
        apoyo_der2=[    
            [apoyo_der1[0][0]-data['tramos'][keys[i]]['apoyo_der']['espesor_muro'],tramo[0][1]],
            [apoyo_der1[0][0]-data['tramos'][keys[i]]['apoyo_der']['espesor_muro'],tramo[2*(n+1)][1]]
        ]
        tramo.extend(apoyo_der2)

        inclinacion = ((tramo[2][0]) - (tramo[0][0])) / (
        (tramo[2][1]) - (tramo[0][1])
        )       




    
    print(tramo)

    Graficar_tramo(tramo)

    tramo=[[des[0][0],des[0][1]]]
