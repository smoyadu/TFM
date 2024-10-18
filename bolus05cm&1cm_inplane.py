# -*- coding: utf-8 -*-
"""Bolus05cm&1cm_Inplane.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15UyE5SlQjTymG3EK4iCycIif3InvlDRu
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


""" profundidad en cm - datos - bolus 0.5 cm """

p0datos05 = """

-4.1575,0
-4.1216,0
-4.0858,0
-4.05,0
-4.0141,0
-3.9783,0
-3.9425,0
-3.9066,0
-3.8708,0
-3.835,0
-3.7991,0
-3.7633,0
-3.7275,0
-3.6916,0
-3.6558,0
-3.62,0
-3.5841,0
-3.5483,86.004
-3.5125,287.4901
-3.4766,360.1918
-3.4408,436.4441
-3.405,519.5809
-3.3691,586.726
-3.3333,677.9617
-3.2975,772.35
-3.2616,792.1056
-3.2258,820.3206
-3.19,826.127
-3.1541,828.644
-3.1183,828.644
-3.0824,829.6653
-3.0466,830.5081
-3.0108,833.397
-2.9749,835.2484
-2.9391,835.6128
-2.9033,835.37
-2.8674,835.37
-2.8316,835.0046
-2.7958,832.763
-2.7599,831.3243
-2.7241,830.0903
-2.6883,827.4198
-2.6524,828.3439
-2.6166,826.9435
-2.5808,828.3439
-2.5449,827.4198
-2.5091,825.7922
-2.4733,819.2448
-2.4374,817.4407
-2.4016,813.3048
-2.3658,813.3048
-2.3299,813.3048
-2.2941,812.7941
-2.2583,808.2815
-2.2224,807.4569
-2.1866,803.2337
-2.1508,802.6599
-2.1149,805.7863
-2.0791,807.4569
-2.0433,808.0074
-2.0074,808.8269
-1.9716,812.0196
-1.9358,807.4569
-1.8999,803.5198
-1.8641,802.9471
-1.8283,798.8854
-1.7924,802.084
-1.7566,802.084
-1.7208,798.5924
-1.6849,796.8294
-1.6491,795.355
-1.6133,790.9255
-1.5774,788.5737
-1.5416,784.7958
-1.5058,780.5464
-1.4699,780.2686
-1.4341,780.5464
-1.3983,784.2213
-1.3624,784.5083
-1.3266,785.9508
-1.2908,786.8217
-1.2549,784.5083
-1.2191,782.5115
-1.1833,782.5115
-1.1474,776.7347
-1.1116,776.7347
-1.0757,779.9916
-1.0399,779.9916
-1.0041,775.9419
-0.96825,775.9419
-0.93241,776.7347
-0.89658,781.3844
-0.86074,781.3844
-0.82491,781.3844
-0.78908,782.795
-0.75324,781.3844
-0.71741,778.8917
-0.68158,778.8917
-0.64574,779.7154
-0.60991,779.7154
-0.57407,781.1043
-0.53824,781.9466
-0.50241,783.079
-0.46657,782.795
-0.43074,782.795
-0.3949,782.795
-0.35907,784.5083
-0.32324,784.7958
-0.2874,785.3723
-0.25157,787.1128
-0.21573,788.2809
-0.1799,790.3363
-0.14407,785.3723
-0.10823,790.3363
-0.072398,791.5153
-0.036564,793.2872
-0.00073005,785.9508
0.035104,785.9508
0.070938,780.5464
0.10677,784.7958
0.14261,785.0838
0.17844,786.2407
0.21427,789.1603
0.25011,790.6308
0.28594,790.6308
0.32178,789.1603
0.35761,785.0838
0.39344,782.795
0.42928,776.4694
0.46511,773.1105
0.50095,773.1105
0.53678,772.35
0.57261,771.5924
0.60845,771.5924
0.64428,771.3406
0.68012,769.3373
0.71595,775.6797
0.75178,775.6797
0.78762,775.6797
0.82345,773.8743
0.85928,772.6031
0.89512,772.6031
0.93095,771.8446
0.96679,769.8362
1.0026,768.343
1.0385,765.6324
1.0743,764.6547
1.1101,765.8774
1.146,769.0883
1.1818,769.0883
1.2176,772.0971
1.2535,771.089
1.2893,774.1295
1.3251,772.0971
1.361,771.8446
1.3968,769.0883
1.4326,770.8378
1.4685,766.8603
1.5043,768.0952
1.5401,768.5911
1.576,770.8378
1.6118,775.1586
1.6476,778.8917
1.6835,779.1655
1.7193,779.1655
1.7551,773.1105
1.791,773.1105
1.8268,771.089
1.8626,770.5869
1.8985,771.089
1.9343,774.1295
1.9701,768.5911
2.006,766.8603
2.0418,766.8603
2.0776,766.8603
2.1135,766.3683
2.1493,766.3683
2.1851,763.681
2.221,763.4382
2.2568,763.4382
2.2926,763.4382
2.3285,764.4109
2.3643,765.3876
2.4001,763.681
2.436,763.681
2.4718,763.681
2.5076,763.681
2.5435,763.681
2.5793,768.0952
2.6151,767.3534
2.651,767.3534
2.6868,770.0861
2.7227,770.0861
2.7585,767.3534
2.7943,766.8603
2.8302,766.1227
2.866,759.8225
2.9018,759.8225
2.9377,758.3889
2.9735,757.6744
3.0093,766.1227
3.0452,763.681
3.081,766.1227
3.1168,766.1227
3.1527,763.681
3.1885,760.3019
3.2243,755.0671
3.2602,745.9278
3.296,725.1504
3.3318,654.2763
3.3677,555.8033
3.4035,445.058
3.4393,349.4945
3.4752,44.8675
3.511,0
3.5468,0
3.5827,0
3.6185,0
3.6543,0
3.6902,0
3.726,0
3.7618,0
3.7977,0
3.8335,0



