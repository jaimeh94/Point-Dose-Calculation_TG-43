import pandas as pd
import numpy as np
from datetime import datetime

# cGy/h/U, cGy cm2/h
DoseRateConstant = 1.1080 
#Activity Ci
Activity = 12
#Air kerma rate constant (cGy cm2/h / mCi) = 4.082

length=3.6 #mm

RAKR = 52190 # uGy/h at 1 m
# CalDate = datetime(2020,11,18,13,9)
MeanLife=73.83 # dias


# f(r,theta)
# r(mm) 0-5-10-15-20-25-30-35-40-45-50-55-60
Anisotropy2D =pd.DataFrame([[0.0,	0.7910,	0.7950,	0.7850,	0.8370,	0.8760,	0.9083,	0.9360,	0.9442,	0.9589,	0.9694,	0.9724,	0.9780,	0.9845,	0.9897,	0.9919,	0.9894,	0.9849,	0.9861,	1.0000,	1.0058,	0.9996,	0.9930,	0.9908,	0.9893,	0.9844,	0.9775,	0.9769,	0.9736,	0.9591,	0.9460,	0.9262,	0.9061,	0.8830,	0.8330,	0.8063,	0.7976,	0.7159],	
[5.0,	  0.6670,	0.6710,	0.7270,	0.7863,	0.8360,	0.8749,	0.9040,	0.9262,	0.9433,	0.9564,	0.9672,	0.9770,	0.9849,	0.9906,	0.9949,	0.9983,	1.0009,	1.0017,	1.0000,	0.9977,	0.9959,	0.9944,	0.9925,	0.9896,	0.9848,	0.9776,	0.9678,	0.9564,	0.9432,	0.9251,	0.9024,	0.8729,	0.8324,	0.7790,	0.7100,	0.6230,	0.6090],	
[10.0,	0.6310,	0.6610,	0.7270,	0.7893,	0.8390,	0.8752,	0.9020,	0.9250,	0.9429,	0.9575,	0.9693,	0.9778,	0.9846,	0.9904,	0.9950,	0.9980,	0.9995,	1.0000,	1.0000,	1.0009,	1.0015,	1.0000,	0.9957,	0.9902,	0.9851,	0.9801,	0.9725,	0.9608,	0.9456,	0.9272,	0.9041,	0.8735,	0.8320,	0.7780,	0.7070,	0.6240,	0.5850],	
[15.0,	0.6339,	0.6751,	0.7378,	0.7981,	0.8449,	0.8796,	0.9058,	0.9264,	0.9460,	0.9601,	0.9691,	0.9773,	0.9847,	0.9910,	0.9955,	0.9979,	0.9984,	0.9986,	1.0000,	1.0018,	1.0024,	1.0006,	0.9963,	0.9910,	0.9860,	0.9810,	0.9736,	0.9621,	0.9466,	0.9284,	0.9058,	0.8765,	0.8380,	0.7862,	0.7201,	0.6461,	0.5917],	
[20.0,	0.6450,	0.6840,	0.7450,	0.8017,	0.8460,	0.8803,	0.9070,	0.9270,	0.9481,	0.9612,	0.9679,	0.9767,	0.9852,	0.9917,	0.9962,	0.9988,	0.9999,	1.0000,	1.0000,	1.0001,	0.9997,	0.9983,	0.9955,	0.9917,	0.9871,	0.9810,	0.9719,	0.9601,	0.9456,	0.9275,	0.9054,	0.8768,	0.8400,	0.7910,	0.7270,	0.6520,	0.6030],	
[25.0,	0.6535,	0.6920,	0.7516,	0.8065,	0.8492,	0.8809,	0.9066,	0.9282,	0.9492,	0.9624,	0.9696,	0.9778,	0.9854,	0.9914,	0.9957,	0.9985,	0.9999,	1.0003,	1.0000,	0.9998,	0.9995,	0.9982,	0.9956,	0.9920,	0.9875,	0.9818,	0.9740,	0.9630,	0.9487,	0.9312,	0.9093,	0.8805,	0.8433,	0.7959,	0.7341,	0.6606,	0.6130],	
[30.0,	0.6600,	0.7000,	0.7580,	0.8122,	0.8540,	0.8820,	0.9060,	0.9296,	0.9497,	0.9634,	0.9723,	0.9794,	0.9852,	0.9902,	0.9941,	0.9970,	0.9989,	0.9998,	1.0000,	1.0004,	1.0006,	0.9992,	0.9960,	0.9917,	0.9872,	0.9828,	0.9779,	0.9679,	0.9532,	0.9366,	0.9150,	0.8857,	0.8472,	0.8010,	0.7420,	0.6720,	0.6220],	
[35.0,	0.6676,	0.7084,	0.7642,	0.8175,	0.8587,	0.8837,	0.9062,	0.9303,	0.9497,	0.9636,	0.9733,	0.9797,	0.9845,	0.9885,	0.9920,	0.9951,	0.9979,	0.9996,	1.0000,	1.0005,	1.0007,	0.9992,	0.9954,	0.9908,	0.9865,	0.9831,	0.9799,	0.9708,	0.9557,	0.9394,	0.9186,	0.8893,	0.8501,	0.8055,	0.7499,	0.6822,	0.6314],	
[40.0,	0.6765,	0.7170,	0.7703,	0.8222,	0.8631,	0.8859,	0.9073,	0.9304,	0.9494,	0.9630,	0.9725,	0.9789,	0.9832,	0.9864,	0.9893,	0.9929,	0.9969,	0.9998,	1.0000,	0.9999,	0.9998,	0.9979,	0.9940,	0.9893,	0.9854,	0.9827,	0.9800,	0.9713,	0.9559,	0.9394,	0.9200,	0.8912,	0.8520,	0.8094,	0.7579,	0.6910,	0.6414],	
[45.0,	0.6862,	0.7259,	0.7762,	0.8266,	0.8674,	0.8885,	0.9090,	0.9300,	0.9488,	0.9619,	0.9705,	0.9771,	0.9814,	0.9839,	0.9862,	0.9903,	0.9959,	1.0001,	1.0000,	0.9990,	0.9982,	0.9959,	0.9918,	0.9873,	0.9840,	0.9818,	0.9789,	0.9704,	0.9545,	0.9375,	0.9199,	0.8920,	0.8533,	0.8128,	0.7659,	0.6990,	0.6517],	
[50.0,	0.6960,	0.7350,	0.7820,	0.8309,	0.8720,	0.8915,	0.9110,	0.9293,	0.9478,	0.9604,	0.9680,	0.9749,	0.9793,	0.9810,	0.9827,	0.9874,	0.9947,	1.0004,	1.0000,	0.9980,	0.9964,	0.9936,	0.9893,	0.9849,	0.9822,	0.9806,	0.9772,	0.9688,	0.9525,	0.9347,	0.9191,	0.8924,	0.8541,	0.8160,	0.7740,	0.7070,	0.6620]],
columns=['r(mm)\\theta(°)', '0',	'5',	'10',	'15',	'20',	'25',	'30',	'35',	'40',	'45',	'50',	'55',	'60',	'65',	'70',	'75',	'80',	'85',	'90',	'95',	'100',	'105',	'110',	'115',	'120',	'125',	'130',	'135',	'140',	'145',	'150',	'155',	'160',	'165',	'170',	'175',	'180']
)
Anisotropy2D = Anisotropy2D.drop('r(mm)\\theta(°)',axis=1)

