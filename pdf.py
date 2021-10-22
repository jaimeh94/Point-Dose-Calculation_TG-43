from fpdf import FPDF  # fpdf class
from datetime import datetime
import pydicom
import os

def inform(RT_Plan,result,CalDate,RAKR):
  # save FPDF() class into a 
  # variable pdf
  pdf = FPDF(format='Letter')


  # Add a page
  pdf.add_page()
    
  # set style and size of font 
  # that you want in the pdf
  pdf.set_font("Arial", size = 15, style='B')
  pdf.cell(200, 20, txt = "",
          ln = 2, align = 'C')
  # create a cell
  pdf.cell(200, 5, txt = "CALCULO MANUAL DE DOSIS EN BRAQUITERAPIA USANDO", 
          ln = 1, align = 'C')
    
  # add another cell
  pdf.cell(200, 5, txt = "EL PROTOCOLO TG-43 DE LA AAMP",
          ln = 2, align = 'C')
  pdf.cell(200, 10, txt = "",
          ln = 2, align = 'C')

  pdf.set_font("Arial", size = 12, style='B')
  # add another cell
  pdf.cell(200, 5, txt = "DATOS DE LA FUENTE:",
          ln = 2, align = 'L')

  pdf.set_font("Arial", size = 12)
  pdf.cell(100, 5, txt = "Radionucleido: ",
          ln = 0, align = 'L')
  pdf.cell(20, 5, txt = "Ir-192",
          ln = 1, align = 'L')

  pdf.cell(100, 5, txt = "Fecha de Calibracion: ",
          ln = 0, align = 'L')
  pdf.cell(200, 5, txt = str(CalDate),
          ln = 1, align = 'L')

  pdf.cell(100, 5, txt = "RAKR: ",
          ln = 0, align = 'L')
  pdf.cell(200, 5, txt = str(RAKR),
          ln = 1, align = 'L')

  pdf.cell(200, 5, txt = "",
          ln = 2, align = 'C')

  pdf.set_font("Arial", size = 12, style='B')
  # add another cell
  pdf.cell(200, 5, txt = "DATOS DEL PACIENTE:",
          ln = 2, align = 'L')

  pdf.set_font("Arial", size = 12)
  pdf.cell(100, 5, txt = "Nombre: ",
          ln = 0, align = 'L')
  pdf.cell(20, 5, txt = str(RT_Plan.PatientName),
          ln = 1, align = 'L')

  pdf.cell(100, 5, txt = "ID: ",
          ln = 0, align = 'L')
  pdf.cell(20, 10, txt = str(RT_Plan.PatientID),
          ln = 1, align = 'L')

  pdf.cell(200, 5, txt = "",
          ln = 2, align = 'C')

  pdf.set_font("Arial", size = 12, style='B')
  # add another cell
  pdf.cell(200, 5, txt = "DATOS DEL PLAN DE TRTAMIENTO:",
          ln = 2, align = 'L')

  pdf.set_font("Arial", size = 12)
  pdf.cell(100, 5, txt = "Fecha de planificacion: ",
          ln = 0, align = 'L')
  pdf.cell(20, 5, txt = str(RT_Plan.SourceSequence[0].SourceStrengthReferenceDate),
          ln = 1, align = 'L')

  pdf.cell(100, 5, txt = "Numero de canales: ",
          ln = 0, align = 'L')
  pdf.cell(20, 5, txt = str(len(RT_Plan.ApplicationSetupSequence[0].ChannelSequence)),
          ln = 1, align = 'L')

  # pdf.cell(100, 5, txt = "Posiciones de la fuente: ",
  #         ln = 0, align = 'L')
  # pdf.cell(20, 5, txt = "Ir-192",
  #         ln = 1, align = 'L')

  pdf.cell(200, 5, txt = "",
          ln = 2, align = 'C')

  pdf.set_font("Arial", size = 12, style='B')
  # add another cell
  pdf.cell(200, 5, txt = "RESULTADOS COMPARATIVOS:",
          ln = 2, align = 'C')

  for col in result.columns:
    th=0
    if col == result.columns[-1]:
      th=1
    pdf.cell(50, 5, txt = col,
            ln = th, align = 'C', border=1)
  pdf.set_font("Arial", size = 12)
  for i in range(result.shape[0]):
    # print(i)
    for j in range(result.shape[1]):
      # print(df.loc[i,j])
      th=0
      if j == result.shape[1]-1:
        th=1
      pdf.cell(50, 5, txt = str(result.iloc[i,j]), ln = th, align = 'C', border=1)

  # save the pdf with name .pdf
  pdf.output("%s.pdf" % str(RT_Plan.PatientID))   