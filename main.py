import sys
from PyQt5 import QtCore, QtWidgets
from main_window import Ui_MainWindow
from plotter import Plotter
from querier import Querier
from functools import partial
import traceback

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """# `AppWindow`
        Initialises the main application window.
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("CSV Grapher")

        self.connect_trigger(self.ui.newFile, self.load_data, "Error encountered while loading file")
        self.connect_trigger(self.ui.saveFile, self.save_figure, "Error encountered while saving file")

        self.connect_click(self.ui.applyButton, self.apply_to_preview, "Error applying plot to preview")

    def load_data(self):
        """# `load_data`
        Opens a file context for the user to open a .csv file from.
        When the file is chosen, it resets the window and sets up a new `Querier`
        """
        f, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Project Data", "", "CSV (*.csv)")
        if f:
            self.clear_all()
            self.querier = Querier(f)
            self.set_options()
    
    def clear_all(self):
        """# `clear_all`
        Clears all list views, combo boxes and text inputs
        """
        to_clear = ["columnSelect", "columnWhere", "columnCondSel", "currentConds",
                    "xAxis", "yAxis", "basedOn", "basedOnList",
                    "plotTitle", "xAxisLabel", "yAxisLabel", "legendLabel"]

        for widget in to_clear:
            eval(f"self.ui.{widget}.clear()")

    def set_options(self):
        """# `set_options`
        Sets up the window widgets, such as the combo boxes and list widgets with data from the imported .csv file
        """
        columns = self.querier.columns()
        self.ui.columnWhere.addItems(columns)
        self.ui.xAxis.addItems(columns)
        self.ui.yAxis.addItems(columns)
        self.ui.basedOn.addItems(["COLUMNS"] + columns)

        self.fill_lists(self.ui.columnSelect, columns)
        self.fill_lists(self.ui.basedOnList, columns)

    def fill_lists(self, widget: QtWidgets.QListWidget, values: list[str], check = True):
        """# `fill_lists`
        Given a `QListWidget` and a list of strings, fill the list widget with items from the list of strings
        ## Args:
            widget (QtWidgets.QListWidget): A PyQt ListWidget to add items to
            values (list[str]): A list of strings that will be added as items in the list widget
            check (bool, optional): If true then the items will have a checkbox as well. Defaults to True.
        """
        for value in values:
            item = QtWidgets.QListWidgetItem(value)
            if check:
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
            widget.addItem(item)

    def update_text_edit(self, field: QtWidgets.QTextEdit, value: QtWidgets.QComboBox):
        field.setText(value.currentText()) # TODO

    def change_ptype(self):
        pass # TODO

    def apply_to_preview(self, save=False):
        return # TODO
        if save:
            return fig
        else:
            self.ui.plotView.setHtml(fig.to_html(include_plotlyjs="cdn"))

    def save_figure(self):
        # TODO
        f, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", "", "EPS (*.eps);; PNG (*.png);; JPG (*.jpg);; SVG (*.svg)")
        
        if f:
            fig = self.apply_to_preview(True)
            fig.update_layout(width = self.ui.width.value(), height = self.ui.height.value(), font = dict(size = self.ui.fontSize.value()))
            fig.write_image(f)


    # === CONNECT BUTTONS AND TRIGGERES === 
    def connect_click(self, widget: QtWidgets.QWidget, function: callable, error_message: str = ""):
        """# `connect_click`
        Give a clickable widget a function to call when clicked. If any error occurs during that call display a given error message.

        ## Args:
            widget (QtWidgets.QWidget): The clickable widget to connect a function to
            function (callable): The function to call upon clicking the widget
            error_message (str, optional): The error message to display if an error occurs during the function call. Defaults to "".
        """
        widget.clicked.connect(partial(self.error_handle, function, error_message))

    def connect_trigger(self, widget: QtWidgets.QWidget, function: callable, error_message: str = ""):
        """# `connect_trigger`
        Give a triggerable widget a function to call when triggered. If any error occurs during that call display a given error message.
        
        ## Args:
            widget (QtWidgets.QWidget): The triggerable widget to connect a function to
            function (callable): The function to call upon triggering the widget
            error_message (str, optional): The error message to display if an error occurs during the function call. Defaults to "".
        """
        widget.triggered.connect(partial(self.error_handle, function, error_message))

    # === ERROR DISPLAYER ===
    def display_error(self, short: str, detailed: str):
        """# `display_error`
        Displays an error window with a short and a long description.

        ## Args:
            - `short (str)`: A short and concise description of the error
            - `detailed (str)`: A long description of the error, usually including the traceback
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Close)
        msg.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Close)

        msg.setText(short)
        msg.setDetailedText(detailed)
        msg.exec_()

    def error_handle(self, func: callable, error_message: str):
        """# `error_handle`
        Wrap a function in an error handler that displays a window showing a given error message that can be expanded to display the traceback.

        ## Args:
            - `func (callable)`: Function to wrap inside the error handler
            - `error_message (str)`: The short message to display when an error occurs
        """
        try:
            func()
        except Exception as e:
            self.display_error(error_message, traceback.format_exc())


app = QtWidgets.QApplication(sys.argv)
w = AppWindow()
w.show()
app.exec()