# g(r)
#r(mm) g(r)
RadialDoseFuntion = pd.DataFrame([[0.0,	1.0080	],
[5.0,	1.0000	],
[10.0,	1.0000	],
[15.0,	1.0030	],
[20.0,	1.0070	],
[25.0,	1.0080	],
[30.0,	1.0080	],
[35.0,	1.0067	],
[40.0,	1.0040	],
[45.0,	1.0002	],
[50.0,	0.9950	],
[55.0,	0.9884	],
[60.0,	0.9810	],
[65.0,	0.9732	],
[70.0,	0.9640	],
[75.0,	0.9527	],
[80.0,	0.9400	],
[85.0,	0.9268	],
[90.0,	0.9130	],
[95.0,	0.8982	],
[100.0,	0.8820],	
[105.0,	0.8639],	
[110.0,	0.8440],	
[115.0,	0.8222],	
[120.0,	0.7990],	
[125.0,	0.7743],	
[130.0,	0.7470],	
[135.0,	0.7158],	
[140.0,	0.6810]],columns=['r(mm)','g(r)'])

class Source:
  """
  Class of Source Ir-192
  """
  def __init__(self, Activity,DoseRateConstant,Anisotropy2D,RadialDoseFuntion,length,RAKR,CalDate,MeanLife):
    self.Activity=Activity
    self.DoseRateConstant=DoseRateConstant
    self.Anisotropy2D=Anisotropy2D
    self.RadialDoseFuntion=RadialDoseFuntion
    self.length=length
    self.RAKR=RAKR
    self.CalDate=CalDate
    self.MeanLife=MeanLife

