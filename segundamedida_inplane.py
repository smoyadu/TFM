# -*- coding: utf-8 -*-
"""SegundaMedida_Inplane.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BL3z8J0sRGA4XEtF7-YDS74GptyVmrYv
"""

import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from scipy.interpolate import interp1d

# Función para calcular FWHM (Full Width Half Maximum)
def calcular_fwhm(posicion, dosis):
    max_dosis = max(dosis)
    half_max_dosis = max_dosis / 2

    # Interpolar los datos para encontrar el FWHM con mayor precisión
    interp_func = interp1d(posicion, dosis)

    # Encontrar posiciones a la mitad de la dosis máxima
    posiciones_half_max = np.where(dosis >= half_max_dosis)[0]

    if len(posiciones_half_max) > 1:
        fwhm = abs(posicion[posiciones_half_max[-1]] - posicion[posiciones_half_max[0]])
        return fwhm
    else:
        return None

# Función corregida para calcular la simetría y planitud
def calcular_simetria_planitud(posicion, dosis):
    # Simetría: Compara la dosis a ambos lados del eje central (posicion 0)
    indice_central = np.argmin(np.abs(posicion))  # Encuentra el índice más cercano a 0 (eje central)
    dosis_central = dosis[indice_central]

    izquierda = dosis[:indice_central]
    derecha = dosis[indice_central+1:][::-1]  # Invertir la parte derecha para comparar con la izquierda

    # Asegurarnos de que las dos partes tengan la misma longitud
    if len(izquierda) > len(derecha):
        izquierda = izquierda[:len(derecha)]
    elif len(derecha) > len(izquierda):
        derecha = derecha[:len(izquierda)]

    simetria = np.mean(np.abs(izquierda - derecha) / dosis_central) * 100  # Error relativo porcentual

    # Planitud: Variación dentro del área entre el 80% y 100% de la dosis máxima
    max_dosis = max(dosis)
    limite_inferior = 0.8 * max_dosis

    # Filtrar la región de interés (dosis >= 80% de la dosis máxima)
    indices_region = np.where(dosis >= limite_inferior)[0]

    if len(indices_region) > 0:
        dosis_region = dosis[indices_region]
        max_region = max(dosis_region)
        min_region = min(dosis_region)
        planitud = (max_region - min_region) / (max_region + min_region) * 100
    else:
        planitud = None

    return simetria, planitud

""" Data = cm, cGy """

