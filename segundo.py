# Los tipos de apoyo pueden ser viga, muro_sobre_viga, viga_sobre_muro, losa
# Ubicacion es respecto al centro


import json
import numpy as np
import matplotlib.pyplot as plt


with open("Est_escaleras.json", "r") as f:
    data = json.load(f)


def Graficar_tramo(stairs, apoyo_derecho, apoyo_izquierdo):
    blabla = 0
    xx = []
    zz = []

    for tr in stairs:
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


def Calcular_contrahuella(data):
    pl = 0
    for tramos in data["tramos"].values():
        pl = pl + len(tramos["peldanos"])
    ch = data["generales"]["altura_piso"] / pl
    return ch


def Calcular_vertices_tramo_derecho(data, ch, stairs, long_des):
    des = [
        [stairs[-1][0], stairs[-1][1] + ch],
        [stairs[-1][0] + long_des, stairs[-1][1] + ch],
        [
            stairs[-1][0] + long_des,
            stairs[-1][1] + ch - data["generales"]["espesor_losa"],
        ],
    ]

    # calculo la inclunación de la losa para asegurar el ancho de losa
    inclinacion = np.arctan((stairs[2][0]) - (stairs[0][0])) / ch

    # calcula los vertices de la losa
    vertices_inferiores = [
        [
            stairs[-1][0]
            + np.tan(inclinacion) * (ch + data["generales"]["espesor_losa"]),
            des[2][1],
        ],
        [
            stairs[0][0] + data["generales"]["espesor_losa"] / (np.cos(inclinacion)),
            stairs[0][1],
        ],
    ]

    des2 = [
        [
            vertices_inferiores[1][0]
            - (data["generales"]["espesor_losa"] * np.tan(inclinacion)),
            stairs[0][1] - data["generales"]["espesor_losa"],
        ],
        [stairs[0][0] - long_des, stairs[0][1] - data["generales"]["espesor_losa"]],
        [stairs[0][0] - long_des, stairs[0][1]],
        [stairs[0][0], stairs[0][1]],
    ]

    return des, vertices_inferiores, des2

