# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plotOptions = QtWidgets.QStackedWidget(self.centralwidget)
        self.plotOptions.setGeometry(QtCore.QRect(10, 80, 241, 471))
        self.plotOptions.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plotOptions.setObjectName("plotOptions")
        self.lineOptions = QtWidgets.QWidget()
        self.lineOptions.setObjectName("lineOptions")
        self.l_xAxis = QtWidgets.QComboBox(self.lineOptions)
        self.l_xAxis.setGeometry(QtCore.QRect(10, 40, 211, 22))
        self.l_xAxis.setObjectName("l_xAxis")
        self.l_yAxis = QtWidgets.QComboBox(self.lineOptions)
        self.l_yAxis.setGeometry(QtCore.QRect(10, 100, 211, 22))
        self.l_yAxis.setObjectName("l_yAxis")
        self.l_graphs = QtWidgets.QListWidget(self.lineOptions)
        self.l_graphs.setGeometry(QtCore.QRect(10, 200, 211, 251))
        self.l_graphs.setObjectName("l_graphs")
        self._l_xlabel = QtWidgets.QLabel(self.lineOptions)
        self._l_xlabel.setGeometry(QtCore.QRect(10, 20, 211, 16))
        self._l_xlabel.setObjectName("_l_xlabel")
        self._l_ylabel = QtWidgets.QLabel(self.lineOptions)
        self._l_ylabel.setGeometry(QtCore.QRect(10, 80, 211, 16))
        self._l_ylabel.setObjectName("_l_ylabel")
        self._l_colabel = QtWidgets.QLabel(self.lineOptions)
        self._l_colabel.setGeometry(QtCore.QRect(10, 150, 211, 16))
        self._l_colabel.setObjectName("_l_colabel")
        self.l_column = QtWidgets.QComboBox(self.lineOptions)
        self.l_column.setGeometry(QtCore.QRect(10, 170, 211, 22))
        self.l_column.setObjectName("l_column")
        self.plotOptions.addWidget(self.lineOptions)
        self.pieOptions = QtWidgets.QWidget()
        self.pieOptions.setObjectName("pieOptions")
        self.p_label = QtWidgets.QComboBox(self.pieOptions)
        self.p_label.setGeometry(QtCore.QRect(10, 40, 211, 22))
        self.p_label.setObjectName("p_label")
        self._p_datlabel = QtWidgets.QLabel(self.pieOptions)
        self._p_datlabel.setGeometry(QtCore.QRect(10, 20, 211, 16))
        self._p_datlabel.setObjectName("_p_datlabel")
        self.p_include = QtWidgets.QListWidget(self.pieOptions)
        self.p_include.setGeometry(QtCore.QRect(10, 140, 211, 121))
        self.p_include.setObjectName("p_include")
        self._p_colabel = QtWidgets.QLabel(self.pieOptions)
        self._p_colabel.setGeometry(QtCore.QRect(10, 120, 211, 16))
        self._p_colabel.setObjectName("_p_colabel")
        self._p_filabel = QtWidgets.QLabel(self.pieOptions)
        self._p_filabel.setGeometry(QtCore.QRect(10, 270, 211, 16))
        self._p_filabel.setObjectName("_p_filabel")
        self.p_filtered = QtWidgets.QListWidget(self.pieOptions)
        self.p_filtered.setGeometry(QtCore.QRect(10, 320, 211, 141))
        self.p_filtered.setObjectName("p_filtered")
        self.p_filter = QtWidgets.QComboBox(self.pieOptions)
        self.p_filter.setGeometry(QtCore.QRect(10, 290, 211, 22))
        self.p_filter.setObjectName("p_filter")
        self._p_datlabel_2 = QtWidgets.QLabel(self.pieOptions)
        self._p_datlabel_2.setGeometry(QtCore.QRect(10, 70, 211, 16))
        self._p_datlabel_2.setObjectName("_p_datlabel_2")
        self.p_value = QtWidgets.QComboBox(self.pieOptions)
        self.p_value.setGeometry(QtCore.QRect(10, 90, 211, 22))
        self.p_value.setObjectName("p_value")
        self.plotOptions.addWidget(self.pieOptions)
        self.barOptions = QtWidgets.QWidget()
        self.barOptions.setObjectName("barOptions")
        self.b_value = QtWidgets.QComboBox(self.barOptions)
        self.b_value.setGeometry(QtCore.QRect(10, 90, 211, 22))
        self.b_value.setObjectName("b_value")
        self.b_inlabels = QtWidgets.QListWidget(self.barOptions)
        self.b_inlabels.setGeometry(QtCore.QRect(10, 200, 211, 101))
        self.b_inlabels.setObjectName("b_inlabels")
        self._b_valabel = QtWidgets.QLabel(self.barOptions)
        self._b_valabel.setGeometry(QtCore.QRect(10, 70, 211, 16))
        self._b_valabel.setObjectName("_b_valabel")
        self._b_label = QtWidgets.QLabel(self.barOptions)
        self._b_label.setGeometry(QtCore.QRect(10, 20, 211, 16))
        self._b_label.setObjectName("_b_label")
        self.b_label = QtWidgets.QComboBox(self.barOptions)
        self.b_label.setGeometry(QtCore.QRect(10, 40, 211, 22))
        self.b_label.setObjectName("b_label")
        self.b_orient = QtWidgets.QComboBox(self.barOptions)
        self.b_orient.setGeometry(QtCore.QRect(10, 140, 211, 22))
        self.b_orient.setObjectName("b_orient")
        self.b_orient.addItem("")
        self.b_orient.addItem("")
        self._b_orilabel = QtWidgets.QLabel(self.barOptions)
        self._b_orilabel.setGeometry(QtCore.QRect(10, 120, 211, 16))
        self._b_orilabel.setObjectName("_b_orilabel")
        self._b_inlabel = QtWidgets.QLabel(self.barOptions)
        self._b_inlabel.setGeometry(QtCore.QRect(10, 180, 211, 16))
        self._b_inlabel.setObjectName("_b_inlabel")
        self._b_fillabel = QtWidgets.QLabel(self.barOptions)
        self._b_fillabel.setGeometry(QtCore.QRect(10, 320, 211, 16))
        self._b_fillabel.setObjectName("_b_fillabel")
        self.b_filtered = QtWidgets.QListWidget(self.barOptions)
        self.b_filtered.setGeometry(QtCore.QRect(10, 370, 211, 91))
        self.b_filtered.setObjectName("b_filtered")
        self.b_filter = QtWidgets.QComboBox(self.barOptions)
        self.b_filter.setGeometry(QtCore.QRect(10, 340, 211, 22))
        self.b_filter.setObjectName("b_filter")
        self.plotOptions.addWidget(self.barOptions)
        self.plotType = QtWidgets.QComboBox(self.centralwidget)
        self.plotType.setGeometry(QtCore.QRect(10, 30, 241, 22))
        self.plotType.setObjectName("plotType")
        self.plotType.addItem("")
        self.plotType.addItem("")
        self.plotType.addItem("")
        self.plotView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.plotView.setGeometry(QtCore.QRect(270, 70, 511, 351))
        self.plotView.setObjectName("plotView")
        self.plotTitle = QtWidgets.QLineEdit(self.centralwidget)
        self.plotTitle.setGeometry(QtCore.QRect(290, 440, 391, 20))
        self.plotTitle.setInputMask("")
        self.plotTitle.setText("")
        self.plotTitle.setMaxLength(32767)
        self.plotTitle.setFrame(True)
        self.plotTitle.setObjectName("plotTitle")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 16))
        self.label.setObjectName("label")
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setGeometry(QtCore.QRect(710, 440, 75, 23))
        self.applyButton.setObjectName("applyButton")
        self.xAxisLabel = QtWidgets.QLineEdit(self.centralwidget)
        self.xAxisLabel.setGeometry(QtCore.QRect(290, 470, 191, 20))
        self.xAxisLabel.setInputMask("")
        self.xAxisLabel.setText("")
        self.xAxisLabel.setMaxLength(32767)
        self.xAxisLabel.setFrame(True)
        self.xAxisLabel.setObjectName("xAxisLabel")
        self.yAxisLabel = QtWidgets.QLineEdit(self.centralwidget)
        self.yAxisLabel.setGeometry(QtCore.QRect(490, 470, 191, 20))
        self.yAxisLabel.setInputMask("")
        self.yAxisLabel.setText("")
        self.yAxisLabel.setMaxLength(32767)
        self.yAxisLabel.setFrame(True)
        self.yAxisLabel.setObjectName("yAxisLabel")
        self.legendLabel = QtWidgets.QLineEdit(self.centralwidget)
        self.legendLabel.setGeometry(QtCore.QRect(490, 530, 191, 20))
        self.legendLabel.setInputMask("")
        self.legendLabel.setText("")
        self.legendLabel.setMaxLength(32767)
        self.legendLabel.setFrame(True)
        self.legendLabel.setObjectName("legendLabel")
        self.width = QtWidgets.QSpinBox(self.centralwidget)
        self.width.setGeometry(QtCore.QRect(290, 530, 91, 22))
        self.width.setMinimum(0)
        self.width.setMaximum(5000)
        self.width.setProperty("value", 700)
        self.width.setObjectName("width")
        self.height = QtWidgets.QSpinBox(self.centralwidget)
        self.height.setGeometry(QtCore.QRect(390, 530, 91, 22))
        self.height.setSuffix("")
        self.height.setPrefix("")
        self.height.setMaximum(5000)
        self.height.setProperty("value", 500)
        self.height.setObjectName("height")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 510, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(390, 510, 47, 13))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.newFile = QtWidgets.QAction(MainWindow)
        self.newFile.setObjectName("newFile")
        self.saveFile = QtWidgets.QAction(MainWindow)
        self.saveFile.setObjectName("saveFile")
        self.menuFile.addAction(self.newFile)
        self.menuFile.addAction(self.saveFile)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.plotOptions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self._l_xlabel.setText(_translate("MainWindow", "X Axis"))
        self._l_ylabel.setText(_translate("MainWindow", "Y Axis"))
        self._l_colabel.setText(_translate("MainWindow", "Column to plot"))
        self._p_datlabel.setText(_translate("MainWindow", "Label"))
        self._p_colabel.setText(_translate("MainWindow", "Labels to include:"))
        self._p_filabel.setText(_translate("MainWindow", "Filter"))
        self._p_datlabel_2.setText(_translate("MainWindow", "Value"))
        self._b_valabel.setText(_translate("MainWindow", "Value Axis"))
        self._b_label.setText(_translate("MainWindow", "Label Axis"))
        self.b_orient.setItemText(0, _translate("MainWindow", "Vertical"))
        self.b_orient.setItemText(1, _translate("MainWindow", "Horisontal"))
        self._b_orilabel.setText(_translate("MainWindow", "Orientation"))
        self._b_inlabel.setText(_translate("MainWindow", "Included Labels"))
        self._b_fillabel.setText(_translate("MainWindow", "Filter based on column"))
        self.plotType.setItemText(0, _translate("MainWindow", "Line"))
        self.plotType.setItemText(1, _translate("MainWindow", "Pie"))
        self.plotType.setItemText(2, _translate("MainWindow", "Bar"))
        self.plotTitle.setPlaceholderText(_translate("MainWindow", "Plot Title"))
        self.label.setText(_translate("MainWindow", "Plot Type"))
        self.applyButton.setText(_translate("MainWindow", "Apply"))
        self.xAxisLabel.setPlaceholderText(_translate("MainWindow", "X Axis Label (If Applicable)"))
        self.yAxisLabel.setPlaceholderText(_translate("MainWindow", "Y Axis Label (If Applicable)"))
        self.legendLabel.setPlaceholderText(_translate("MainWindow", "Legend Title"))
        self.label_2.setText(_translate("MainWindow", "Width"))
        self.label_3.setText(_translate("MainWindow", "Height"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.newFile.setText(_translate("MainWindow", "New"))
        self.saveFile.setText(_translate("MainWindow", "Save As"))
from PyQt5 import QtWebEngineWidgets