"""



p1datos05 = """


-4.0658,0
-4.0299,0
-3.9941,0
-3.9583,0
-3.9224,0
-3.8866,0
-3.8508,0
-3.8149,0
-3.7791,0
-3.7432,0
-3.7074,0
-3.6716,0
-3.6357,0
-3.5999,0
-3.5641,197.8395
-3.5282,303.107
-3.4924,381.417
-3.4566,449.9662
-3.4207,536.8144
-3.3849,585.4767
-3.3491,681.2293
-3.3132,753.1813
-3.2774,779.7154
-3.2416,793.8781
-3.2057,800.9265
-3.1699,803.2337
-3.1341,803.2337
-3.0982,806.9031
-3.0624,809.6383
-3.0266,814.5605
-2.9907,816.9746
-2.9549,820.7391
-2.9191,821.7567
-2.8832,823.3036
-2.8474,825.9602
-2.8116,825.9602
-2.7757,827.7319
-2.7399,828.1924
-2.7041,828.1924
-2.6682,828.7926
-2.6324,831.19
-2.5966,830.6459
-2.5607,829.6653
-2.5249,829.6653
-2.4891,829.8078
-2.4532,829.8078
-2.4174,829.8078
-2.3816,831.3243
-2.3457,832.2475
-2.3099,831.3243
-2.2741,830.5081
-2.2382,831.3243
-2.2024,829.0871
-2.1666,826.9435
-2.1307,827.4198
-2.0949,826.9435
-2.0591,820.3206
-2.0232,819.8953
-1.9874,820.3206
-1.9516,820.3206
-1.9157,822.7348
-1.8799,823.6755
-1.844,823.6755
-1.8082,825.1077
-1.7724,821.5564
-1.7365,822.3482
-1.7007,823.6755
-1.6649,825.9602
-1.629,827.4198
-1.5932,827.4198
-1.5574,824.9333
-1.5215,822.7348
-1.4857,821.5564
-1.4499,822.5423
-1.414,824.4024
-1.3782,827.5764
-1.3424,827.8864
-1.3065,829.8078
-1.2707,828.4944
-1.2349,826.9435
-1.199,826.9435
-1.1632,826.9435
-1.1274,826.7825
-1.0915,826.7825
-1.0557,826.127
-1.0199,826.9435
-0.98403,826.127
-0.9482,825.2807
-0.91237,821.151
-0.87653,821.151
-0.8407,821.151
-0.80486,821.151
-0.76903,821.151
-0.7332,822.7348
-0.69736,825.7922
-0.66153,822.7348
-0.62569,823.4903
-0.58986,822.7348
-0.55403,822.1526
-0.51819,819.2448
-0.48236,820.1088
-0.44653,820.3206
-0.41069,818.8031
-0.37486,820.9459
-0.33902,823.3036
-0.30319,826.2927
-0.26736,826.7825
-0.23152,828.7926
-0.19569,828.644
-0.15985,829.8078
-0.12402,832.2475
-0.088186,834.0212
-0.052352,835.8553
-0.016518,838.2845
0.019316,839.7809
0.05515,839.6541
0.090984,837.1868
0.12682,836.5813
0.16265,834.7602
0.19849,833.6477
0.23432,833.397
0.27015,832.6349
0.30599,831.055
0.34182,831.055
0.37766,830.2303
0.41349,829.5221
0.44932,827.1033
0.48516,824.5807
0.52099,823.4903
0.55683,825.623
0.59266,826.7825
0.62849,827.5764
0.66433,829.5221
0.70016,830.9193
0.736,830.7829
0.77183,830.7829
0.80766,826.127
0.8435,826.127
0.87933,827.5764
0.91517,830.0903
0.951,830.0903
0.98683,830.7829
1.0227,830.0903
1.0585,828.0399
1.0943,827.8864
1.1302,824.4024
1.166,824.2228
1.2018,824.2228
1.2377,828.1924
1.2735,828.0399
1.3093,829.8078
1.3452,829.3779
1.381,828.7926
1.4168,827.2621
1.4527,826.2927
1.4885,826.2927
1.5243,826.6204
1.5602,826.6204
1.596,828.4944
1.6318,829.9494
1.6677,830.6459
1.7035,831.3243
1.7393,834.5149
1.7752,835.9764
1.811,835.9764
1.8468,835.9764
1.8827,835.4915
1.9185,834.2686
1.9543,835.2484
1.9902,835.4915
2.026,835.4915
2.0619,833.271
2.0977,832.5063
2.1335,832.5063
2.1694,831.8554
2.2052,831.458
2.241,831.8554
2.2769,834.0212
2.3127,831.458
2.3485,830.5081
2.3844,829.3779
2.4202,825.9602
2.456,820.9459
2.4919,816.9746
2.5277,814.5605
2.5635,805.7863
2.5994,803.8053
2.6352,802.9471
2.671,801.7954
2.7069,797.712
2.7427,792.4009
2.7785,782.795
2.8144,778.6189
2.8502,776.7347
2.886,771.3406
2.9219,769.8362
2.9577,766.8603
2.9935,764.6547
3.0294,755.7764
3.0652,752.2411
3.101,741.4982
3.1369,734.4728
3.1727,725.1504
3.2085,720.4545
3.2444,716.6956
3.2802,698.2408
3.316,661.0084
3.3519,612.4059
3.3877,550.3964
3.4235,455.504
3.4594,356.7542
3.4952,191.6558
3.531,0
3.5669,0
3.6027,0
3.6385,0
3.6744,0
3.7102,0
3.746,0
3.7819,0
3.8177,0
3.8535,0
3.8894,0
3.9252,0