p4datos = """

-3.8002,0
-3.7643,0
-3.7285,0
-3.6927,0
-3.6568,0
-3.621,0
-3.5852,0
-3.5493,0
-3.5135,32.0211
-3.4777,33.9019
-3.4418,36.9291
-3.406,39.2274
-3.3702,40.8574
-3.3343,42.308
-3.2985,43.7974
-3.2627,44.3568
-3.2268,44.5339
-3.191,44.6903
-3.1552,44.7027
-3.1193,44.7027
-3.0835,44.6697
-3.0477,44.468
-3.0118,44.3445
-2.976,43.9866
-2.9401,43.5509
-2.9043,43.3168
-2.8685,43.1484
-2.8326,43.0007
-2.7968,42.7751
-2.761,42.7382
-2.7251,42.689
-2.6893,42.5825
-2.6535,42.5825
-2.6176,42.4309
-2.5818,42.3735
-2.546,42.1319
-2.5101,41.9887
-2.4743,41.8824
-2.4385,41.6861
-2.4026,41.6493
-2.3668,41.4164
-2.331,41.2735
-2.2951,41.0531
-2.2593,40.7881
-2.2235,40.3564
-2.1876,40.2465
-2.1518,40.1408
-2.116,39.9416
-2.0801,39.7994
-2.0443,39.7872
-2.0085,39.6695
-1.9726,39.5721
-1.9368,39.5275
-1.901,39.3896
-1.8651,39.3733
-1.8293,39.3288
-1.7935,39.2193
-1.7576,39.1788
-1.7218,39.1626
-1.686,39.114
-1.6501,39.0047
-1.6143,38.9358
-1.5785,38.948
-1.5426,38.9116
-1.5068,38.8994
-1.471,38.8104
-1.4351,38.7093
-1.3993,38.6567
-1.3635,38.4385
-1.3276,38.4345
-1.2918,38.4345
-1.256,38.4385
-1.2201,38.4628
-1.1843,38.4628
-1.1485,38.2528
-1.1126,38.2205
-1.0768,38.2205
-1.0409,38.3174
-1.0051,38.4506
-0.96928,38.487
-0.93345,38.5072
-0.89761,38.4951
-0.86178,38.4506
-0.82595,38.4224
-0.79011,38.2246
-0.75428,38.1479
-0.71844,38.0955
-0.68261,38.0874
-0.64678,38.039
-0.61094,38.039
-0.57511,38.031
-0.53927,37.9503
-0.50344,37.9705
-0.46761,37.9584
-0.43177,37.9624
-0.39594,38.1842
-0.3601,38.3093
-0.32427,38.4466
-0.28844,38.5557
-0.2526,38.6527
-0.21677,38.681
-0.18093,38.6203
-0.1451,38.4547
-0.10927,38.3255
-0.073433,38.3255
-0.037599,38.3255
-0.0017647,38.4547
0.034069,38.5355
0.069903,38.4951
0.10574,38.5355
0.14157,38.7659
0.17741,38.8428
0.21324,38.8549
0.24907,38.9075
0.28491,38.9966
0.32074,39.0735
0.35657,39.0532
0.39241,38.9561
0.42824,38.8104
0.46408,38.5112
0.49991,38.4143
0.53574,38.269
0.57158,38.0189
0.60741,37.8134
0.64325,37.7087
0.67908,37.6885
0.71491,37.757
0.75075,37.8134
0.78658,37.9544
0.82242,38.1721
0.85825,38.2205
0.89408,38.2205
0.92992,38.1237
0.96575,37.8698
1.0016,37.8698
1.0374,37.8899
1.0733,37.9181
1.1091,38.1318
1.1449,38.378
1.1808,38.4668
1.2166,38.5557
1.2524,38.5557
1.2883,38.6608
1.3241,38.7497
1.3599,38.6769
1.3958,38.5961
1.4316,38.5718
1.4674,38.5961
1.5033,38.483
1.5391,38.487
1.5749,38.487
1.6108,38.5395
1.6466,38.483
1.6824,38.4668
1.7183,38.2609
1.7541,38.2125
1.7899,38.0955
1.8258,38.0834
1.8616,38.0592
1.8974,38.0552
1.9333,37.9262
1.9691,37.9262
2.0049,37.9262
2.0408,37.9342
2.0766,38.0914
2.1124,38.1197
2.1483,38.1923
2.1841,38.1883
2.2199,38.0269
2.2558,37.9745
2.2916,37.757
2.3274,37.5879
2.3633,36.9372
2.3991,36.5245
2.4349,36.1846
2.4708,36.1206
2.5066,36.1047
2.5424,35.925
2.5783,36.0967
2.6141,36.0009
2.6499,35.921
2.6858,35.8851
2.7216,35.8851
2.7574,35.8532
2.7933,35.8054
2.8291,35.7535
2.865,35.6021
2.9008,35.5464
2.9366,35.4747
2.9725,35.3792
3.0083,35.3077
3.0441,35.1964
3.08,35.0812
3.1158,34.7717
3.1516,34.637
3.1875,34.4786
3.2233,34.2888
3.2591,34.0952
3.295,33.7325
3.3308,32.7862
3.3666,32.3446
3.4025,30.7889
3.4383,30.0277
3.4741,27.1109
3.51,15.2262
3.5458,0
3.5816,0
3.6175,0
3.6533,0
3.6891,0
3.725,0
3.7608,0
3.7966,0
3.8325,0
3.8683,0
3.9041,0
3.94,0
3.9758,0
4.0116,0
4.0475,0
4.0833,0
4.1191,0
4.155,0
4.1908,0


"""