def Apoyo_derecho_murosobreviga(stairs, apoyo_derecho, tramos, des):
    apoyo_der1 = [[des[2][0], des[2][1]], [des[2][0], stairs[0][1]]]

    viga_der = [
                [
                    apoyo_der1[0][0]
                    + tramos["apoyo_der"]["seccion_viga"][0]
                    - tramos["apoyo_der"]["espesor_muro"],
                    stairs[0][1],
                ],
                [
                    apoyo_der1[0][0]
                    + tramos["apoyo_der"]["seccion_viga"][0]
                    - tramos["apoyo_der"]["espesor_muro"],
                    stairs[0][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[0][0] - tramos["apoyo_der"]["espesor_muro"],
                    stairs[0][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[0][0] - tramos["apoyo_der"]["espesor_muro"],
                    stairs[0][1],
                ],
            ]

    apoyo_der2 = [
                [
                    apoyo_der1[0][0] - tramos["apoyo_der"]["espesor_muro"],
                    stairs[0][1],
                ],
                [
                    apoyo_der1[0][0] - tramos["apoyo_der"]["espesor_muro"],
                    des[2][1],
                ],
                [des[2][0], des[2][1]],
            ]
    apoyo_derecho.extend(apoyo_der1)
    apoyo_derecho.extend(viga_der)
    apoyo_derecho.extend(apoyo_der2)


ch = Calcular_contrahuella(data)

stairs = [[0, 0]]
apoyo_derecho = []
apoyo_izquierdo = []
z = 0


for tramos in data["tramos"].values():

    peldanos = list(tramos["peldanos"].keys())
    escalera_derecha = True
    long_des = (
        tramos["descanso"]["vertices"][1][0] - tramos["descanso"]["vertices"][0][0]
    )

    # veo si los escalones van hacia la derecha o izquierda
    if (
        tramos["peldanos"][peldanos[1]]["vertices"][0][0]
        < tramos["peldanos"][peldanos[0]]["vertices"][0][0]
    ):
        escalera_derecha = False

    # TODO - for innecsario
    # el rango es el numero de peldanos del tramo, aqui genero los vertices de n peldaños
    for peldanos in tramos["peldanos"].values():
        z = z + ch
        k = peldanos["vertices"]

        # si la escalera sube hacia la derecha
        if escalera_derecha == True:

            vertices_peldanos = [[k[0][0], z], [k[1][0], z]]

        # si la escalera sube hacia la izquierda
        else:

            vertices_peldanos = [[k[1][0], ch + z], [k[0][0], ch + z]]

        stairs.extend(vertices_peldanos)

    # el orden de dibujado depende de si la escalera va hacia la izquierda o la derecha
    if escalera_derecha == True:

        # genero los vertices del descanso en base a donde acabaron los peldaños
        des, vertices_inferiores, des2 = Calcular_vertices_tramo_derecho(
            data, ch, stairs, long_des
        )

        if tramos["apoyo_der"]["tipo"] == "muro_sobre_viga":
            Apoyo_derecho_murosobreviga(stairs, apoyo_derecho, tramos, des)

        if tramos["apoyo_der"]["tipo"] == "viga":
            apoyo_der1 = [
                [des[1][0], des[1][1]],
                [
                    des[1][0] + tramos["apoyo_der"]["seccion_viga"][0],
                    des[1][1],
                ],
                [
                    des[1][0] + tramos["apoyo_der"]["seccion_viga"][0],
                    des[1][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    des[1][0],
                    des[1][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [des[1][0], des[1][1]],
            ]
            apoyo_derecho.extend(apoyo_der1)

        if tramos["apoyo_izq"]["tipo"] == "viga":
            apoyo_izq = [
                [des2[1][0], des2[1][1]],
                [
                    des2[1][0],
                    des2[1][1] - tramos["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    des2[1][0] + tramos["apoyo_izq"]["seccion_viga"][0],
                    des2[1][1] - tramos["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    des2[1][0] + tramos["apoyo_izq"]["seccion_viga"][0],
                    des2[1][1],
                ],
                [des2[1][0], des2[1][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq)

        if tramos["apoyo_izq"]["tipo"] == "muro_sobre_viga":
            apoyo_izq1 = [
                [des2[1][0], des2[1][1]],
                [
                    des2[1][0],
                    des2[1][1] - (len(tramos["peldanos"]) * ch),
                ],
            ]
            viga_izq = [
                [apoyo_izq1[0][0], apoyo_izq1[1][1]],
                [
                    apoyo_izq1[0][0],
                    apoyo_izq1[1][1] - tramos["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    apoyo_izq1[0][0] + tramos["apoyo_izq"]["seccion_viga"][0],
                    apoyo_izq1[1][1] - tramos["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    apoyo_izq1[0][0] + tramos["apoyo_izq"]["seccion_viga"][0],
                    apoyo_izq1[1][1],
                ],
            ]

            apoyo_izq2 = [
                [
                    apoyo_izq1[0][0] + tramos["apoyo_izq"]["espesor_muro"],
                    apoyo_izq1[1][1],
                ],
                [
                    apoyo_izq1[0][0] + tramos["apoyo_izq"]["espesor_muro"],
                    apoyo_izq1[0][1],
                ],
            ]
            apoyo_izquierdo.extend(apoyo_izq1)
            apoyo_izquierdo.extend(viga_izq)
            apoyo_izquierdo.extend(apoyo_izq2)

        stairs.extend(des)
        stairs.extend(vertices_inferiores)
        stairs.extend(des2)

    else:

        des = [
            [stairs[-1][0], stairs[-1][1] + ch],
            [stairs[-1][0] - long_des, stairs[-1][1] + ch],
            [
                stairs[-1][0] - long_des,
                stairs[-1][1] + ch - data["generales"]["espesor_losa"],
            ],
        ]

        inclinacion = np.arctan((stairs[0][0]) - (stairs[2][0])) / (ch)

        vertices_inferiores = [
            [
                stairs[-1][0]
                - np.tan(inclinacion) * (ch + data["generales"]["espesor_losa"]),
                des[0][1] - data["generales"]["espesor_losa"],
            ],
            [
                stairs[0][0]
                - data["generales"]["espesor_losa"] / (np.cos(inclinacion)),
                stairs[0][1],
            ],
        ]

        des2 = [
            [
                vertices_inferiores[1][0]
                + (data["generales"]["espesor_losa"] * np.tan(inclinacion)),
                stairs[0][1] - data["generales"]["espesor_losa"],
            ],
            [stairs[0][0] + long_des, stairs[0][1] - data["generales"]["espesor_losa"]],
            [stairs[0][0] + long_des, stairs[0][1]],
            [stairs[0][0], stairs[0][1]],
        ]
        stairs.extend(des)
        stairs.extend(vertices_inferiores)
        stairs.extend(des2)

        if tramos["apoyo_der"]["tipo"] == "muro_sobre_viga":
            apoyo_der1 = [
                [des2[1][0], des2[1][1]],
                [
                    des2[1][0] - tramos["apoyo_der"]["espesor_muro"],
                    des2[1][1],
                ],
                [
                    des2[1][0] - tramos["apoyo_der"]["espesor_muro"],
                    des2[1][1] - (len(tramos["peldanos"]) * ch),
                ],
            ]

            viga_der = [
                [apoyo_der1[2][0], apoyo_der1[2][1]],
                [
                    apoyo_der1[2][0],
                    apoyo_der1[2][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0] + tramos["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0] + tramos["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1],
                ],
            ]

            apoyo_der2 = [
                [
                    apoyo_der1[2][0] + tramos["apoyo_der"]["espesor_muro"],
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

        if tramos["apoyo_der"]["tipo"] == "viga":
            apoyo_der1 = [
                [des2[2][0], des2[2][1]],
                [
                    des2[2][0] + tramos["apoyo_der"]["seccion_viga"][0],
                    des2[2][1],
                ],
                [
                    des2[2][0] + tramos["apoyo_der"]["seccion_viga"][0],
                    des2[2][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    des2[2][0],
                    des2[2][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [des2[2][0], des2[2][1]],
            ]
            apoyo_derecho.extend(apoyo_der1)

        if tramos["apoyo_izq"]["tipo"] == "muro_sobre_viga":
            apoyo_der1 = [
                [
                    des[2][0] + tramos["apoyo_der"]["espesor_muro"],
                    des[2][1],
                ],
                [des[2][0], des[2][1]],
                [
                    des[2][0],
                    des[2][1] - (len(tramos["peldanos"]) * ch),
                ],
            ]

            viga_der = [
                [apoyo_der1[2][0], apoyo_der1[2][1]],
                [
                    apoyo_der1[2][0],
                    apoyo_der1[2][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0] + tramos["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1] - tramos["apoyo_der"]["seccion_viga"][1],
                ],
                [
                    apoyo_der1[2][0] + tramos["apoyo_der"]["seccion_viga"][1],
                    apoyo_der1[2][1],
                ],
            ]

            apoyo_der2 = [
                [
                    apoyo_der1[2][0] + tramos["apoyo_der"]["espesor_muro"],
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

        if tramos["apoyo_izq"]["tipo"] == "viga":
            apoyo_izq = [
                [des[1][0], des[1][1]],
                [
                    des[1][0] - tramos["apoyo_izq"]["seccion_viga"][0],
                    des[1][1],
                ],
                [
                    des[1][0] - tramos["apoyo_izq"]["seccion_viga"][0],
                    des[1][1] - tramos["apoyo_izq"]["seccion_viga"][1],
                ],
                [
                    des[1][0],
                    des[1][1] - tramos["apoyo_izq"]["seccion_viga"][1],
                ],
                [des[1][0], des[1][1]],
            ]
            apoyo_izquierdo.extend(apoyo_izq)

    Graficar_tramo(stairs, apoyo_derecho, apoyo_izquierdo)

    stairs = [[des[0][0], des[0][1]]]
    apoyo_derecho = []
    apoyo_izquierdo = []

    p = np.array(stairs)
    print("jlshfdj", p[:, 0])