"""



p2datos05 = """


-4.1739,0
-4.1381,0
-4.1022,0
-4.0664,0
-4.0306,0
-3.9947,0
-3.9589,0
-3.9231,0
-3.8872,0
-3.8514,0
-3.8156,0
-3.7797,0
-3.7439,0
-3.7081,0
-3.6722,0
-3.6364,0
-3.6005,0
-3.5647,0
-3.5289,75.6143
-3.493,196.7624
-3.4572,257.048
-3.4214,310.7178
-3.3855,369.0537
-3.3497,435.8104
-3.3139,498.0472
-3.278,543.9377
-3.2422,553.9605
-3.2064,561.7675
-3.1705,564.9216
-3.1347,567.5983
-3.0989,567.7492
-3.063,569.7397
-3.0272,572.2859
-2.9914,575.0604
-2.9555,578.3074
-2.9197,580.2298
-2.8839,583.5095
-2.848,590.2038
-2.8122,590.2038
-2.7764,590.2038
-2.7405,590.2038
-2.7047,589.2167
-2.6689,588.2511
-2.633,592.6471
-2.5972,595.4864
-2.5614,596.1445
-2.5255,596.1445
-2.4897,598.232
-2.4539,596.1445
-2.418,598.232
-2.3822,601.6471
-2.3464,601.6471
-2.3105,598.7788
-2.2747,599.335
-2.2389,598.5955
-2.203,598.5955
-2.1672,598.5955
-2.1314,601.8457
-2.0955,605.3439
-2.0597,605.3439
-2.0239,605.1323
-1.988,599.5224
-1.9522,597.1677
-1.9164,596.1445
-1.8805,595.4864
-1.8447,595.4864
-1.8089,595.0059
-1.773,594.5371
-1.7372,592.3778
-1.7014,592.3778
-1.6655,591.8551
-1.6297,591.3407
-1.5938,589.8311
-1.558,589.8311
-1.5222,590.5796
-1.4863,590.5796
-1.4505,590.7056
-1.4147,591.5972
-1.3788,591.3407
-1.343,591.0856
-1.3072,591.0856
-1.2713,591.0856
-1.2355,590.2038
-1.1997,589.7076
-1.1638,590.2038
-1.128,590.2038
-1.0922,588.4905
-1.0563,589.5844
-1.0205,589.5844
-0.98467,590.8319
-0.94884,592.3778
-0.913,593.49
-0.87717,594.5371
-0.84134,595.325
-0.8055,595.325
-0.76967,594.3835
-0.73383,594.3835
-0.698,592.784
-0.66217,593.346
-0.62633,589.8311
-0.5905,589.8311
-0.55466,589.8311
-0.51883,588.8521
-0.483,586.1536
-0.44716,588.0129
-0.41133,587.8944
-0.37549,587.6582
-0.33966,584.0467
-0.30383,582.6644
-0.26799,581.7342
-0.23216,581.7342
-0.19632,581.1257
-0.16049,581.1257
-0.12466,579.1612
-0.088822,580.2298
-0.052988,580.2298
-0.017154,580.2298
0.01868,580.9249
0.054514,581.6321
0.090347,581.6321
0.12618,581.6321
0.16202,582.56
0.19785,581.6321
0.23368,582.56
0.26952,582.4559
0.30535,580.5262
0.34119,579.0654
0.37702,579.0654
0.41285,578.0268
0.44869,577.1964
0.48452,574.4572
0.52035,573.7779
0.55619,571.2365
0.59202,569.8175
0.62786,569.0439
0.66369,568.2035
0.69952,568.2035
0.73536,566.6987
0.77119,566.9228
0.80703,566.9228
0.84286,567.7492
0.87869,569.0439
0.91453,569.0439
0.95036,569.1978
0.9862,569.3522
1.022,569.4295
1.0579,569.3522
1.0937,569.1978
1.1295,568.5079
1.1654,568.4317
1.2012,567.3726
1.237,566.4008
1.2729,565.6592
1.3087,565.29
1.3445,565.29
1.3804,565.29
1.4162,566.6242
1.452,566.7734
1.4879,566.8481
1.5237,566.8481
1.5595,567.0725
1.5954,568.1276
1.6312,568.8903
1.667,568.8903
1.7029,568.8903
1.7387,570.9179
1.7745,570.6013
1.8104,570.6013
1.8462,570.9179
1.882,572.0417
1.9179,570.8386
1.9537,570.9974
1.9895,571.3965
2.0254,571.7988
2.0612,571.3965
2.097,570.9974
2.1329,570.8386
2.1687,569.9734
2.2046,569.7397
2.2404,569.4295
2.2762,569.4295
2.3121,566.6987
2.3479,565.9553
2.3837,564.5539
2.4196,561.547
2.4554,560.8841
2.4912,560.8841
2.5271,561.3999
2.5629,561.3263
2.5987,560.7365
2.6346,560.3666
2.6704,559.0253
2.7062,558.1958
2.7421,557.968
2.7779,557.8919
2.8137,557.8919
2.8496,557.5868
2.8854,557.357
2.9212,555.3289
2.9571,555.8033
2.9929,555.8033
3.0287,555.7245
3.0646,553.7151
3.1004,553.3858
3.1362,553.1373
3.1721,551.0981
3.2079,549.412
3.2437,544.1377
3.2796,535.538
3.3154,489.7585
3.3512,411.933
3.3871,311.7066
3.4229,227.5482
3.4587,20.5965
3.4946,0
3.5304,0
3.5662,0
3.6021,0
3.6379,0
3.6737,0
3.7096,0
3.7454,0
3.7812,0
3.8171,0



