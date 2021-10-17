import sys
import pydicom
from datetime import datetime


from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QDialog,
    QMainWindow,
    QApplication,
    QWidget,
    QFileDialog
)

from PandasModel import PandasModel
from tg43.Extraction import Extraction
from tg43.validation import validation

class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi('mainscreen.ui',self)
        self.pushButton.clicked.connect(self.dcm_input)

        self.dcm_input = dcm_input_Screen()

    def dcm_input(self):
        self.dcm_input.show()

class dcm_input_Screen(QDialog):
    def __init__(self):
        super(dcm_input_Screen,self).__init__()
        loadUi('dcm_input.ui',self)

        self.browseButton.clicked.connect(self.browsefiles)
        self.calculate_button.clicked.connect(self.getValues)

    def getValues(self):
        RAKR = int(self.lineRAKR.text())
        CalDate = self.dateTimeEdit.dateTime().toPyDateTime()
        fname = self.file_name.text()
        RT_Plan = pydicom.dcmread(fname)

        result = validation(RAKR,CalDate,RT_Plan)

        self.results_screen = results_Screen(result,fname)
        self.results_screen.show()

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file')
        
        self.file_name.setText(fname[0])
        RT_Plan = pydicom.dcmread(fname[0])
        print(type(fname))
        print(Extraction(pydicom.dcmread(fname[0])))

        return RT_Plan

class results_Screen(QDialog):
    def __init__(self,result,fname):
        super(results_Screen,self).__init__()
        self.result = result
        self.fname = fname
        patient = pydicom.dcmread(fname)
        
        model = PandasModel(result)
        loadUi('results.ui',self)

        self.tableView.setModel(model)
        self.label_4.setText(str(patient.PatientName))

app = QApplication(sys.argv)
mainscreen = MainScreen()
mainscreen.show()
sys.exit(app.exec())