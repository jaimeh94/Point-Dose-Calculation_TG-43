from Iridium192 import Source
from Iridium192 import Ir_192
import pandas as pd
import numpy as np
from scipy import interpolate
from datetime import datetime
# Ir = Source()
# print(Ir.length)

fuente = Ir_192
# print(Ir.length)

Position=pd.DataFrame(([[0,0,0],[1,0,0],[2,0,0]]),columns=['x','y','z'])
calc_point=np.array([2,2,2])

PlanDate = datetime(2021,1,21,8,30)

def Dose_Rate(Position,calc_point,fuente,PlanDate):
    deltaPlanCal = (PlanDate-fuente.CalDate).days + (PlanDate-fuente.CalDate).seconds/(24*3600)

    Sk = fuente.RAKR*np.exp(-np.log(2)*deltaPlanCal/fuente.MeanLife)
    r = calc_point-Position
    a = pd.DataFrame([Position.loc[i,['x','y','z']] - Position.loc[i+1,['x','y','z']] if i!=len(Position)-1 else Position.loc[i-1,['x','y','z']] - Position.loc[i,['x','y','z']] for i in range(len(Position))]) 
    r_dot_a=[r.iloc[i].dot(a.iloc[i]) for i in range(len(r))]
    r['modulo_r'] = r.apply(lambda x:np.linalg.norm(x), axis='columns')
    a['modulo_a'] = a.apply(lambda x:np.linalg.norm(x), axis='columns')

    theta = [np.degrees(np.arccos(r_dot_a[i]/(r.modulo_r[i]*a.modulo_a[i]))) for i in range(len(r_dot_a))]

    a_norm = a[['x','y','z']].apply(lambda x:x/np.linalg.norm(x), axis='columns')

    r1 = calc_point - (Position - a_norm*fuente.length/20)
    r1_dot_a=[r1.iloc[i].dot(a[['x','y','z']].iloc[i]) for i in range(len(r1))]
    r1['modulo_r1'] = r1.apply(lambda x:np.linalg.norm(x), axis='columns')
    theta_1 = np.array([np.degrees(np.arccos(r1_dot_a[i]/(r1.modulo_r1[i]*a.modulo_a[i]))) for i in range(len(r1_dot_a))])

    r2 = calc_point - (Position + a_norm*fuente.length/20)
    r2_dot_a=[r2.iloc[i].dot(a[['x','y','z']].iloc[i]) for i in range(len(r2))]
    r2['modulo_r2'] = r2.apply(lambda x:np.linalg.norm(x), axis='columns')
    theta_2 = np.array([np.degrees(np.arccos(r2_dot_a[i]/(r2.modulo_r2[i]*a.modulo_a[i]))) for i in range(len(r2_dot_a))])

    beta = np.radians(theta_2 - theta_1)

    GL0 = 2*np.arctan(fuente.length/20)/(fuente.length/10)
    GL_r_th = np.array([1/(r.modulo_r[i]**2-(fuente.length/20)**2) if (theta[i]==0 or theta[i]==180) else beta[i]/((fuente.length/10)*r.modulo_r[i]*np.sin(np.radians(theta[i]))) for i in range(len(beta))])

    g_r = np.interp(r.modulo_r*10,fuente.RadialDoseFuntion['r(mm)'],fuente.RadialDoseFuntion['g(r)'])

    x,y = np.meshgrid(np.linspace(0,180,37),np.linspace(0,50,11))
    # Anisotropy2D.drop('r(mm)\\theta(°)',axis=1)
    f = interpolate.interp2d(x,y,np.array(fuente.Anisotropy2D),kind='cubic')

    F_r_th = np.array([(f(theta[i],r.modulo_r[i]*10))[0] for i in range(len(r))])
    
    return Sk*fuente.DoseRateConstant*(GL_r_th/GL0)*g_r*F_r_th.T

DR = Dose_Rate(Position,calc_point,fuente,PlanDate)




def Dose(Catheters, Calc_Matrix, fuente, PlanDate):
    """
    This funtion return a matrix of dose in the space
    """
    DoseperMatrix=[]
    for calc_point in Calc_Matrix:
        DoseperCatheter=[]
        for Position in Catheters:
            DoseRate=Dose_Rate(Position[['x','y','z']],calc_point,fuente,PlanDate)
            DoseperDwell = DoseRate*np.array(Position['time']/3600)
            DoseperCatheter.append(DoseperDwell.sum())
        DoseperCatheter = np.array(DoseperCatheter)
        DoseperMatrix.append(DoseperCatheter.sum())
    return DoseperMatrix

print(DR)