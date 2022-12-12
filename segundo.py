# Los tipos de apoyo pueden ser viga, muro_sobre_viga, viga_sobre_muro, losa
# Ubicacion es respecto al centro


import json
import numpy as np
import matplotlib.pyplot as plt


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)


def Graficar_tramo(tramo, apoyo_derecho, apoyo_izquierdo):
    blabla = 0
    xx = []
    zz = []

    for i in range(len(tramo)):
        tramox = tramo[blabla][0]
        xx.append(tramox)

        tramoz = tramo[blabla][1]
        zz.append(tramoz)

        blabla = blabla + 1
    plt.plot(xx, zz)

    blabla = 0
    ee = []
    ii = []

    for i in range(len(apoyo_derecho)):
        tramox = apoyo_derecho[blabla][0]
        ee.append(tramox)

        tramoz = apoyo_derecho[blabla][1]
        ii.append(tramoz)

        blabla = blabla + 1
    plt.plot(ee, ii)

    blabla = 0
    jj = []
    kk = []

    for i in range(len(apoyo_izquierdo)):
        tramox = apoyo_izquierdo[blabla][0]
        jj.append(tramox)

        tramoz = apoyo_izquierdo[blabla][1]
        kk.append(tramoz)

        blabla = blabla + 1
    plt.plot(jj, kk)
    plt.show()


keys = list(data["tramos"].keys())

# calular contrahuella
ch = data["generales"]["altura_piso"] / (
    len(data["tramos"][keys[0]]["peldanos"]) + len(data["tramos"][keys[1]]["peldanos"])
)


z_inicial = 0
tramo = [[0, 0]]
apoyo_derecho = []
apoyo_izquierdo = []
z = z_inicial