# Ir_192=Source(Activity=Activity,DoseRateConstant=DoseRateConstant,Anisotropy2D=Anisotropy2D,RadialDoseFuntion=RadialDoseFuntion,length=length,RAKR=RAKR,CalDate=CalDate,MeanLife=MeanLife)

class Ir_192:
  """
  Class of Source Ir-192
  """
  def __init__(self, CalDate, RAKR):
    # cGy/h/U, cGy cm2/h
    DoseRateConstant = 1.1080 
    #Activity Ci
    Activity = 12
    #Air kerma rate constant (cGy cm2/h / mCi) = 4.082

    length=3.6 #mm

    # RAKR = 52190 # uGy/h at 1 m
    # CalDate = datetime(2020,11,18,13,9)
    MeanLife=73.83 # dias


    # f(r,theta)
    # r(mm) 0-5-10-15-20-25-30-35-40-45-50-55-60
    Anisotropy2D =pd.DataFrame([[0.0,	0.7910,	0.7950,	0.7850,	0.8370,	0.8760,	0.9083,	0.9360,	0.9442,	0.9589,	0.9694,	0.9724,	0.9780,	0.9845,	0.9897,	0.9919,	0.9894,	0.9849,	0.9861,	1.0000,	1.0058,	0.9996,	0.9930,	0.9908,	0.9893,	0.9844,	0.9775,	0.9769,	0.9736,	0.9591,	0.9460,	0.9262,	0.9061,	0.8830,	0.8330,	0.8063,	0.7976,	0.7159],	
    [5.0,	  0.6670,	0.6710,	0.7270,	0.7863,	0.8360,	0.8749,	0.9040,	0.9262,	0.9433,	0.9564,	0.9672,	0.9770,	0.9849,	0.9906,	0.9949,	0.9983,	1.0009,	1.0017,	1.0000,	0.9977,	0.9959,	0.9944,	0.9925,	0.9896,	0.9848,	0.9776,	0.9678,	0.9564,	0.9432,	0.9251,	0.9024,	0.8729,	0.8324,	0.7790,	0.7100,	0.6230,	0.6090],	
    [10.0,	0.6310,	0.6610,	0.7270,	0.7893,	0.8390,	0.8752,	0.9020,	0.9250,	0.9429,	0.9575,	0.9693,	0.9778,	0.9846,	0.9904,	0.9950,	0.9980,	0.9995,	1.0000,	1.0000,	1.0009,	1.0015,	1.0000,	0.9957,	0.9902,	0.9851,	0.9801,	0.9725,	0.9608,	0.9456,	0.9272,	0.9041,	0.8735,	0.8320,	0.7780,	0.7070,	0.6240,	0.5850],	
    [15.0,	0.6339,	0.6751,	0.7378,	0.7981,	0.8449,	0.8796,	0.9058,	0.9264,	0.9460,	0.9601,	0.9691,	0.9773,	0.9847,	0.9910,	0.9955,	0.9979,	0.9984,	0.9986,	1.0000,	1.0018,	1.0024,	1.0006,	0.9963,	0.9910,	0.9860,	0.9810,	0.9736,	0.9621,	0.9466,	0.9284,	0.9058,	0.8765,	0.8380,	0.7862,	0.7201,	0.6461,	0.5917],	
    [20.0,	0.6450,	0.6840,	0.7450,	0.8017,	0.8460,	0.8803,	0.9070,	0.9270,	0.9481,	0.9612,	0.9679,	0.9767,	0.9852,	0.9917,	0.9962,	0.9988,	0.9999,	1.0000,	1.0000,	1.0001,	0.9997,	0.9983,	0.9955,	0.9917,	0.9871,	0.9810,	0.9719,	0.9601,	0.9456,	0.9275,	0.9054,	0.8768,	0.8400,	0.7910,	0.7270,	0.6520,	0.6030],	
    [25.0,	0.6535,	0.6920,	0.7516,	0.8065,	0.8492,	0.8809,	0.9066,	0.9282,	0.9492,	0.9624,	0.9696,	0.9778,	0.9854,	0.9914,	0.9957,	0.9985,	0.9999,	1.0003,	1.0000,	0.9998,	0.9995,	0.9982,	0.9956,	0.9920,	0.9875,	0.9818,	0.9740,	0.9630,	0.9487,	0.9312,	0.9093,	0.8805,	0.8433,	0.7959,	0.7341,	0.6606,	0.6130],	
    [30.0,	0.6600,	0.7000,	0.7580,	0.8122,	0.8540,	0.8820,	0.9060,	0.9296,	0.9497,	0.9634,	0.9723,	0.9794,	0.9852,	0.9902,	0.9941,	0.9970,	0.9989,	0.9998,	1.0000,	1.0004,	1.0006,	0.9992,	0.9960,	0.9917,	0.9872,	0.9828,	0.9779,	0.9679,	0.9532,	0.9366,	0.9150,	0.8857,	0.8472,	0.8010,	0.7420,	0.6720,	0.6220],	
    [35.0,	0.6676,	0.7084,	0.7642,	0.8175,	0.8587,	0.8837,	0.9062,	0.9303,	0.9497,	0.9636,	0.9733,	0.9797,	0.9845,	0.9885,	0.9920,	0.9951,	0.9979,	0.9996,	1.0000,	1.0005,	1.0007,	0.9992,	0.9954,	0.9908,	0.9865,	0.9831,	0.9799,	0.9708,	0.9557,	0.9394,	0.9186,	0.8893,	0.8501,	0.8055,	0.7499,	0.6822,	0.6314],	
    [40.0,	0.6765,	0.7170,	0.7703,	0.8222,	0.8631,	0.8859,	0.9073,	0.9304,	0.9494,	0.9630,	0.9725,	0.9789,	0.9832,	0.9864,	0.9893,	0.9929,	0.9969,	0.9998,	1.0000,	0.9999,	0.9998,	0.9979,	0.9940,	0.9893,	0.9854,	0.9827,	0.9800,	0.9713,	0.9559,	0.9394,	0.9200,	0.8912,	0.8520,	0.8094,	0.7579,	0.6910,	0.6414],	
    [45.0,	0.6862,	0.7259,	0.7762,	0.8266,	0.8674,	0.8885,	0.9090,	0.9300,	0.9488,	0.9619,	0.9705,	0.9771,	0.9814,	0.9839,	0.9862,	0.9903,	0.9959,	1.0001,	1.0000,	0.9990,	0.9982,	0.9959,	0.9918,	0.9873,	0.9840,	0.9818,	0.9789,	0.9704,	0.9545,	0.9375,	0.9199,	0.8920,	0.8533,	0.8128,	0.7659,	0.6990,	0.6517],	
    [50.0,	0.6960,	0.7350,	0.7820,	0.8309,	0.8720,	0.8915,	0.9110,	0.9293,	0.9478,	0.9604,	0.9680,	0.9749,	0.9793,	0.9810,	0.9827,	0.9874,	0.9947,	1.0004,	1.0000,	0.9980,	0.9964,	0.9936,	0.9893,	0.9849,	0.9822,	0.9806,	0.9772,	0.9688,	0.9525,	0.9347,	0.9191,	0.8924,	0.8541,	0.8160,	0.7740,	0.7070,	0.6620]],
    columns=['r(mm)\\theta(°)', '0',	'5',	'10',	'15',	'20',	'25',	'30',	'35',	'40',	'45',	'50',	'55',	'60',	'65',	'70',	'75',	'80',	'85',	'90',	'95',	'100',	'105',	'110',	'115',	'120',	'125',	'130',	'135',	'140',	'145',	'150',	'155',	'160',	'165',	'170',	'175',	'180']
    )
    Anisotropy2D = Anisotropy2D.drop('r(mm)\\theta(°)',axis=1)

    # g(r)
    #r(mm) g(r)
    RadialDoseFuntion = pd.DataFrame([[0.0,	1.0080	],
    [5.0,	1.0000	],
    [10.0,	1.0000	],
    [15.0,	1.0030	],
    [20.0,	1.0070	],
    [25.0,	1.0080	],
    [30.0,	1.0080	],
    [35.0,	1.0067	],
    [40.0,	1.0040	],
    [45.0,	1.0002	],
    [50.0,	0.9950	],
    [55.0,	0.9884	],
    [60.0,	0.9810	],
    [65.0,	0.9732	],
    [70.0,	0.9640	],
    [75.0,	0.9527	],
    [80.0,	0.9400	],
    [85.0,	0.9268	],
    [90.0,	0.9130	],
    [95.0,	0.8982	],
    [100.0,	0.8820],	
    [105.0,	0.8639],	
    [110.0,	0.8440],	
    [115.0,	0.8222],	
    [120.0,	0.7990],	
    [125.0,	0.7743],	
    [130.0,	0.7470],	
    [135.0,	0.7158],	
    [140.0,	0.6810]],columns=['r(mm)','g(r)'])
    
    
    self.Activity=Activity
    self.DoseRateConstant=DoseRateConstant
    self.Anisotropy2D=Anisotropy2D
    self.RadialDoseFuntion=RadialDoseFuntion
    self.length=length
    self.RAKR=RAKR
    self.CalDate=CalDate
    self.MeanLife=MeanLife