p3datos = """

-4.1576,0
-4.1217,0
-4.0859,0
-4.0501,0
-4.0142,0
-3.9784,0
-3.9426,0
-3.9067,0
-3.8709,0
-3.8351,0
-3.7992,0
-3.7634,0
-3.7276,0
-3.6917,0
-3.6559,0
-3.6201,144.4768
-3.5842,178.5357
-3.5484,207.1757
-3.5126,233.3765
-3.4767,269.2367
-3.4409,293.3153
-3.4051,312.9917
-3.3692,328.6853
-3.3334,338.7164
-3.2976,343.4329
-3.2617,347.3446
-3.2259,350.923
-3.1901,353.6892
-3.1542,358.1098
-3.1184,361.5027
-3.0826,364.2785
-3.0467,366.7896
-3.0109,370.5815
-2.9751,371.4683
-2.9392,376.2673
-2.9034,377.5191
-2.8676,379.4173
-2.8317,381.0154
-2.7959,383.4353
-2.7601,384.0032
-2.7242,385.3049
-2.6884,389.0668
-2.6526,389.8866
-2.6167,391.2803
-2.5809,393.1638
-2.5451,391.5261
-2.5092,391.5261
-2.4734,391.5261
-2.4376,391.5261
-2.4017,390.5425
-2.3659,392.591
-2.3301,394.3079
-2.2942,395.0419
-2.2584,395.2863
-2.2225,395.2863
-2.1867,394.8789
-2.1509,395.2863
-2.115,396.0186
-2.0792,396.3435
-2.0434,396.3435
-2.0075,401.4052
-1.9717,402.5904
-1.9359,402.4329
-1.9,399.4912
-1.8642,396.9923
-1.8284,395.856
-1.7925,395.5306
-1.7567,393.7361
-1.7209,393.2456
-1.685,392.1816
-1.6492,390.9524
-1.6134,390.2145
-1.5775,390.0506
-1.5417,389.0668
-1.5059,388.4932
-1.47,388.6571
-1.4342,389.0668
-1.3984,389.0668
-1.3625,393.4909
-1.3267,392.9184
-1.2909,392.1816
-1.255,391.0344
-1.2192,391.1163
-1.1834,389.7226
-1.1475,391.1163
-1.1117,391.1163
-1.0759,388.4932
-1.04,385.0605
-1.0042,385.5495
-0.96836,385.0605
-0.93253,384.6535
-0.89669,381.7388
-0.86086,382.061
-0.82502,380.5346
-0.78919,381.2563
-0.75336,381.5778
-0.71752,383.1923
-0.68169,381.6583
-0.64585,383.6786
-0.61002,385.9574
-0.57419,385.0605
-0.53835,385.9574
-0.50252,388.1655
-0.46669,388.4113
-0.43085,388.4113
-0.39502,389.5587
-0.35918,389.8866
-0.32335,388.821
-0.28752,387.5105
-0.25168,385.2234
-0.21585,385.2234
-0.18001,385.7942
-0.14418,384.7348
-0.10835,385.7942
-0.072512,385.8758
-0.036678,385.8758
-0.00084375,384.979
0.03499,385.4679
0.070824,385.4679
0.10666,385.5495
0.14249,385.5495
0.17833,386.8561
0.21416,385.8758
0.24999,384.4095
0.28583,382.4645
0.32166,380.0549
0.3575,379.9751
0.39333,380.0549
0.42916,383.0304
0.465,384.0844
0.50083,386.6926
0.53667,387.6742
0.5725,387.0196
0.60833,388.0017
0.64417,389.3947
0.68,388.2474
0.71584,386.6926
0.75167,385.8758
0.7875,382.4645
0.82334,381.7388
0.85917,381.0154
0.89501,381.417
0.93084,381.0957
0.96667,380.5346
1.0025,379.9751
1.0383,379.4173
1.0742,378.2282
1.11,378.2282
1.1458,379.6561
1.1817,378.2282
1.2175,377.6764
1.2533,377.1267
1.2892,375.9562
1.325,375.801
1.3608,373.9541
1.3967,372.816
1.4325,374.0305
1.4683,374.0305
1.5042,374.0305
1.54,376.5792
1.5759,376.5792
1.6117,374.1833
1.6475,375.9562
1.6834,375.9562
1.7192,374.1833
1.755,375.9562
1.7909,376.8135
1.8267,376.5792
1.8625,376.0339
1.8984,376.1117
1.9342,376.5792
1.97,378.7028
2.0059,381.4974
2.0417,384.4095
2.0775,386.1207
2.1134,386.2023
2.1492,387.5924
2.185,388.0017
2.2209,388.0017
2.2567,387.5924
2.2925,388.0836
2.3284,385.9574
2.3642,385.7942
2.4,383.5975
2.4359,383.5164
2.4717,380.855
2.5075,382.061
2.5434,382.061
2.5792,381.6583
2.615,381.6583
2.6509,381.6583
2.6867,380.6947
2.7225,379.8953
2.7584,379.3377
2.7942,377.6764
2.83,376.7354
2.8659,376.5792
2.9017,373.8016
2.9375,373.6493
2.9734,371.6915
3.0092,370.3613
3.045,369.4869
3.0809,368.7663
3.1167,367.4884
3.1525,364.4114
3.1884,362.6226
3.2242,359.4088
3.26,357.2051
3.2959,355.9194
3.3317,353.0568
3.3675,346.4324
3.4034,328.583
3.4392,308.8163
3.475,274.6099
3.5109,219.9417
3.5467,146.0703
3.5826,0
3.6184,0
3.6542,0
3.6901,0
3.7259,0
3.7617,0
3.7976,0
3.8334,0
3.8692,0



"""

