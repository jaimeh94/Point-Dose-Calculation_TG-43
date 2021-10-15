import pydicom
import numpy as np
import pandas as pd
from Iridium192 import Ir_192
from Dose import Dose
from datetime import datetime
from Extraction import Extraction

def validation(RAKR,CalDate,RT_Plan):
  fuente = Ir_192(CalDate=CalDate, RAKR=RAKR)

  Catheters, Calc_Matrix, PlanDate, IcruDosePoints = Extraction(RT_Plan)

  Dosis = Dose(Catheters,Calc_Matrix,fuente,PlanDate)

  Puntos = IcruDosePoints
  Puntos['Manual'] = Dosis

  Puntos['Error(%)'] = round(100*(Puntos.Plan - Puntos.Manual)/Puntos.Manual,2)

  return Puntos