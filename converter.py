from PyQt5 import QtCore, QtWidgets
from converter_window import Ui_MainWindow
import pandas as pd

class ConverterWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ConverterWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Wide To Long Converter")
        self.show()

        self.ui.actionOpen.triggered.connect(self.load_data)
        self.ui.actionSave_As.triggered.connect(self.save_data)

        self.data = None

    def load_data(self):
        f, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Project Data", "", "CSV (*.csv)")
        if f:
            self.ui.columns.clear()
            self.data = pd.read_csv(f)
            cols = self.data.columns

            add_to_list(cols, self.ui.columns)
            add_to_list(cols, self.ui.indices)

    def save_data(self):
        f, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", "", "CSV (*.csv)")
        
        if not f:
            return

        to_melt = []
        indices = []
        for i in range(self.ui.columns.count()):
            item = self.ui.columns.item(i)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                to_melt.append(item.text())

            item = self.ui.indices.item(i)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                indices.append(item.text())

        
        mdf = pd.melt(self.data, id_vars = indices, value_vars=to_melt).reset_index(drop = True)
        mdf.to_csv(f, index=False)

def add_to_list(add_list, qtlist):
    for c in add_list:
        item = QtWidgets.QListWidgetItem(c)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        qtlist.addItem(item)