p2datos = """


-4.0098,0
-3.974,0
-3.9381,0
-3.9023,0
-3.8664,0
-3.8306,0
-3.7948,0
-3.7589,0
-3.7231,0
-3.6873,0
-3.6514,0
-3.6156,0
-3.5798,0
-3.5439,276.4827
-3.5081,326.4176
-3.4723,386.1207
-3.4364,444.9883
-3.4006,512.9256
-3.3648,567.5983
-3.3289,598.7788
-3.2931,656.3622
-3.2573,667.0481
-3.2214,673.2195
-3.1856,677.7739
-3.1498,682.4185
-3.1139,684.243
-3.0781,688.7296
-3.0423,689.3947
-3.0064,690.2901
-2.9706,696.5604
-2.9348,701.1626
-2.8989,705.622
-2.8631,711.9054
-2.8273,722.195
-2.7914,726.8542
-2.7556,730.6874
-2.7198,732.1112
-2.6839,733.5298
-2.6481,735.414
-2.6123,735.1789
-2.5764,737.0571
-2.5406,741.0316
-2.5048,741.0316
-2.4689,743.1304
-2.4331,748.7283
-2.3973,752.0063
-2.3614,754.8309
-2.3256,758.6274
-2.2898,759.8225
-2.2539,763.1956
-2.2181,763.1956
-2.1823,763.681
-2.1464,763.681
-2.1106,763.681
-2.0748,763.681
-2.0389,766.3683
-2.0031,764.6547
-1.9672,765.6324
-1.9314,765.6324
-1.8956,765.3876
-1.8597,762.9533
-1.8239,763.1956
-1.7881,762.4692
-1.7522,762.4692
-1.7164,760.5419
-1.6806,759.1049
-1.6447,759.1049
-1.6089,756.9615
-1.5731,756.0131
-1.5372,754.8309
-1.5014,754.8309
-1.4656,753.8875
-1.4297,752.2411
-1.3939,751.3026
-1.3581,751.3026
-1.3222,752.2411
-1.2864,756.9615
-1.2506,757.9124
-1.2147,757.9124
-1.1789,757.9124
-1.1431,758.866
-1.1072,760.0621
-1.0714,760.7821
-1.0356,761.2631
-0.99973,767.8476
-0.9639,767.3534
-0.92806,766.8603
-0.89223,766.8603
-0.8564,766.8603
-0.82056,765.6324
-0.78473,767.1067
-0.74889,766.8603
-0.71306,764.8987
-0.67723,765.6324
-0.64139,765.3876
-0.60556,763.9241
-0.56973,763.9241
-0.53389,771.5924
-0.49806,769.0883
-0.46222,769.0883
-0.42639,769.8362
-0.39056,769.3373
-0.35472,763.1956
-0.31889,762.9533
-0.28305,762.9533
-0.24722,760.7821
-0.21139,760.7821
-0.17555,766.3683
-0.13972,767.6004
-0.10388,770.8378
-0.06805,771.8446
-0.032216,771.8446
0.0036181,771.3406
0.039452,771.3406
0.075286,770.3364
0.11112,770.3364
0.14695,768.5911
0.18279,765.143
0.21862,762.4692
0.25446,763.9241
0.29029,766.3683
0.32612,770.3364
0.36196,771.5924
0.39779,773.6193
0.43363,777.001
0.46946,777.001
0.50529,778.6189
0.54113,777.001
0.57696,776.2051
0.6128,776.2051
0.64863,784.2213
0.68446,784.5083
0.7203,782.2287
0.75613,784.5083
0.79197,785.0838
0.8278,785.0838
0.86363,785.0838
0.89947,785.0838
0.9353,778.8917
0.97113,771.089
1.007,771.089
1.0428,771.089
1.0786,771.089
1.1145,768.343
1.1503,767.1067
1.1861,765.8774
1.222,761.0225
1.2578,761.0225
1.2936,773.6193
1.3295,773.6193
1.3653,773.6193
1.4011,777.2683
1.437,778.6189
1.4728,773.6193
1.5086,772.0971
1.5445,771.8446
1.5803,761.9861
1.6161,765.8774
1.652,769.0883
1.6878,764.6547
1.7236,764.6547
1.7595,764.6547
1.7953,764.6547
1.8311,762.2276
1.867,762.7111
1.9028,768.343
1.9387,768.5911
1.9745,770.0861
2.0103,770.3364
2.0462,770.0861
2.082,767.1067
2.1178,765.8774
2.1537,765.143
2.1895,765.143
2.2253,763.9241
2.2612,770.0861
2.297,770.0861
2.3328,768.5911
2.3687,765.8774
2.4045,765.8774
2.4403,760.5419
2.4762,760.3019
2.512,760.5419
2.5478,761.2631
2.5837,756.487
2.6195,756.0131
2.6553,754.5949
2.6912,754.359
2.727,754.359
2.7628,757.9124
2.7987,757.9124
2.8345,752.476
2.8703,747.5607
2.9062,745.4615
2.942,744.529
2.9778,743.8297
3.0137,744.529
3.0495,744.529
3.0853,744.2959
3.1212,744.2959
3.157,743.5967
3.1928,734.2373
3.2287,729.0188
3.2645,717.9521
3.3003,712.41
3.3362,654.9192
3.372,570.6803
3.4078,470.1072
3.4437,357.5278
3.4795,139.1318
3.5153,0
3.5512,0
3.587,0
3.6228,0
3.6587,0
3.6945,0
3.7303,0
3.7662,0
3.802,0
3.8379,0
3.8737,0
3.9095,0
3.9454,0
3.9812,0



"""

