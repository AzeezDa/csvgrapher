import sys
from PyQt5 import QtCore, QtWidgets
from main_window import Ui_MainWindow
from plot_parameters import PlotParameters
from plotter import Plotter
from querier import Querier, EqualityCondition
from functools import partial
from numpy import int64
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

        self.querier = None
        self.subquerier = None
        self.previous_tab = 0
        self.conditions = []

        # Save and loading
        self.connect_trigger(self.ui.newFile, self.load_data, "Error encountered while loading file")
        self.connect_trigger(self.ui.saveFile, self.save_figure, "Error encountered while saving file")

        # Apply button
        self.connect_click(self.ui.applyButton, self.apply_to_preview, "Error applying plot to preview")

        # Add condition
        self.connect_click(self.ui.addCondition, self.add_condition, "Error while adding condition")

        # Remove all Condition
        self.connect_click(self.ui.clearConds, self.clear_conditions, "Error while clearing conditions")

        # Where combobox changes
        self.connect_text_change(self.ui.columnWhere, self.update_where_list, "Error while updating the WHERE list")

        # plotType changes
        self.connect_text_change(self.ui.plotType, self.plot_type_update, "Error while updating the Y-axis")

        # basedOn combobox changes
        self.connect_text_change(self.ui.basedOn, self.based_on_update, "Error while updating the based-on list")

        # Changing x ticks customisability
        self.connect_check_change(self.ui.enableXTicks, self.x_ticks_update, "Error while changing x ticks state")

        # Changing x ticks customisability
        self.connect_check_change(self.ui.enableYTicks, self.y_ticks_update, "Error while changing y ticks state")

        self.ui.optionsTabview.currentChanged.connect(partial(self.error_handle, self.tab_changed, "Error changing tabs"))


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

        self.fill_lists(self.ui.columnSelect, columns)

    def fill_lists(self, widget: QtWidgets.QListWidget, values: list[str], check = True):
        """# `fill_lists`
        Given a `QListWidget` and a list of strings, fill the list widget with items from the list of strings
        ## Args:
            `widget (QtWidgets.QListWidget)`: A PyQt ListWidget to add items to
            `values (list[str])`: A list of strings that will be added as items in the list widget
            `check (bool, optional)`: If true then the items will have a checkbox as well. Defaults to True.
        """
        for value in values:
            self.add_to_list(widget, value, check)

    def add_to_list(self, widget: QtWidgets.QListWidget, value: str, check = True):
        """ # `add_to_list`
        Given a `QListWidget` add an item with a string `value` to it. Also if `check` is `True` then that item has a checkbox

        ## Args:
            `widget (QtWidgets.QListWidget)`: A list widget to add an item to.
            `value (str)`: The value to add to the list.
            `check (bool, optional)`: True if the item should have a checkbox. Defaults to True.
        """
        item = QtWidgets.QListWidgetItem(value)
        if check:
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
        widget.addItem(item)

    def get_checked(self, widget: QtWidgets.QListWidget) -> list[str]:
        """# `get_checked`
        Get the checked items in a given `QListWidget`

        ## Args:
            `widget (QtWidgets.QListWidget)`: An `QListWidget` to get the currently checked items from

        ## Returns:
            `list[str]`: A list of `string`s of the checked items in the given list
        """
        checked = []
        for i in range(widget.count()):
            item = widget.item(i)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                checked.append(item.text())

        return checked

    def apply_to_preview(self, save=False):
        """# `apply_to_preview`
        Applies the plot parameters into the Plotter and get the resulting figure based on whether or not it is a preview or save

        ## Args:
            `save (bool, optional)`: If `True` then the figure returned is supplied with the save parameters rather than preview parameters. Defaults to False.

        ## Returns:
            `Figure`: A plotly figure
        """
        parameters = self.scrape_parameters()

        if save:
            return Plotter(self.subquerier.dataframe(), parameters).plot()
        else:
            parameters.width = 700
            parameters.height = 500
            parameters.font_size = 14
            figure = Plotter(self.subquerier.dataframe(), parameters).plot()
            self.ui.plotView.setHtml(figure.to_html(include_plotlyjs="cdn"))

    def save_figure(self):
        """# `save_figure`
        Get the preview with the save parameters and write it to the given file
        """
        f, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", "", "EPS (*.eps);; PNG (*.png);; JPG (*.jpg);; SVG (*.svg)")
        
        if f:
            figure = self.apply_to_preview(True)
            figure.write_image(f)

    def scrape_parameters(self) -> PlotParameters:
        """# `scrape_parameters`

        Returns:
            `PlotParameters`: A `PlotParameters` dataclass containing the parameters from the Qt Window 
        """
        based_on_list = self.get_checked(self.ui.basedOnList)
        based_on = self.ui.basedOn.currentText()
        if self.ui.basedOn != "COLUMNS":
            based_on_list = self.subquerier.incorporate_dtype(based_on, based_on_list)
        parameters = PlotParameters(
            self.ui.xAxis.currentText(),
            self.ui.yAxis.currentText(),
            based_on,
            based_on_list,
            self.ui.plotType.currentText(),
            self.ui.multicolour.isChecked(),
            self.ui.barOrient.currentText() == 'Vertical', # Is vertical
            self.ui.plotTitle.text(),
            self.ui.xAxisLabel.text(),
            self.ui.yAxisLabel.text(),
            self.ui.legendLabel.text(),
            self.ui.showLegend.isChecked(),
            self.ui.width.value(),
            self.ui.height.value(),
            self.ui.fontSize.value(),
            self.ui.titlePosition.currentText(),
            self.ui.xTicksFormat.currentText(),
            self.ui.yTicksFormat.currentText(),
            self.ui.enableXTicks.isChecked(),
            self.ui.enableYTicks.isChecked(),
            self.ui.xTicks.value(),
            self.ui.yTicks.value()
        )

        return parameters

    def tab_changed(self):
        """# `tab_changed`
        The function that is called when the tab is changed. It update the tab that is switched to.
        """
        tab_index = self.ui.optionsTabview.currentIndex()
        if self.querier is None or self.previous_tab != 0: # If don't switch from Query Tab then skip
            self.previous_tab = tab_index
            return

        # If we switch from Query Tab then we clean all other data and parameters in the Plot Settings
        self.previous_tab = tab_index

        result = self.querier.query(self.get_checked(self.ui.columnSelect), self.conditions)
        self.subquerier = Querier(result) # Handles queries in the queried table generated by the Query Tab
        columns = self.subquerier.columns()
        
        # Clear and reset Plot Settings parameters
        self.ui.xAxis.clear()
        self.ui.yAxis.clear()
        self.ui.basedOn.clear()
        self.ui.basedOnList.clear()
        self.ui.xAxis.addItems(columns)
        self.ui.yAxis.addItems(columns)
        self.ui.basedOn.addItems(["COLUMNS"] + columns)

    def add_condition(self):
        """# `add_condition`
        Add a condition to the condition list. Used in the Query Tab
        """
        column = self.ui.columnWhere.currentText()
        checked = self.get_checked(self.ui.columnCondSel)
        checked = self.querier.incorporate_dtype(column, checked) # Correct the type because all values are stored as strings

        condition = EqualityCondition(column, checked)
        self.conditions.append(condition)
        self.add_to_list(self.ui.currentConds, str(condition), False)

    def clear_conditions(self):
        """# `clear_conditions`
        Removes all items in the current condition list
        """
        self.ui.currentConds.clear()
        self.conditions.clear()

    def update_where_list(self):
        """# `update_where_list`
        In the Query Tab, when a the column name under the WHERE statement changes update the list under the EQUALS label
        """
        self.ui.columnCondSel.clear()
        column = self.ui.columnWhere.currentText()
        uniques = self.querier.uniques(column)
        self.fill_lists(self.ui.columnCondSel, uniques)
        
    def based_on_update(self):
        """# `based_on_update`
        In the Plot Settings tab, if the based on value changes (in the combo box) then update the list below it.
        """
        if self.subquerier is None:
            return

        self.ui.basedOnList.clear()
        basedOn = self.ui.basedOn.currentText()
        if basedOn == "COLUMNS":
            self.fill_lists(self.ui.basedOnList, self.subquerier.columns())
            self.ui.yAxis.setEnabled(False)
        else:
            self.fill_lists(self.ui.basedOnList, self.subquerier.uniques(basedOn))
            self.ui.yAxis.setEnabled(True)

    def plot_type_update(self):
        """# `plot_type_update`
        In the Plot Settings tab, when the plot type value changes (in the combo box), update the settings underneath it to switch to a side containing any specific settings.
        Also change the name of the labels above the axis choices to reflect a better terminology connected to the plot type
        """
        current_type = self.ui.plotType.currentText()
        if current_type in ["Bar", "Pie"]:
            if current_type == "Bar":
                self.ui.plotSettings.setCurrentIndex(1) # Bar has specific settings on page 2 of the stacked widget
            else:
                self.ui.plotSettings.setCurrentIndex(0) # Pie has no specific settings

            self.ui.variableLabel.setText("Label")
            self.ui.valueLabel.setText("Value")
        else: # Line plot
            self.ui.plotSettings.setCurrentIndex(0) # No specific settings
            self.ui.variableLabel.setText("X Axis")
            self.ui.valueLabel.setText("Y Axis")

    def x_ticks_update(self):
        """# `x_ticks_update`
        If the user enables the x ticks customisability then enable to spin box that customises the number of ticks 
        """
        self.ui.xTicks.setEnabled(self.ui.enableXTicks.isChecked())


    def y_ticks_update(self):
        """# `y_ticks_update`
        If the user enables the y ticks customisability then enable to spin box that customises the number of ticks 
        """
        self.ui.yTicks.setEnabled(self.ui.enableYTicks.isChecked())

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

    def connect_text_change(self, widget: QtWidgets.QWidget, function: callable, error_message: str = ""):
        """# `connect_text_change`
        Give a widget whose text can change a function to call when its text is changed. If any error occurs during that call display a given error message.
        
        ## Args:
            widget (QtWidgets.QWidget): The widget whose text can change
            function (callable): The function to call upon changing the text of the widget
            error_message (str, optional): The error message to display if an error occurs during the function call. Defaults to "".
        """
        widget.currentTextChanged.connect(partial(self.error_handle, function, error_message))

    def connect_check_change(self, widget: QtWidgets.QWidget, function: callable, error_message: str = ""):
        """# `connect_check_change`
        Give a widget whose check can change a function to call when its text is changed. If any error occurs during that call display a given error message.
        
        ## Args:
            widget (QtWidgets.QWidget): The widget whose check state can change
            function (callable): The function to call upon changing the check state of the widget
            error_message (str, optional): The error message to display if an error occurs during the function call. Defaults to "".
        """
        widget.stateChanged.connect(partial(self.error_handle, function, error_message))

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