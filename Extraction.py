import pydicom
import numpy as np
import pandas as pd
from Iridium192 import Ir_192
from Dose import Dose
from datetime import datetime

RT_Plan = pydicom.dcmread('./Martha Altamar BQT/RP.1.3.6.1.4.1.2452.6.1116510183.1322412770.3776939407.874610829.dcm')

total_time = RT_Plan.ApplicationSetupSequence[0].ChannelSequence[0].ChannelTotalTime
total_time_weight = RT_Plan.ApplicationSetupSequence[0].ChannelSequence[0].FinalCumulativeTimeWeight

Catheter = RT_Plan.ApplicationSetupSequence[0].ChannelSequence[0].BrachyControlPointSequence
cum_time=0
time_dwell=0
Position=[]
for i in range(len(Catheter)):
    if i%2==1:
        raw_time_dwell = Catheter[i].CumulativeTimeWeight - cum_time
        dwell = Catheter[i].ControlPoint3DPosition
        cum_time = Catheter[i].CumulativeTimeWeight
        time_dwell=round(10*raw_time_dwell*total_time/total_time_weight,2)
        
        dwell.append(time_dwell)
        Position.append(np.array(dwell)/10)

Position = pd.DataFrame(Position,columns=['x','y','z','time'])

points = RT_Plan.DoseReferenceSequence

calc_point = np.array(points[3].DoseReferencePointCoordinates)/10

fuente = Ir_192(CalDate=datetime(2021,4,22,5,22), RAKR=52570)

rawPlanDate = RT_Plan.SourceSequence[0].SourceStrengthReferenceDate
rawPlanTime = RT_Plan.SourceSequence[0].SourceStrengthReferenceTime

PlanDate = datetime(int(rawPlanDate[:4]),int(rawPlanDate[4:6]),int(rawPlanDate[6:8]),int(rawPlanTime[:2]),int(rawPlanTime[2:4]))

Dosis = Dose([Position],[calc_point],fuente,PlanDate)

print(Dosis)