p1datos = """


-4.0559,0
-4.0201,0
-3.9842,0
-3.9484,0
-3.9126,0
-3.8767,0
-3.8409,0
-3.8051,0
-3.7692,0
-3.7334,0
-3.6976,0
-3.6617,0
-3.6259,0
-3.5901,34.6053
-3.5542,271.0185
-3.5184,331.8178
-3.4826,410.0546
-3.4467,472.381
-3.4109,558.7999
-3.3751,619.7771
-3.3392,696.5604
-3.3034,741.0316
-3.2676,756.487
-3.2317,774.3852
-3.1959,783.3637
-3.1601,796.2401
-3.1242,802.9471
-3.0884,807.7326
-3.0526,811.7591
-3.0167,813.3048
-2.9809,814.0619
-2.9451,814.0619
-2.9092,814.0619
-2.8734,817.2083
-2.8376,819.2448
-2.8017,819.2448
-2.7659,819.2448
-2.7301,818.3551
-2.6942,818.5799
-2.6584,818.3551
-2.6225,814.8079
-2.5867,820.7391
-2.5509,823.3036
-2.515,825.623
-2.4792,825.623
-2.4434,824.9333
-2.4075,822.7348
-2.3717,819.2448
-2.3359,816.0252
-2.3,816.0252
-2.2642,816.0252
-2.2284,817.2083
-2.1925,821.7567
-2.1567,820.5307
-2.1209,820.5307
-2.085,820.5307
-2.0492,819.8953
-2.0134,819.2448
-1.9775,819.6801
-1.9417,818.5799
-1.9059,817.4407
-1.87,808.8269
-1.8342,808.8269
-1.7984,808.2815
-1.7625,806.3462
-1.7267,804.6582
-1.6909,804.6582
-1.655,806.625
-1.6192,805.5053
-1.5834,805.5053
-1.5475,808.2815
-1.5117,809.9069
-1.4759,808.0074
-1.44,808.0074
-1.4042,809.9069
-1.3684,804.3745
-1.3325,802.084
-1.2967,802.3722
-1.2609,802.9471
-1.225,802.3722
-1.1892,802.3722
-1.1534,802.9471
-1.1175,802.3722
-1.0817,800.3452
-1.0459,798.0057
-1.01,798.8854
-0.97419,798.0057
-0.93835,798.0057
-0.90252,795.9452
-0.86669,794.1736
-0.83085,791.8104
-0.79502,791.8104
-0.75918,791.8104
-0.72335,789.1603
-0.68752,789.1603
-0.65168,788.2809
-0.61585,786.8217
-0.58001,786.8217
-0.54418,788.2809
-0.50835,788.2809
-0.47251,788.2809
-0.43668,788.2809
-0.40084,787.9884
-0.36501,787.6962
-0.32918,784.7958
-0.29334,782.2287
-0.25751,782.2287
-0.22167,784.5083
-0.18584,780.5464
-0.15001,779.9916
-0.11417,778.8917
-0.078338,778.8917
-0.042504,767.6004
-0.0066702,764.4109
0.029164,763.4382
0.064998,763.4382
0.10083,763.4382
0.13667,763.4382
0.1725,763.4382
0.20833,761.5039
0.24417,761.5039
0.28,762.4692
0.31584,762.4692
0.35167,762.4692
0.3875,767.3534
0.42334,767.6004
0.45917,766.1227
0.49501,761.2631
0.53084,761.2631
0.56667,758.6274
0.60251,758.6274
0.63834,760.5419
0.67417,760.5419
0.71001,760.5419
0.74584,758.3889
0.78168,753.4166
0.81751,752.9461
0.85334,753.4166
0.88918,756.9615
0.92501,756.9615
0.96085,757.199
0.99668,761.9861
1.0325,760.0621
1.0683,759.3439
1.1042,760.0621
1.14,761.9861
1.1759,760.0621
1.2117,759.3439
1.2475,757.6744
1.2834,756.9615
1.3192,756.9615
1.355,757.9124
1.3909,760.7821
1.4267,763.1956
1.4625,765.8774
1.4984,765.8774
1.5342,767.1067
1.57,767.1067
1.6059,767.3534
1.6417,766.1227
1.6775,762.9533
1.7134,770.5869
1.7492,770.5869
1.785,768.0952
1.8209,768.0952
1.8567,772.0971
1.8925,772.0971
1.9284,772.0971
1.9642,772.35
2,779.44
2.0359,783.079
2.0717,788.2809
2.1075,790.9255
2.1434,787.6962
2.1792,779.9916
2.215,776.2051
2.2509,767.3534
2.2867,767.3534
2.3225,769.3373
2.3584,773.6193
2.3942,769.3373
2.43,769.3373
2.4659,765.8774
2.5017,765.8774
2.5375,768.0952
2.5734,768.0952
2.6092,768.0952
2.645,766.6142
2.6809,761.0225
2.7167,758.1506
2.7525,756.0131
2.7884,752.476
2.8242,752.2411
2.86,749.4295
2.8959,748.4947
2.9317,748.7283
2.9675,748.7283
3.0034,747.094
3.0392,747.094
3.075,745.6946
3.1109,745.6946
3.1467,742.8973
3.1826,738.462
3.2184,734.4728
3.2542,729.0188
3.2901,722.4428
3.3259,701.4082
3.3617,636.7352
3.3976,557.7395
3.4334,446.5377
3.4692,343.7299
3.5051,65.7397
3.5409,0
3.5767,0
3.6126,0
3.6484,0
3.6842,0
3.7201,0
3.7559,0
3.7917,0
3.8276,0
3.8634,0
3.8992,0
3.9351,0
3.9709,0


"""