"""


""" profundidad en cm - datos - bolus 1 cm """


p0datos1 = """


-3.8506,0
-3.8147,0
-3.7789,0
-3.7431,0
-3.7072,0
-3.6714,0
-3.6356,0
-3.5997,176.7402
-3.5639,269.6846
-3.5281,323.2718
-3.4922,391.772
-3.4564,463.6904
-3.4206,531.2252
-3.3847,574.0314
-3.3489,623.9196
-3.3131,652.6626
-3.2772,669.744
-3.2414,680.0594
-3.2056,689.1724
-3.1697,695.3726
-3.1339,712.9147
-3.0981,722.195
-3.0622,727.5791
-3.0264,728.3006
-2.9906,731.1626
-2.9547,733.7657
-2.9189,734.0016
-2.8831,745.6946
-2.8472,750.3654
-2.8114,753.652
-2.7756,764.6547
-2.7397,767.3534
-2.7039,770.5869
-2.6681,770.5869
-2.6322,770.5869
-2.5964,772.8567
-2.5606,772.8567
-2.5247,776.2051
-2.4889,781.1043
-2.4531,787.6962
-2.4172,788.5737
-2.3814,791.5153
-2.3455,792.4009
-2.3097,792.4009
-2.2739,797.712
-2.238,798.8854
-2.2022,802.9471
-2.1664,805.7863
-2.1305,806.0666
-2.0947,808.2815
-2.0589,809.0983
-2.023,809.0983
-1.9872,811.2351
-1.9514,812.0196
-1.9155,811.2351
-1.8797,812.5371
-1.8439,812.7941
-1.808,812.7941
-1.7722,813.8107
-1.7364,811.4976
-1.7005,802.3722
-1.6647,806.9031
-1.6289,807.4569
-1.593,806.9031
-1.5572,806.9031
-1.5214,806.0666
-1.4855,804.9412
-1.4497,805.5053
-1.4139,807.4569
-1.378,807.7326
-1.3422,812.2789
-1.3064,812.2789
-1.2705,810.9715
-1.2347,808.0074
-1.1989,806.625
-1.163,803.2337
-1.1272,803.2337
-1.0914,801.7954
-1.0555,802.9471
-1.0197,806.0666
-0.98386,811.2351
-0.94802,813.3048
-0.91219,812.7941
-0.87636,812.7941
-0.84052,810.7068
-0.80469,810.7068
-0.76885,812.7941
-0.73302,818.1287
-0.69719,816.7393
-0.66135,816.9746
-0.62552,818.1287
-0.58968,818.1287
-0.55385,818.1287
-0.51802,819.8953
-0.48218,820.1088
-0.44635,818.5799
-0.41052,812.2789
-0.37468,807.4569
-0.33885,802.6599
-0.30301,802.6599
-0.26718,807.1804
-0.23135,800.3452
-0.19551,799.4703
-0.15968,799.4703
-0.12384,798.2992
-0.08801,798.2992
-0.052176,798.5924
-0.016342,798.5924
0.019492,797.712
0.055326,796.8294
0.09116,791.8104
0.12699,796.8294
0.16283,796.8294
0.19866,798.0057
0.2345,800.6361
0.27033,802.6599
0.30616,804.9412
0.342,810.7068
0.37783,812.0196
0.41367,812.0196
0.4495,806.9031
0.48533,804.0902
0.52117,791.8104
0.557,790.6308
0.59284,790.0419
0.62867,787.1128
0.6645,785.6613
0.70034,776.7347
0.73617,771.3406
0.77201,766.8603
0.80784,766.1227
0.84367,767.6004
0.87951,767.6004
0.91534,769.0883
0.95118,769.8362
0.98701,771.3406
1.0228,772.0971
1.0587,772.8567
1.0945,772.8567
1.1303,772.0971
1.1662,777.001
1.202,764.6547
1.2378,774.3852
1.2737,776.7347
1.3095,777.2683
1.3453,777.2683
1.3812,777.2683
1.417,783.079
1.4529,782.5115
1.4887,781.1043
1.5245,781.3844
1.5604,782.5115
1.5962,781.1043
1.632,783.3637
1.6679,785.9508
1.7037,789.1603
1.7395,787.1128
1.7754,793.8781
1.8112,797.1238
1.847,797.418
1.8829,795.355
1.9187,797.418
1.9545,796.8294
1.9904,795.355
2.0262,786.8217
2.062,787.1128
2.0979,787.1128
2.1337,786.8217
2.1695,789.4539
2.2054,792.1056
2.2412,789.4539
2.277,785.9508
2.3129,784.7958
2.3487,778.8917
2.3845,772.0971
2.4204,766.3683
2.4562,760.7821
2.492,756.7242
2.5279,752.2411
2.5637,752.0063
2.5995,748.0276
2.6354,744.0628
2.6712,741.9647
2.707,741.9647
2.7429,737.994
2.7787,735.649
2.8145,735.1789
2.8504,733.7657
2.8862,730.2115
2.922,723.9239
2.9579,721.947
2.9937,720.4545
3.0295,716.9472
3.0654,715.4367
3.1012,715.6887
3.137,710.8966
3.1729,707.8762
3.2087,702.3933
3.2445,694.9005
3.2804,687.8516
3.3162,668.7252
3.352,632.0917
3.3879,567.2975
3.4237,476.5135
3.4596,375.4911
3.4954,273.7936
3.5312,0
3.5671,0
3.6029,0
3.6387,0
3.6746,0
3.7104,0
3.7462,0
3.7821,0
3.8179,0
3.8537,0
3.8896,0
3.9254,0
3.9612,0
3.9971,0
4.0329,0
4.0687,0
4.1046,0
4.1404,0
4.1762,0



