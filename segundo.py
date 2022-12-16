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

    for tr in tramo:
        tramox, tramoz = tr
        xx.append(tramox)
        zz.append(tramoz)

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

#TODO - Esto esta malito
ch = data["generales"]["altura_piso"] / (
    len(data["tramos"][keys[0]]["peldanos"]) + len(data["tramos"][keys[1]]["peldanos"])
)


tramo = [[0, 0]]
apoyo_derecho = []
apoyo_izquierdo = []
z = 0

ziii = np.linspace(0, 2.5, 6)
#print(ziii)

# el rango es el numero de tramos

# for tramo in data['tramos'].values():

for i in range(len(data["tramos"])):

    ch = data["generales"]["altura_piso"] / (
    len(data["tramos"][keys[0]]["peldanos"]) + len(data["tramos"][keys[1]]["peldanos"])
    )

    
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

    # TODO - for innecsario
    # el rango es el numero de peldanos del tramo, aqui genero los vertices de n peldaños
    for n in range(len(data["tramos"][keys[i]]["peldanos"])):
        z = z + ch
        k = data["tramos"][keys[i]]["peldanos"][peldanos[n]]["vertices"]

        # si la escalera sube hacia la derecha
        if escalera_derecha == True:

            xxzz = [[k[0][0], z], [k[1][0], z]]

        # si la escalera sube hacia la izquierda
        else:

            xxzz = [[k[1][0], ch + z], [k[0][0], ch + z]]

        tramo.extend(xxzz)
    #print("primeros vertices ", tramo)
    #print(tramo[-1][0])

    # el orden de dibujado depende de si la escalera va hacia la izquierda o la derecha
    if escalera_derecha == True:

        # genero los vertices del descanso en base a donde acabaron los peldaños
        des = [
            [tramo[-1][0], tramo[-1][1] + ch],
            [tramo[-1][0] + long_des, tramo[-1][1] + ch],
            [
                tramo[-1][0] + long_des,
                tramo[-1][1] + ch - data["generales"]["espesor_losa"],
            ],
        ]

        # calculo la inclunación de la losa para asegurar el ancho de losa
        inclinacion = np.arctan((tramo[2][0]) - (tramo[0][0])) / ch

        # calcula los vertices de la losa
        vertices_inferiores = [
            [
                tramo[-1][0]
                + np.tan(inclinacion) * (ch + data["generales"]["espesor_losa"]),
                des[2][1],
            ],
            [
                tramo[0][0] + data["generales"]["espesor_losa"] / (np.cos(inclinacion)),
                tramo[0][1],
            ],
        ]

        des2 = [
            [
                vertices_inferiores[1][0]
                - (data["generales"]["espesor_losa"] * np.tan(inclinacion)),
                tramo[0][1] - data["generales"]["espesor_losa"],
            ],
            [tramo[0][0] - long_des, tramo[0][1] - data["generales"]["espesor_losa"]],
            [tramo[0][0] - long_des, tramo[0][1]],
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
                [
                    apoyo_der1[0][0]
                    - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    tramo[0][1],
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
                    des[2][1],
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
                [des2[1][0], des2[1][1]],
                [
                    des2[1][0],
                    des2[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    des2[1][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    des2[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    des2[1][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    des2[1][1],
                ],
                [des2[1][0], des2[1][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq)

        if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "muro_sobre_viga":
            apoyo_izq1 = [
                [des2[1][0], des2[1][1]],
                [
                    des2[1][0],
                    des2[1][1] - (len(data["tramos"][keys[i - 1]]["peldanos"]) * ch),
                ],
            ]
            viga_izq = [
                [apoyo_izq1[0][0], apoyo_izq1[1][1]],
                [
                    apoyo_izq1[0][0],
                    apoyo_izq1[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    apoyo_izq1[0][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    apoyo_izq1[1][1]
                    - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    apoyo_izq1[0][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    apoyo_izq1[1][1],
                ],
            ]

            apoyo_izq2 = [
                [
                    apoyo_izq1[0][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["espesor_muro"],
                    apoyo_izq1[1][1],
                ],
                [
                    apoyo_izq1[0][0]
                    + data["tramos"][keys[i]]["apoyo_izq"]["espesor_muro"],
                    apoyo_izq1[0][1],
                ],
            ]
            apoyo_izquierdo.extend(apoyo_izq1)
            apoyo_izquierdo.extend(viga_izq)
            apoyo_izquierdo.extend(apoyo_izq2)

        tramo.extend(des)
        tramo.extend(vertices_inferiores)
        tramo.extend(des2)

    else:

        des = [
            [tramo[-1][0], tramo[-1][1] + ch],
            [tramo[-1][0] - long_des, tramo[-1][1] + ch],
            [
                tramo[-1][0] - long_des,
                tramo[-1][1] + ch - data["generales"]["espesor_losa"],
            ],
        ]

        inclinacion = np.arctan((tramo[0][0]) - (tramo[2][0])) / (ch)

        vertices_inferiores = [
            [
                tramo[-1][0]
                - np.tan(inclinacion) * (ch + data["generales"]["espesor_losa"]),
                des[0][1] - data["generales"]["espesor_losa"],
            ],
            [
                tramo[0][0] - data["generales"]["espesor_losa"] / (np.cos(inclinacion)),
                tramo[0][1],
            ],
        ]

        des2 = [
            [
                vertices_inferiores[1][0]
                + (data["generales"]["espesor_losa"] * np.tan(inclinacion)),
                tramo[0][1] - data["generales"]["espesor_losa"],
            ],
            [tramo[0][0] + long_des, tramo[0][1] - data["generales"]["espesor_losa"]],
            [tramo[0][0] + long_des, tramo[0][1]],
            [tramo[0][0], tramo[0][1]],
        ]
        tramo.extend(des)
        tramo.extend(vertices_inferiores)
        tramo.extend(des2)

        if data["tramos"][keys[i]]["apoyo_der"]["tipo"] == "muro_sobre_viga":
            apoyo_der1 = [
                [des2[1][0], des2[1][1]],
                [
                    des2[1][0] - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    des2[1][1],
                ],
                [
                    des2[1][0] - data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    des2[1][1] - (len(data["tramos"][keys[i - 1]]["peldanos"]) * ch),
                ],
            ]

            viga_der = [
                [apoyo_der1[2][0], apoyo_der1[2][1]],
                [
                    apoyo_der1[2][0],
                    apoyo_der1[2][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1],
                ],
            ]

            apoyo_der2 = [
                [
                    apoyo_der1[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    apoyo_der1[2][1],
                ],
                [
                    apoyo_der1[0][0],
                    apoyo_der1[0][1],
                ],
            ]
            apoyo_derecho.extend(apoyo_der1)
            apoyo_derecho.extend(viga_der)
            apoyo_derecho.extend(apoyo_der2)

        if data["tramos"][keys[i]]["apoyo_der"]["tipo"] == "viga":
            apoyo_der1 = [
                [des2[2][0], des2[2][1]],
                [
                    des2[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0],
                    des2[2][1],
                ],
                [
                    des2[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][0],
                    des2[2][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    des2[2][0],
                    des2[2][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [des2[2][0], des2[2][1]],
            ]
            apoyo_derecho.extend(apoyo_der1)

        if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "muro_sobre_viga":
            apoyo_der1 = [
                [
                    des[2][0] + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    des[2][1],
                ],
                [des[2][0], des[2][1]],
                [
                    des[2][0],
                    des[2][1] - (len(data["tramos"][keys[i - 1]]["peldanos"]) * ch),
                ],
            ]

            viga_der = [
                [apoyo_der1[2][0], apoyo_der1[2][1]],
                [
                    apoyo_der1[2][0],
                    apoyo_der1[2][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1]
                    - data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1],
                ],
            ]

            apoyo_der2 = [
                [
                    apoyo_der1[2][0]
                    + data["tramos"][keys[i]]["apoyo_der"]["espesor_muro"],
                    apoyo_der1[2][1],
                ],
                [
                    apoyo_der1[0][0],
                    apoyo_der1[0][1],
                ],
            ]
            apoyo_izquierdo.extend(apoyo_der1)
            apoyo_izquierdo.extend(viga_der)
            apoyo_izquierdo.extend(apoyo_der2)

        if data["tramos"][keys[i]]["apoyo_izq"]["tipo"] == "viga":
            apoyo_izq = [
                [des[1][0], des[1][1]],
                [
                    des[1][0] - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    des[1][1],
                ],
                [
                    des[1][0] - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][0],
                    des[1][1] - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    des[1][0],
                    des[1][1] - data["tramos"][keys[i]]["apoyo_izq"]["seccion_viga"][1],
                ],
                [des[1][0], des[1][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq)

    #print(tramo)
    p=np.array(tramo)
    print(p[:,0])
    #Graficar_tramo(tramo, apoyo_derecho, apoyo_izquierdo)

    tramo = [[des[0][0], des[0][1]]]
    apoyo_derecho = []
    apoyo_izquierdo = []

    