p0datos = """


-4.1127,0
-4.0768,0
-4.041,0
-4.0052,0
-3.9693,0
-3.9335,0
-3.8977,0
-3.8618,0
-3.826,0
-3.7902,0
-3.7543,0
-3.7185,0
-3.6827,0
-3.6468,0
-3.611,0
-3.5752,157.8613
-3.5393,319.745
-3.5035,400.4507
-3.4677,465.6119
-3.4318,551.7027
-3.396,623.0042
-3.3602,701.1626
-3.3243,752.2411
-3.2885,779.9916
-3.2527,795.9452
-3.2168,798.2992
-3.181,798.2992
-3.1451,792.9917
-3.1093,791.5153
-3.0735,786.8217
-3.0376,786.8217
-3.0018,784.7958
-2.966,784.7958
-2.9301,784.5083
-2.8943,786.2407
-2.8585,787.6962
-2.8226,790.3363
-2.7868,793.8781
-2.751,793.8781
-2.7151,791.8104
-2.6793,787.9884
-2.6435,781.9466
-2.6076,775.6797
-2.5718,774.1295
-2.536,770.3364
-2.5001,762.7111
-2.4643,761.5039
-2.4285,760.0621
-2.3926,759.3439
-2.3568,758.866
-2.321,761.7449
-2.2851,758.866
-2.2493,762.9533
-2.2135,756.9615
-2.1776,756.487
-2.1418,748.2611
-2.106,744.9952
-2.0701,743.8297
-2.0343,741.9647
-1.9985,736.3535
-1.9626,732.5846
-1.9268,729.7349
-1.891,729.7349
-1.8551,729.7349
-1.8193,729.7349
-1.7835,733.0575
-1.7476,733.0575
-1.7118,732.1112
-1.676,728.5403
-1.6401,728.5403
-1.6043,723.9239
-1.5685,723.9239
-1.5326,723.6777
-1.4968,725.3948
-1.461,720.7038
-1.4251,720.7038
-1.3893,719.9554
-1.3535,720.7038
-1.3176,719.9554
-1.2818,719.9554
-1.2459,717.1986
-1.2101,719.4555
-1.1743,719.9554
-1.1384,719.4555
-1.1026,717.9521
-1.0668,718.4538
-1.0309,718.4538
-0.99511,717.1986
-0.95928,718.4538
-0.92344,718.4538
-0.88761,715.1847
-0.85178,715.1847
-0.81594,714.6805
-0.78011,714.6805
-0.74427,713.6716
-0.70844,714.6805
-0.67261,714.6805
-0.63677,716.9472
-0.60094,721.2017
-0.5651,724.9057
-0.52927,724.9057
-0.49344,726.6118
-0.4576,727.82
-0.42177,727.82
-0.38593,723.9239
-0.3501,724.9057
-0.31427,724.9057
-0.27843,724.9057
-0.2426,724.9057
-0.20676,724.9057
-0.17093,727.0962
-0.1351,730.9251
-0.099263,727.82
-0.063429,729.4964
-0.027595,732.8211
0.0082389,732.8211
0.044073,735.414
0.079907,737.5257
0.11574,739.6308
0.15157,738.228
0.18741,738.228
0.22324,735.8839
0.25908,738.228
0.29491,739.1635
0.33074,746.161
0.36658,748.2611
0.40241,752.711
0.43825,754.1232
0.47408,756.0131
0.50991,756.9615
0.54575,756.7242
0.58158,756.0131
0.61742,753.652
0.65325,750.1314
0.68908,745.2283
0.72492,744.2959
0.76075,744.7621
0.79659,751.0682
0.83242,751.3026
0.86825,751.3026
0.90409,751.3026
0.93992,751.0682
0.97576,748.7283
1.0116,746.8607
1.0474,747.094
1.0833,748.7283
1.1191,748.7283
1.1549,751.5371
1.1908,752.476
1.2266,751.5371
1.2624,751.5371
1.2983,754.359
1.3341,754.359
1.3699,754.359
1.4058,763.9241
1.4416,764.8987
1.4774,766.1227
1.5133,776.4694
1.5491,778.0759
1.5849,778.0759
1.6208,780.825
1.6566,782.5115
1.6924,784.5083
1.7283,784.5083
1.7641,785.6613
1.7999,785.0838
1.8358,785.6613
1.8716,785.6613
1.9074,789.1603
1.9433,790.3363
1.9791,793.8781
2.0149,797.418
2.0508,801.5062
2.0866,808.2815
2.1224,810.7068
2.1583,811.2351
2.1941,810.7068
2.2299,805.7863
2.2658,806.9031
2.3016,806.9031
2.3374,804.0902
2.3733,806.0666
2.4091,806.0666
2.4449,805.5053
2.4808,805.5053
2.5166,805.5053
2.5524,810.4412
2.5883,816.7393
2.6241,820.3206
2.66,821.5564
2.6958,824.7577
2.7316,825.4525
2.7675,825.9602
2.8033,824.7577
2.8391,817.6715
2.875,819.2448
2.9108,819.2448
2.9466,819.2448
2.9825,822.9259
3.0183,826.127
3.0541,826.127
3.09,823.6755
3.1258,822.9259
3.1616,822.5423
3.1975,822.5423
3.2333,822.5423
3.2691,819.8953
3.305,803.8053
3.3408,784.2213
3.3766,690.9679
3.4125,568.8903
3.4483,455.0174
3.4841,333.9723
3.52,38.9763
3.5558,0
3.5916,0
3.6275,0
3.6633,0
3.6991,0
3.735,0
3.7708,0
3.8066,0
3.8425,0
3.8783,0
3.9141,0


"""

# Usamos StringIO para simular un archivo CSV a partir de las cadenas de datos
data_p4 = pd.read_csv(StringIO(p4datos), header=None, names=["posicion", "dosis"])
data_p3 = pd.read_csv(StringIO(p3datos), header=None, names=["posicion", "dosis"])
data_p2 = pd.read_csv(StringIO(p2datos), header=None, names=["posicion", "dosis"])
data_p1 = pd.read_csv(StringIO(p1datos), header=None, names=["posicion", "dosis"])
data_p0 = pd.read_csv(StringIO(p0datos), header=None, names=["posicion", "dosis"])