"""



p1datos1 = """


-3.9162,0
-3.8804,0
-3.8445,0
-3.8087,0
-3.7729,0
-3.737,0
-3.7012,0
-3.6654,0
-3.6295,0
-3.5937,0
-3.5578,0
-3.522,0.82082
-3.4862,265.8114
-3.4503,332.0309
-3.4145,419.5987
-3.3787,490.8801
-3.3428,560.7365
-3.307,628.6393
-3.2712,698.9666
-3.2353,748.4947
-3.1995,772.8567
-3.1637,781.1043
-3.1278,796.5348
-3.092,813.0501
-3.0562,819.2448
-3.0203,825.9602
-2.9845,826.6204
-2.9487,824.4024
-2.9128,824.4024
-2.877,824.4024
-2.8412,822.7348
-2.8053,822.7348
-2.7695,824.4024
-2.7337,823.6755
-2.6978,824.0418
-2.662,824.2228
-2.6262,828.644
-2.5903,829.9494
-2.5545,830.6459
-2.5187,830.6459
-2.4828,830.5081
-2.447,831.19
-2.4112,830.5081
-2.3753,829.8078
-2.3395,829.3779
-2.3037,829.3779
-2.2678,827.4198
-2.232,826.127
-2.1962,824.9333
-2.1603,827.4198
-2.1245,827.4198
-2.0887,829.9494
-2.0528,830.6459
-2.017,831.9866
-1.9812,833.897
-1.9453,834.5149
-1.9095,834.2686
-1.8737,835.0046
-1.8378,834.7602
-1.802,832.5063
-1.7662,829.6653
-1.7303,828.644
-1.6945,827.8864
-1.6587,827.2621
-1.6228,827.2621
-1.587,827.2621
-1.5511,828.0399
-1.5153,829.3779
-1.4795,829.5221
-1.4436,829.6653
-1.4078,828.3439
-1.372,822.3482
-1.3361,819.0248
-1.3003,813.5584
-1.2645,812.5371
-1.2286,812.5371
-1.1928,813.0501
-1.157,814.8079
-1.1211,813.0501
-1.0853,814.8079
-1.0495,814.0619
-1.0136,809.3688
-0.9778,809.3688
-0.94197,810.9715
-0.90614,810.9715
-0.8703,811.4976
-0.83447,812.5371
-0.79864,811.4976
-0.7628,811.4976
-0.72697,811.4976
-0.69113,805.5053
-0.6553,808.5546
-0.61947,810.4412
-0.58363,812.0196
-0.5478,811.7591
-0.51196,813.0501
-0.47613,812.0196
-0.4403,809.6383
-0.40446,805.7863
-0.36863,805.7863
-0.33279,803.2337
-0.29696,799.4703
-0.26113,799.4703
-0.22529,801.7954
-0.18946,807.7326
-0.15362,810.4412
-0.11779,813.0501
-0.081956,810.4412
-0.046122,801.7954
-0.010288,799.178
0.025546,796.2401
0.06138,794.7644
0.097214,797.418
0.13305,797.418
0.16888,797.418
0.20472,798.0057
0.24055,797.418
0.27638,794.7644
0.31222,792.6963
0.34805,789.1603
0.38389,788.5737
0.41972,788.5737
0.45555,788.5737
0.49139,788.5737
0.52722,791.2203
0.56305,790.0419
0.59889,790.0419
0.63472,790.0419
0.67056,791.5153
0.70639,789.1603
0.74222,787.4043
0.77806,787.4043
0.81389,789.4539
0.84973,786.8217
0.88556,787.1128
0.92139,787.9884
0.95723,790.3363
0.99306,792.6963
1.0289,796.2401
1.0647,797.1238
1.1006,797.1238
1.1364,797.1238
1.1722,797.712
1.2081,797.1238
1.2439,797.418
1.2797,798.8854
1.3156,798.8854
1.3514,800.6361
1.3872,802.9471
1.4231,808.0074
1.4589,817.6715
1.4947,821.9554
1.5306,823.3036
1.5664,823.8593
1.6022,825.623
1.6381,825.4525
1.6739,828.4944
1.7097,831.8554
1.7456,833.0179
1.7814,833.7726
1.8172,834.0212
1.8531,834.8825
1.8889,835.0046
1.9247,835.7341
1.9606,835.7341
1.9964,835.7341
2.0322,835.7341
2.0681,834.3919
2.1039,834.5149
2.1397,835.7341
2.1756,837.4296
2.2114,838.2845
2.2473,839.402
2.2831,842.847
2.3189,842.5664
2.3548,842.847
2.3906,843.8552
2.4264,844.0027
2.4623,848.7482
2.4981,850.0534
2.5339,850.2458
2.5698,850.2458
2.6056,850.8319
2.6414,850.0534
2.6773,850.2458
2.7131,851.2304
2.7489,850.2458
2.7848,848.7482
2.8206,848.7482
2.8564,845.3741
2.8923,844.7546
2.9281,844.7546
2.9639,844.7546
2.9998,844.7546
3.0356,845.2177
3.0714,844.7546
3.1073,843.274
3.1431,841.4733
3.1789,838.5307
3.2148,835.0046
3.2506,813.0501
3.2864,735.649
3.3223,592.9223
3.3581,482.2919
3.3939,366.5816
3.4298,72.6061
3.4656,0
3.5014,0
3.5373,0
3.5731,0
3.6089,0
3.6448,0
3.6806,0
3.7164,0
3.7523,0
3.7881,0
3.8239,0
3.8598,0
3.8956,0
3.9314,0
3.9673,0
4.0031,0
4.0389,0
4.0748,0




