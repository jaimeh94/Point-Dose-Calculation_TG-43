import pydicom
import numpy as np
import pandas as pd
from tg43.Iridium192 import Ir_192
from tg43.Dose import Dose
from datetime import datetime

def Extraction(RT_Plan):
  import pydicom
  import numpy as np
  import pandas as pd
  from datetime import datetime

  Catheters=list()
  for j in range(len(RT_Plan.ApplicationSetupSequence[0].ChannelSequence)):
    total_time = RT_Plan.ApplicationSetupSequence[0].ChannelSequence[j].ChannelTotalTime
    total_time_weight = RT_Plan.ApplicationSetupSequence[0].ChannelSequence[j].FinalCumulativeTimeWeight

    Catheter = RT_Plan.ApplicationSetupSequence[0].ChannelSequence[j].BrachyControlPointSequence
    cum_time=0
    time_dwell=0
    Position=[]
    for i in range(len(Catheter)):
        raw_time_dwell = Catheter[i].CumulativeTimeWeight - cum_time
        cum_time = Catheter[i].CumulativeTimeWeight
                
        if raw_time_dwell != 0:
          dwell = Catheter[i].ControlPoint3DPosition
          time_dwell=round(10*raw_time_dwell*total_time/total_time_weight,2)
          dwell.append(time_dwell)
          Position.append(np.array(dwell)/10)

    Position = pd.DataFrame(Position,columns=['x','y','z','time'])
    Catheters.append(Position)

  
  points = RT_Plan.DoseReferenceSequence
  Calc_Matrix=[]
  for k in range(len(points)):
    calc_point = np.array(points[k].DoseReferencePointCoordinates)/10
    Calc_Matrix.append(calc_point)

  IcruDosePoints = pd.DataFrame([(x.DoseReferenceDescription,round(100*float(x.TargetPrescriptionDose),2)) for x in points], columns=['Points','Plan (cGy)'])

  rawPlanDate = RT_Plan.SourceSequence[0].SourceStrengthReferenceDate
  rawPlanTime = RT_Plan.SourceSequence[0].SourceStrengthReferenceTime

  PlanDate = datetime(int(rawPlanDate[:4]),int(rawPlanDate[4:6]),int(rawPlanDate[6:8]),int(rawPlanTime[:2]),int(rawPlanTime[2:4]))

  return (Catheters,Calc_Matrix, PlanDate, IcruDosePoints)