plt.figure(figsize=(10, 6))

plt.plot(data_p4['posicion'], data_p4['dosis'], label='p = 4 cm')
plt.plot(data_p3['posicion'], data_p3['dosis'], label='p = 3 cm')
plt.plot(data_p2['posicion'], data_p2['dosis'], label='p = 2 cm')
plt.plot(data_p1['posicion'], data_p1['dosis'], label='p = 1 cm')
plt.plot(data_p0['posicion'], data_p0['dosis'], label='p = 0 cm')

plt.xlabel('Distancia fuera del eje [cm]')
plt.ylabel('Dosis [cGy]')
plt.title('9 MeV, aplicador 10 cm, 0° ')
plt.grid()
plt.legend()

plt.show()

plt.plot(data_p4['posicion'], data_p4['dosis'], label='p = 4 cm')

# Implementar análisis para cada perfil de profundidad

profundidades = [data_p4, data_p3, data_p2, data_p1, data_p0]
resultados_fwhm = []
resultados_simetria_planitud = []

for i, data in enumerate(profundidades):
    posicion = data['posicion'].values
    dosis = data['dosis'].values

    # FWHM
    fwhm = calcular_fwhm(posicion, dosis)
    if fwhm is not None:
        print(f'FWHM para p = {4-i} cm: {fwhm:.2f} cm')
    else:
        print(f'FWHM no se pudo calcular para p = {4-i} cm')
    resultados_fwhm.append(fwhm)

    # Simetría y planitud
    simetria, planitud = calcular_simetria_planitud(posicion, dosis)
    if planitud is not None:
        print(f'Simetría para p = {4-i} cm: {simetria:.2f}%')
        print(f'Planitud para p = {4-i} cm: {planitud:.2f}%')
    else:
        print(f'Planitud no se pudo calcular para p = {4-i} cm')

    resultados_simetria_planitud.append((simetria, planitud))

# Visualizar los resultados
print("\nResultados FWHM (Ancho del Haz a la Mitad de la Dosis):", resultados_fwhm)
print("\nResultados de Simetría y Planitud (en porcentaje):", resultados_simetria_planitud)

# Función para calcular FWHM (Full Width Half Maximum)
def calcular_fwhm(posicion, dosis):
    max_dosis = max(dosis)
    half_max_dosis = max_dosis / 2

    # Buscar las posiciones donde la dosis es mayor o igual al 50% de la dosis máxima
    posiciones_half_max = np.where(dosis >= half_max_dosis)[0]

    if len(posiciones_half_max) > 1:
        fwhm_start = posicion[posiciones_half_max[0]]  # Primera posición donde se alcanza el 50%
        fwhm_end = posicion[posiciones_half_max[-1]]  # Última posición donde se alcanza el 50%
        fwhm = abs(fwhm_end - fwhm_start)
        return fwhm, fwhm_start, fwhm_end
    else:
        # Si no se puede calcular el FWHM, devuelve None para los tres valores
        return None, None, None

# Función corregida para calcular la simetría y planitud
def calcular_simetria_planitud(posicion, dosis):
    # Simetría: Compara la dosis a ambos lados del eje central (posicion 0)
    indice_central = np.argmin(np.abs(posicion))  # Encuentra el índice más cercano a 0 (eje central)
    dosis_central = dosis[indice_central]

    izquierda = dosis[:indice_central]
    derecha = dosis[indice_central+1:][::-1]  # Invertir la parte derecha para comparar con la izquierda

    # Asegurarnos de que las dos partes tengan la misma longitud
    if len(izquierda) > len(derecha):
        izquierda = izquierda[:len(derecha)]
    elif len(derecha) > len(izquierda):
        derecha = derecha[:len(izquierda)]

    simetria = np.mean(np.abs(izquierda - derecha) / dosis_central) * 100  # Error relativo porcentual

    # Planitud: Variación dentro del área entre el 80% y 100% de la dosis máxima
    max_dosis = max(dosis)
    limite_inferior = 0.8 * max_dosis

    # Filtrar la región de interés (dosis >= 80% de la dosis máxima)
    indices_region = np.where(dosis >= limite_inferior)[0]

    if len(indices_region) > 0:
        dosis_region = dosis[indices_region]
        max_region = max(dosis_region)
        min_region = min(dosis_region)
        planitud = (max_region - min_region) / (max_region + min_region) * 100
    else:
        planitud = None
        limite_inferior = None
        indices_region = None

    return simetria, planitud, limite_inferior, indices_region

# Implementar análisis para cada perfil de profundidad
profundidades = [data_p4, data_p3, data_p2, data_p1, data_p0]
etiquetas = ['p = 4 cm', 'p = 3 cm', 'p = 2 cm', 'p = 1 cm', 'p = 0 cm']
colores = ['b', 'g', 'r', 'orange', 'purple']