"""



p2datos1 = """

-3.8277,0
-3.7918,0
-3.756,0
-3.7202,0
-3.6843,0
-3.6485,0
-3.6127,0
-3.5768,0
-3.541,0
-3.5052,0
-3.4693,0
-3.4335,0
-3.3977,0
-3.3618,0
-3.326,0
-3.2902,0
-3.2543,0
-3.2185,0
-3.1827,0
-3.1468,0
-3.111,0
-3.0752,111.275
-3.0393,238.3237
-3.0035,252.9572
-2.9677,262.2809
-2.9318,287.2497
-2.896,307.7498
-2.8602,326.1207
-2.8243,345.1647
-2.7885,348.3237
-2.7527,355.7273
-2.7168,357.4632
-2.681,359.4088
-2.6452,361.437
-2.6093,361.8974
-2.5735,363.0852
-2.5377,365.1471
-2.5018,366.2366
-2.466,366.2366
-2.4302,366.2366
-2.3943,365.8254
-2.3585,365.8254
-2.3227,366.1678
-2.2868,366.1678
-2.251,366.1678
-2.2151,367.6996
-2.1793,368.9817
-2.1435,367.348
-2.1076,370.655
-2.0718,370.876
-2.036,371.3198
-2.0001,372.967
-1.9643,372.967
-1.9285,373.3455
-1.8926,373.3455
-1.8568,372.816
-1.821,369.7773
-1.7851,368.1242
-1.7493,365.9621
-1.7135,365.621
-1.6776,364.0128
-1.6418,364.0128
-1.606,364.212
-1.5701,364.0792
-1.5343,363.8801
-1.4985,363.8801
-1.4626,360.5189
-1.4268,358.7584
-1.391,357.3986
-1.3551,358.4339
-1.3193,356.5613
-1.2835,356.5613
-1.2476,359.0183
-1.2118,359.2135
-1.176,359.2135
-1.1401,357.7863
-1.1043,357.5278
-1.0685,357.5278
-1.0326,357.8509
-0.99679,358.3042
-0.96096,359.9958
-0.92513,363.9464
-0.88929,363.9464
-0.85346,363.9464
-0.81762,363.9464
-0.78179,364.212
-0.74596,364.1456
-0.71012,364.1456
-0.67429,364.1456
-0.63845,364.212
-0.60262,365.2146
-0.56679,367.0681
-0.53095,367.7702
-0.49512,366.2366
-0.45928,366.0306
-0.42345,365.553
-0.38762,365.8254
-0.35178,364.8114
-0.31595,364.0128
-0.28012,364.8114
-0.24428,365.2821
-0.20845,365.2821
-0.17261,364.7445
-0.13678,365.3497
-0.10095,366.5816
-0.065111,366.2366
-0.029278,365.8937
0.0065564,366.0992
0.04239,366.0306
0.078224,366.0306
0.11406,364.5444
0.14989,363.2175
0.18573,364.7445
0.22156,363.019
0.25739,362.8207
0.29323,362.8207
0.32906,361.5027
0.3649,359.1484
0.40073,359.4088
0.43656,359.1484
0.4724,359.1484
0.50823,359.1484
0.54407,359.2135
0.5799,359.2135
0.61573,360.0612
0.65157,360.1265
0.6874,360.5189
0.72324,360.5844
0.75907,360.2572
0.7949,360.5189
0.83074,360.5844
0.86657,360.5844
0.90241,362.4906
0.93824,365.1471
0.97407,365.1471
1.0099,366.0992
1.0457,366.7896
1.0816,366.1678
1.1174,368.2663
1.1532,369.4869
1.1891,369.5594
1.2249,368.6231
1.2607,369.4869
1.2966,369.9958
1.3324,370.7286
1.3682,369.7773
1.4041,372.2895
1.4399,372.2895
1.4757,372.2145
1.5116,372.7406
1.5474,373.3455
1.5833,373.3455
1.6191,373.8016
1.6549,373.4214
1.6908,373.6493
1.7266,374.7968
1.7624,378.3072
1.7983,379.02
1.8341,380.2946
1.8699,378.3072
1.9058,377.9915
1.9416,375.6459
1.9774,377.9915
2.0133,376.5792
2.0491,378.3862
2.0849,379.4969
2.1208,380.6947
2.1566,379.4969
2.1924,380.6947
2.2283,380.9352
2.2641,378.8613
2.2999,378.8613
2.3358,378.8613
2.3716,378.8613
2.4074,377.8338
2.4433,377.1267
2.4791,375.4911
2.5149,374.6431
2.5508,374.3363
2.5866,373.4973
2.6224,373.4973
2.6583,372.816
2.6941,372.1396
2.7299,369.27
2.7658,367.2779
2.8016,364.2785
2.8374,362.9529
2.8733,362.9529
2.9091,356.497
2.9449,346.0086
2.9808,318.991
3.0166,192.5358
3.0524,0
3.0883,0
3.1241,0
3.1599,0
3.1958,0
3.2316,0
3.2674,0
3.3033,0
3.3391,0
3.3749,0
3.4108,0
3.4466,0
3.4824,0
3.5183,0
3.5541,0
3.59,0
3.6258,0
3.6616,0
3.6975,0
3.7333,0
3.7691,0
3.805,0
3.8408,0
3.8766,0
3.9125,0
3.9483,0
3.9841,0
4.02,0
4.0558,0
4.0916,0
4.1275,0
4.1633,0
4.1991,0