# el rango es el numero de tramos
for i in range(len(data["tramos"])):

    peldanos = list(data["tramos"][keys[i]]["peldanos"].keys())
    escalera_derecha = True
    long_des = (
        data["tramos"][keys[i]]["descanso"]["vertices"][1][0]
        - data["tramos"][keys[i]]["descanso"]["vertices"][0][0]
    )

    # veo si los escalones van hacia la derecha o izquierda
    if (
        data["tramos"][keys[i]]["peldanos"][peldanos[1]]["vertices"][0][0]
        < data["tramos"][keys[i]]["peldanos"][peldanos[0]]["vertices"][0][0]
    ):
        escalera_derecha = False

    # el rango es el numero de peldanos del tramo
    for n in range(len(data["tramos"][keys[i]]["peldanos"])):
        z = z + ch
        k = data["tramos"][keys[i]]["peldanos"][peldanos[n]]["vertices"]

        # si la escalera sube hacia la derecha
        if escalera_derecha == True:

            xxzz = [[k[0][0], z], [k[1][0], z]]

        # si la escalera sube hacia la izquierda
        else:

            xxzz = [[k[1][0], ch+z], [k[0][0], ch+z]]

        tramo.extend(xxzz)
    print("primeros vertices ", tramo)
    print(tramo[-1][0])
    if escalera_derecha == True:

        des = [
            [tramo[-1][0], tramo[-1][1] + ch],
            [tramo[-1][0] + long_des, tramo[-1][1] + ch],
            [tramo[-1][0] + long_des, tramo[-1][1]],
        ]
        inclinacion = np.arctan((tramo[2][0]) - (tramo[0][0])) / (
            (tramo[2][1]) - (tramo[0][1])
        )
        

        vertices_inferiores = [
            [
                tramo[-1][0]
                + round((data["generales"]["espesor_losa"] / (np.cos(inclinacion))), 2),
                tramo[-1][1],
            ],
            [
                tramo[0][0]
                + round((data["generales"]["espesor_losa"] / (np.cos(inclinacion))), 2),
                tramo[0][1],
            ],
            [tramo[0][0], tramo[0][1]],
        ]


        if data["tramos"][keys[i]]["apoyo_der"]["tipo"] == "muro_sobre_viga":
            apoyo_der1 = [[des[2][0], des[2][1]], [des[2][0], tramo[0][1]]]

            viga_der = [
                [
                    apoyo_der1[0][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1],
                ],
                [
                    apoyo_der1[0][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[0][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
            ]

            apoyo_der2 = [
                [
                    apoyo_der1[0][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1],
                ],
                [
                    apoyo_der1[0][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[-1][1],
                    
                ],
                [des[2][0], des[2][1]],
            ]
            apoyo_derecho.extend(apoyo_der1)
            apoyo_derecho.extend(viga_der)
            apoyo_derecho.extend(apoyo_der2)

        if data["tramos"][keys[i]]["apoyo_der"]["tipo"] == "viga":
            apoyo_der1 = [
                [des[1][0], des[1][1]],
                [
                    des[1][0] + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0],
                    des[1][1],
                ],
                [
                    des[1][0] + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0],
                    des[1][1] - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    des[1][0],
                    des[1][1] - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [des[1][0], des[1][1]],
            ]
            apoyo_derecho.extend(apoyo_der1)

        # if data["tramos"][keys[i]]["apoyo_der"]["tipo"] == "viga_sobre_muro":

        # if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "viga_sobre_muro":

        if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "viga":
            apoyo_izq = [
                [vertices_inferiores[1][0], vertices_inferiores[1][1]],
                [
                    vertices_inferiores[1][0],
                    vertices_inferiores[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    vertices_inferiores[1][0]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    vertices_inferiores[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    vertices_inferiores[1][0]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    vertices_inferiores[1][1],
                ],
                [vertices_inferiores[1][0], vertices_inferiores[1][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq)
        #aun no esta listo :p
        if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "muro_sobre_viga":
            apoyo_izq1 = [
                [tramo[0][0], tramo[0][1]],
                [tramo[0][0], tramo[0][1] - data["generales"]["altura_piso"]],
            ]
            viga_izq = [
                [apoyo_izq1[0][1]
                - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0]
                + data["generales"]["espesor_losa"],tramo[0][1] - data["generales"]["altura_piso"]],
                [apoyo_izq1[0][1]
                - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0]
                + data["generales"]["espesor_losa"],tramo[0][1],]

            
            ]

            apoyo_izq2 = [
                [
                    tramo[0][0] + data["generales"]["espesor_losa"],
                    tramo[0][1] - data["generales"]["altura_piso"],
                ],
                [tramo[0][0] + data["generales"]["espesor_losa"], tramo[0][1]],
                [tramo[0][0], tramo[0][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq1)
            apoyo_izquierdo.extend(viga_izq)
            apoyo_izquierdo.extend(apoyo_izq2)

        
    
    else:

        des = [
            [tramo[-1][0], tramo[-1][1] + ch],
            [tramo[-1][0] - long_des, tramo[-1][1] + ch],
            [tramo[-1][0] - long_des, tramo[-1][1]],
        ]

        inclinacion = np.arctan((tramo[0][0]) - (tramo[2][0])) / (
            (tramo[3][1]) - (tramo[0][1])
        )

        

        vertices_inferiores = [
            [
                tramo[-1][0]
                - round((data["generales"]["espesor_losa"] / (np.cos(inclinacion))), 2),
                tramo[-1][1],
            ],
            [
                tramo[0][0]
                - round((data["generales"]["espesor_losa"] / (np.cos(inclinacion))), 2),
                tramo[0][1],
            ],
            [tramo[0][0],tramo[0][1]]
        ]


        if data["tramos"][keys[i]]["apoyo_der"]["tipo"] == "muro_sobre_viga":
            apoyo_der1 = [[tramo[-1][0] + long_des, tramo[0][1]],
            
            
            ]

            viga_der = [
                [
                    apoyo_der1[0][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1],
                ],
                [
                    apoyo_der1[0][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1] - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[0][0] + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1] - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
            ]

            apoyo_der2 = [
                [
                    apoyo_der1[0][0] + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1],
                ],
                [
                    apoyo_der1[0][0] + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[-1][1],
                ],
            ]
            apoyo_derecho.extend(apoyo_der1)
            apoyo_derecho.extend(viga_der)
            apoyo_derecho.extend(apoyo_der2)

            
        if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "viga":    
            apoyo_izq = [
                [
                    vertices_inferiores[1][0],
                    vertices_inferiores[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    vertices_inferiores[1][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    vertices_inferiores[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    vertices_inferiores[1][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    vertices_inferiores[1][1],
                ],
                [tramo[0][0], tramo[0][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq)


    tramo.extend(des)
    tramo.extend(vertices_inferiores)

    print(tramo)

    Graficar_tramo(tramo, apoyo_derecho, apoyo_izquierdo)

    tramo = [[des[0][0], des[0][1]]]
    apoyo_derecho=[]
    apoyo_izquierdo=[]
    print(tramo)