# Generar gráficos individuales para cada curva
for i, data in enumerate(profundidades):
    posicion = data['posicion'].values
    dosis = data['dosis'].values

    # FWHM
    fwhm, fwhm_start, fwhm_end = calcular_fwhm(posicion, dosis)

    # Simetría y planitud
    simetria, planitud, limite_inferior, indices_region = calcular_simetria_planitud(posicion, dosis)

    # Crear un gráfico individual para cada perfil
    plt.figure(figsize=(10, 6))

    # Graficar el perfil
    plt.plot(posicion, dosis, label=etiquetas[i], color=colores[i])

    # Añadir líneas de FWHM en la gráfica (con opacidad baja)
    if fwhm is not None:
        plt.axvline(fwhm_start, color=colores[i], linestyle='--', alpha=0.5, label=f'FWHM: {fwhm:.2f} cm')
        plt.axvline(fwhm_end, color=colores[i], linestyle='--', alpha=0.5)

    # Añadir la región de 80% a 100% de la dosis máxima (planitud)
    if indices_region is not None:
        plt.fill_between(posicion[indices_region], dosis[indices_region], color=colores[i], alpha=0.15, label='Planitud')

    # Imprimir los resultados
    if fwhm is not None:
        print(f'FWHM para {etiquetas[i]}: {fwhm:.2f} cm')
    print(f'Simetría para {etiquetas[i]}: {simetria:.2f}%')
    if planitud is not None:
        print(f'Planitud para {etiquetas[i]}: {planitud:.2f}%')

    # Configuración de la gráfica
    plt.xlabel('Distancia fuera del eje [cm]')
    plt.ylabel('Dosis [cGy]')
    plt.title(f'Análisis de Perfil de Radiación para {etiquetas[i]}')
    plt.grid()

    # Ajustar la leyenda para ser más clara
    plt.legend(loc='upper right', fontsize='small')

    # Mostrar la gráfica individual
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Función corregida para calcular FWHM
def calcular_fwhm(posicion, dosis):
    max_dosis = max(dosis)
    half_max_dosis = max_dosis / 2

    posiciones_half_max = np.where(dosis >= half_max_dosis)[0]

    if len(posiciones_half_max) > 1:
        fwhm_start = posicion[posiciones_half_max[0]]  # Primera posición donde se alcanza el 50%
        fwhm_end = posicion[posiciones_half_max[-1]]  # Última posición donde se alcanza el 50%
        fwhm = abs(fwhm_end - fwhm_start)
        return fwhm, fwhm_start, fwhm_end
    else:
        return None, None, None

# Función corregida para calcular la simetría y planitud
def calcular_simetria_planitud(posicion, dosis):
    indice_central = np.argmin(np.abs(posicion))  # Encuentra el índice más cercano a 0 (eje central)
    dosis_central = dosis[indice_central]

    izquierda = dosis[:indice_central]
    derecha = dosis[indice_central+1:][::-1]  # Invertir la parte derecha para comparar con la izquierda

    if len(izquierda) > len(derecha):
        izquierda = izquierda[:len(derecha)]
    elif len(derecha) > len(izquierda):
        derecha = derecha[:len(izquierda)]

    simetria = np.mean(np.abs(izquierda - derecha) / dosis_central) * 100  # Error relativo porcentual

    # Planitud: Variación dentro del área entre el 80% y 100% de la dosis máxima
    max_dosis = max(dosis)
    limite_inferior = 0.8 * max_dosis

    # Filtrar la región de interés (dosis >= 80% de la dosis máxima)
    indices_region = np.where(dosis >= limite_inferior)[0]

    if len(indices_region) > 0:
        dosis_region = dosis[indices_region]
        max_region = max(dosis_region)
        min_region = min(dosis_region)
        planitud = (max_region - min_region) / (max_region + min_region) * 100
    else:
        planitud = None

    return simetria, planitud

# Implementar análisis para cada perfil de profundidad
profundidades = [data_p4, data_p3, data_p2, data_p1, data_p0]
etiquetas = ['p = 4 cm', 'p = 3 cm', 'p = 2 cm', 'p = 1 cm', 'p = 0 cm']

# Crear una lista para almacenar los resultados
resultados = []

# Realizar el análisis para cada perfil
for i, data in enumerate(profundidades):
    posicion = data['posicion'].values
    dosis = data['dosis'].values

    # Calcular FWHM
    fwhm, _, _ = calcular_fwhm(posicion, dosis)

    # Calcular simetría y planitud
    simetria, planitud = calcular_simetria_planitud(posicion, dosis)

    # Agregar los resultados a la lista
    resultados.append({
        'Profundidad': etiquetas[i],
        'FWHM (cm)': fwhm if fwhm is not None else 'N/A',
        'Simetría (%)': simetria if simetria is not None else 'N/A',
        'Planitud (%)': planitud if planitud is not None else 'N/A'
    })

# Convertir los resultados a un DataFrame de pandas para generar la tabla
df_resultados = pd.DataFrame(resultados)

# Mostrar la tabla
print(df_resultados)

# Opcional: Guardar la tabla en un archivo Excel o CSV
df_resultados.to_csv('resumen_analisis_radiacion.csv', index=False)
# df_resultados.to_excel('resumen_analisis_radiacion.xlsx', index=False)