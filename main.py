import sys
from PyQt5 import QtCore, QtWidgets
from main_window import Ui_MainWindow
from plotter import Plotter, PlotParameters
from functools import partial
import traceback

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plotter = None

        self.setWindowTitle("CSV Grapher")

        self.ui.newFile.triggered.connect(partial(self.error_handle, self.load_data, "Error encountered while loading file"))
        self.ui.saveFile.triggered.connect(partial(self.error_handle, self.save_figure, "Error encountered while saving file"))

        self.ui.plotType.currentTextChanged.connect(self.change_ptype)

        self.ui.l_column.currentTextChanged.connect(partial(self.update_column_graphs, self.ui.l_graphs, self.ui.l_column))
        self.ui.l_column.currentTextChanged.connect(partial(self.update_text_edit, self.ui.legendLabel, self.ui.l_column))

        self.ui.p_label.currentTextChanged.connect(partial(self.update_column_graphs, self.ui.p_include, self.ui.p_label))
        self.ui.p_label.currentTextChanged.connect(partial(self.update_text_edit, self.ui.legendLabel, self.ui.p_label))
        self.ui.p_filter.currentTextChanged.connect(partial(self.update_column_graphs, self.ui.p_filtered, self.ui.p_filter))

        self.ui.b_label.currentTextChanged.connect(partial(self.update_column_graphs, self.ui.b_inlabels, self.ui.b_label))
        self.ui.b_filter.currentTextChanged.connect(partial(self.update_column_graphs, self.ui.b_filtered, self.ui.b_filter))
        self.ui.b_filter.currentTextChanged.connect(partial(self.update_text_edit, self.ui.legendLabel, self.ui.b_filter))

        self.ui.l_xAxis.currentTextChanged.connect(partial(self.update_text_edit, self.ui.xAxisLabel, self.ui.l_xAxis))
        self.ui.l_yAxis.currentTextChanged.connect(partial(self.update_text_edit, self.ui.yAxisLabel, self.ui.l_yAxis))

        self.ui.b_label.currentTextChanged.connect(partial(self.update_text_edit, self.ui.xAxisLabel, self.ui.b_label))
        self.ui.b_value.currentTextChanged.connect(partial(self.update_text_edit, self.ui.yAxisLabel, self.ui.b_value))


        self.ui.applyButton.clicked.connect(partial(self.error_handle, self.apply_to_preview, "Error applying plot to preview"))
        

    def load_data(self):
        f, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Project Data", "", "CSV (*.csv)")
        if f:
            self.clear_all()
            self.plotter = Plotter(f)
            self.set_options()
    
    def clear_all(self):
        to_clear = ["l_xAxis", "l_yAxis", "l_column", "l_graphs" ,
                    "p_label" ,"p_value", "p_include", "p_filter", "p_filtered", 
                    "b_label", "b_value" ,"b_inlabels", "b_filter", "b_filtered"]

        for w in to_clear:
            eval(f"self.ui.{w}.clear()")

    def set_options(self):
        # Line
        cols = self.plotter.get_columns()
        self.ui.l_xAxis.addItems(cols)
        self.ui.l_yAxis.addItems(cols)
        self.ui.l_column.addItems(cols)

        # Pie
        self.ui.p_label.addItems(cols)
        self.ui.p_value.addItems(cols)
        self.ui.p_filter.addItems(cols)

        # Bar
        self.ui.b_label.addItems(cols)
        self.ui.b_value.addItems(cols)
        self.ui.b_filter.addItems(cols)

    def update_text_edit(self, field: QtWidgets.QTextEdit, value: QtWidgets.QComboBox):
        field.setText(value.currentText())

    def change_ptype(self):
        curr = self.ui.plotType.currentText()
        if self.plotter:
            self.plotter.plot_type = curr

        match curr:
            case "Line":
                self.ui.plotOptions.setCurrentIndex(0)
                self.update_column_graphs(self.ui.l_graphs, self.ui.l_column)
            case "Pie":
                self.ui.plotOptions.setCurrentIndex(1)
                self.update_column_graphs(self.ui.p_include, self.ui.p_label)
                self.update_column_graphs(self.ui.p_filtered, self.ui.p_filter)
            case "Bar":
                self.ui.plotOptions.setCurrentIndex(2)
                self.update_column_graphs(self.ui.b_inlabels, self.ui.b_label)
                self.update_column_graphs(self.ui.b_filtered, self.ui.b_filter)

    def update_column_graphs(self, listview: QtWidgets.QListWidget, choice: QtWidgets.QComboBox):
        if self.plotter is None:
            return

        uniques = self.plotter.get_uniques_in(choice.currentText())

        listview.clear()
        for u in uniques:
            item = QtWidgets.QListWidgetItem(u)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            listview.addItem(item)

    def apply_to_preview(self, save=False):
        sui = self.ui
        params = PlotParameters(sui.xAxisLabel.text(), 
                                sui.yAxisLabel.text(),
                                sui.width.value() if save else 700,
                                sui.height.value() if save else 500,
                                sui.fontSize.value() if save else 14,
                                sui.legendLabel.text(), 
                                sui.plotTitle.text(),
                                sui.titlePosition.currentText(),
                                sui.xTicksFormat.currentText(),
                                sui.yTicksFormat.currentText(),
                                sui.b_legend.isChecked(),
                                sui.b_multicolor.isChecked())
        fig = None

        match self.ui.plotType.currentText():
            case "Line":
                xs, ys, cols = sui.l_xAxis.currentText(), sui.l_yAxis.currentText(), sui.l_column.currentText()
                colgraphs = []
                for i in range(sui.l_graphs.count()):
                    item = sui.l_graphs.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        colgraphs.append(item.text())
            
                fig = self.plotter.get_line_fig(xs, ys, cols, colgraphs, params)

            case "Pie":
                ls, vs, fs = sui.p_label.currentText(), sui.p_value.currentText(), sui.p_filter.currentText()

                includes = []
                for i in range(sui.p_include.count()):
                    item = sui.p_include.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        includes.append(item.text())

                filtered = []
                for i in range(sui.p_filtered.count()):
                    item = sui.p_filtered.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        filtered.append(item.text())

                fig = self.plotter.get_pie_fig(ls, vs, fs, includes, filtered, params)


            case "Bar":
                ls, vs, fs = sui.b_label.currentText(), sui.b_value.currentText(), sui.b_filter.currentText()
                ori = "v" if sui.b_orient.currentText() == "Vertical" else "h"
                colgraphs = []
                for i in range(sui.b_inlabels.count()):
                    item = sui.b_inlabels.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        colgraphs.append(item.text())

                filtered = []
                for i in range(sui.b_filtered.count()):
                    item = sui.b_filtered.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        filtered.append(item.text())
                    
                fig = self.plotter.get_bar_fig(ls, vs, fs, colgraphs, filtered, ori, params)
        if save:
            return fig
        else:
            self.ui.plotView.setHtml(fig.to_html(include_plotlyjs="cdn"))

    def save_figure(self):
        f, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", "", "EPS (*.eps);; PNG (*.png);; JPG (*.jpg);; SVG (*.svg)")
        
        if f:
            fig = self.apply_to_preview(True)
            fig.update_layout(width = self.ui.width.value(), height = self.ui.height.value(), font = dict(size = self.ui.fontSize.value()))
            fig.write_image(f)

    def display_error(self, short: str, detailed: str):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Close)
        msg.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Close)

        msg.setText(short)
        msg.setDetailedText(detailed)
        msg.exec_()

    def error_handle(self, func, error_msg: str):
        try:
            func()
        except Exception as e:
            self.display_error(error_msg, traceback.format_exc())


app = QtWidgets.QApplication(sys.argv)
w = AppWindow()
w.show()
app.exec()