"""

# Usamos StringIO para simular un archivo CSV a partir de las cadenas de datos
data_05p0 = pd.read_csv(StringIO(p0datos05), header=None, names=["posicion", "dosis"])
data_05p1 = pd.read_csv(StringIO(p1datos05), header=None, names=["posicion", "dosis"])
data_05p2 = pd.read_csv(StringIO(p2datos05), header=None, names=["posicion", "dosis"])
data_1p0 = pd.read_csv(StringIO(p0datos1), header=None, names=["posicion", "dosis"])
data_1p1 = pd.read_csv(StringIO(p1datos1), header=None, names=["posicion", "dosis"])
data_1p2 = pd.read_csv(StringIO(p2datos1), header=None, names=["posicion", "dosis"])

plt.figure(figsize=(10, 6))

plt.plot(data_05p0['posicion'], data_05p0['dosis'], label='p = 0 cm b = 0.5 cm')
plt.plot(data_05p1['posicion'], data_05p1['dosis'], label='p = 1 cm b = 0.5 cm ')
plt.plot(data_05p2['posicion'], data_05p2['dosis'], label='p = 2 cm b = 0.5 cm')
plt.plot(data_1p0['posicion'], data_1p0['dosis'], label='p = 0 cm b = 1 cm')
plt.plot(data_1p1['posicion'], data_1p1['dosis'], label='p = 1 cm b = 1 cm')
plt.plot(data_1p2['posicion'], data_1p2['dosis'], label='p = 2 cm b = 1 cm')

plt.xlabel('Distancia fuera del eje [cm]')
plt.ylabel('Dosis [cGy]')
plt.title('9 MeV, aplicador 10 cm, 0° ')
plt.grid()
plt.legend()

plt.show()

plt.figure(figsize=(10, 6))

# Curvas con b = 0.5 cm (usamos líneas continuas)
plt.plot(data_05p0['posicion'], data_05p0['dosis'], label='p = 0 cm b = 0.5 cm', linestyle='-', marker='o')
plt.plot(data_05p1['posicion'], data_05p1['dosis'], label='p = 1 cm b = 0.5 cm', linestyle='-', marker='o')
plt.plot(data_05p2['posicion'], data_05p2['dosis'], label='p = 2 cm b = 0.5 cm', linestyle='-', marker='o')

# Curvas con b = 1 cm (usamos líneas punteadas)
plt.plot(data_1p0['posicion'], data_1p0['dosis'], label='p = 0 cm b = 1 cm', linestyle='--', marker='x')
plt.plot(data_1p1['posicion'], data_1p1['dosis'], label='p = 1 cm b = 1 cm', linestyle='--', marker='x')
plt.plot(data_1p2['posicion'], data_1p2['dosis'], label='p = 2 cm b = 1 cm', linestyle='--', marker='x')

plt.xlabel('Distancia fuera del eje [cm]')
plt.ylabel('Dosis [cGy]')
plt.title('9 MeV, aplicador 10 cm, 0°')
plt.grid(True)
plt.legend()
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

# Datos de dos conjuntos de características b = 0.5 cm y b = 1 cm
profundidades_05 = [data_05p0, data_05p1, data_05p2]
profundidades_1 = [data_1p0, data_1p1, data_1p2]

etiquetas_05 = ['p = 0 cm b = 0.5 cm', 'p = 1 cm b = 0.5 cm', 'p = 2 cm b = 0.5 cm']
etiquetas_1 = ['p = 0 cm b = 1 cm', 'p = 1 cm b = 1 cm', 'p = 2 cm b = 1 cm']

# Crear una lista para almacenar los resultados
resultados = []

# Realizar el análisis para cada perfil de b = 0.5 cm
for i, data in enumerate(profundidades_05):
    posicion = data['posicion'].values
    dosis = data['dosis'].values

    # Calcular FWHM
    fwhm, _, _ = calcular_fwhm(posicion, dosis)

    # Calcular simetría y planitud
    simetria, planitud = calcular_simetria_planitud(posicion, dosis)

    # Agregar los resultados a la lista
    resultados.append({
        'Característica': etiquetas_05[i],
        'FWHM (cm)': fwhm if fwhm is not None else 'N/A',
        'Simetría (%)': simetria if simetria is not None else 'N/A',
        'Planitud (%)': planitud if planitud is not None else 'N/A'
    })

# Realizar el análisis para cada perfil de b = 1 cm
for i, data in enumerate(profundidades_1):
    posicion = data['posicion'].values
    dosis = data['dosis'].values

    # Calcular FWHM
    fwhm, _, _ = calcular_fwhm(posicion, dosis)

    # Calcular simetría y planitud
    simetria, planitud = calcular_simetria_planitud(posicion, dosis)

    # Agregar los resultados a la lista
    resultados.append({
        'Característica': etiquetas_1[i],
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