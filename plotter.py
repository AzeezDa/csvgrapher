import pandas as pd
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go
from plot_parameters import PlotParameters

pd.options.plotting.backend = "plotly"
COLORS = px.colors.qualitative.Plotly
COLOR_AMOUNT = len(COLORS)
COLUMNS = "COLUMNS"

class Plotter():
    """# `Plotter`
    A class that stores a pandas `DataFrame` and a `PlotParameters` dataclass and uses them to plot Plotly graphs.
    """
    def __init__(self, dataframe: DataFrame, plot_parameters: PlotParameters):
        """# `Plotter`
        Initalise the `Plotter` class.

        ## Args:
            - `dataframe (DataFrame)`: A pandas `DataFrame` that will be plotted
            - `plot_parameters (PlotParameters)`: An instance of the `PlotParameters` holding the settings from the Qt window
        """
        self.dataframe = dataframe
        self.plot_parameters = plot_parameters

    def plot(self):
        """# `plot`

        ## Returns:
            `Figure | None`: Returns a `plotly.express` plot based on the plot parameters
        """
        figure = None
        match self.plot_parameters.plot_type:
            case "Line":
                figure = self.__get_line_figure()
            case "Bar":
                figure = self.__get_bar_figure()
            case "Pie":
                figure = self.__get_pie_figure()

        return figure

    
    def __get_line_figure(self):
        """# `__get_line_figure`
        Based on the `Plotter`'s `PlotParamters` return a line plot

        ## Returns:
            Figure: A plotly express line plot
        """
        figure = go.Figure()
        if self.plot_parameters.based_on == COLUMNS:
            x_vals = self.dataframe.loc[:, self.plot_parameters.x_axis].values.tolist()
            max_y = 0
            y_lasts = []
            for column in self.plot_parameters.based_on_list:
                values = self.dataframe.loc[:, column].values.tolist()
                y_lasts.append(values[-1])
                max_y = max(max_y, max(values))
                figure.add_scatter(x = x_vals, y = values, name = column)
            figure = self.__add_line_legend_wide(figure, max_y, y_lasts)
        else:
            dataframe = self.dataframe.loc[self.dataframe[self.plot_parameters.based_on].isin(self.plot_parameters.based_on_list)]
            figure = px.line(dataframe,
                x = self.plot_parameters.x_axis,
                y = self.plot_parameters.y_axis,
                color = self.plot_parameters.based_on)
            figure = self.__add_line_legend_long(figure)


        self.__setup_figure_look(figure)

        margin = max(map(len, self.plot_parameters.based_on_list))
        figure.update_layout(showlegend=False, margin=dict(r=self.plot_parameters.width / 15 + margin * 6))

        return figure

    def __add_line_legend_long(self, figure):
        """# `__add_line_legend`
        Take a plotly express line plot and adds a special legend to it that is a label at the end of each line with the same colour as that line

        ## Args:
            figure (Figure): A plotly express line plot that needs a special legend added

        ## Returns:
            Figure: A plotly express line plot with a special legend added
        """
        if not self.plot_parameters.based_on_list:
            self.__setup_figure_look(figure)
            return figure

        y_max = max(self.dataframe[self.plot_parameters.y_axis])

        y_last_distances = []
        for i, based_on in enumerate(self.plot_parameters.based_on_list):
            y_lasts = self.dataframe.loc[self.dataframe[self.plot_parameters.based_on] == based_on]
            y_last = y_lasts.iloc[-1, self.dataframe.columns.get_loc(self.plot_parameters.y_axis)]
            y_last_distances.append([based_on, COLORS[i % COLOR_AMOUNT], y_last/y_max])

        y_last_distances.sort(reverse=True, key=lambda x: x[2])
        
        aspect_ratio = self.plot_parameters.width/self.plot_parameters.height
        dy = (self.plot_parameters.font_size + 8) / self.plot_parameters.height
        for i in range(len(y_last_distances)):
            current_dy = y_last_distances[i-1][2] - y_last_distances[i][2]
            if i > 1 and abs(current_dy) < dy:
                for j in range(i, len(y_last_distances)):
                    y_last_distances[j][2] -= 1.01*dy-current_dy

            font = {"color": y_last_distances[i][1]}
            figure.add_annotation(font=font, 
                               x=max(1.008, 1+(aspect_ratio-1)/(40*aspect_ratio)), y=y_last_distances[i][2], 
                               xref="x domain", yref="paper",
                               ax=1, ay = 0, xanchor="left", yanchor="middle",
                               text=y_last_distances[i][0], showarrow=False)

        return figure

    def __add_line_legend_wide(self, figure, y_max, y_lasts):
        if not self.plot_parameters.based_on_list:
            self.__setup_figure_look(figure)
            return figure

        y_last_distances = []
        for i, based_on in enumerate(self.plot_parameters.based_on_list):
            y_last_distances.append([based_on, COLORS[i % COLOR_AMOUNT], y_lasts[i]/y_max])

        y_last_distances.sort(reverse=True, key=lambda x: x[2])
        
        aspect_ratio = self.plot_parameters.width/self.plot_parameters.height
        dy = (self.plot_parameters.font_size + 8) / self.plot_parameters.height
        for i in range(len(y_last_distances)):
            current_dy = y_last_distances[i-1][2] - y_last_distances[i][2]
            if i > 1 and abs(current_dy) < dy:
                for j in range(i, len(y_last_distances)):
                    y_last_distances[j][2] -= 1.01*dy-current_dy

            font = {"color": y_last_distances[i][1]}
            figure.add_annotation(font=font, 
                               x=max(1.008, 1+(aspect_ratio-1)/(40*aspect_ratio)), y=y_last_distances[i][2], 
                               xref="x domain", yref="paper",
                               ax=1, ay = 0, xanchor="left", yanchor="middle",
                               text=y_last_distances[i][0], showarrow=False)

        return figure


    def __get_bar_figure(self):
        """# `__get_bar_figure`
        Based on the `Plotter`'s `PlotParamters` return a bar plot

        ## Returns:
            Figure: A plotly express bar plot
        """
        if self.plot_parameters.based_on == COLUMNS:
            figure = go.Figure()
            header = [self.plot_parameters.x_axis]+self.plot_parameters.based_on_list
            dataframe = self.dataframe.loc[:,header]
            if self.plot_parameters.vertical_bar:
                for data in dataframe.values.tolist():
                    figure.add_bar(
                        x = self.plot_parameters.based_on_list,
                        y = data[1::],
                        name = self.plot_parameters.x_axis)
                figure.update_layout(xaxis={'categoryorder':'total ascending'})
            else:
                for data in dataframe.values.tolist():
                    figure.add_bar(
                        y = self.plot_parameters.based_on_list,
                        x = data[1::],
                        name = self.plot_parameters.x_axis,
                        orientation = "h")
                figure.update_layout(yaxis={'categoryorder':'total ascending'})
        else:
            dataframe = self.dataframe.loc[self.dataframe[self.plot_parameters.based_on].isin(self.plot_parameters.based_on_list)]
            if self.plot_parameters.vertical_bar:
                figure = px.bar(dataframe,
                    x = self.plot_parameters.x_axis,
                    y = self.plot_parameters.y_axis,
                    color = self.plot_parameters.based_on_list)
                figure.update_layout(xaxis={'categoryorder':'total ascending'})
            else:
                figure = px.bar(dataframe,
                    x = self.plot_parameters.y_axis,
                    y = self.plot_parameters.x_axis,
                    color = self.plot_parameters.based_on_list,
                    orientation = "h")
                figure.update_layout(yaxis={'categoryorder':'total ascending'})
        
        self.__setup_figure_look(figure, not self.plot_parameters.vertical_bar)
        figure.update_layout(barmode="stack", showlegend = self.plot_parameters.show_legend)
        
        if self.plot_parameters.based_on == COLUMNS:
            if self.plot_parameters.multicoloured_bar:
                figure.update_traces(marker_color = COLORS)
        else:
            if not self.plot_parameters.multicoloured_bar:
                figure.update_traces(marker_color = COLORS)

        return figure

    def __get_pie_figure(self):
        """# `__get_pie_figure'
        Based on the `Plotter`'s `PlotParamters` return a pie plot

        ## Returns:
            Figure: A plotly express pie plot
        """
        if self.plot_parameters.based_on == COLUMNS:
            figure = go.Figure()
            figure.add_pie(labels = self.plot_parameters.based_on_list,
                           values = self.dataframe.loc[:, self.plot_parameters.based_on_list].values.tolist()[0])
        else:
            dataframe = self.dataframe.loc[self.dataframe[self.plot_parameters.based_on].isin(self.plot_parameters.based_on_list)]
            figure = px.pie(dataframe,
                        names = self.plot_parameters.x_axis,
                        values = self.plot_parameters.y_axis)

        self.__setup_figure_look(figure)
        figure.update_traces(textinfo = "label+percent", textposition="outside")
        figure.update_layout(showlegend = False)
        
        return figure

    def __setup_figure_look(self, figure, transpose = False):
        """# `__setup_figure_look`
        Given a plotly express figure, set up the default apperance settings to it.
        There is also an optional argument `transpose` which if true will rotate the plot 90 degrees clockwise (for example a bar chart's base will be on the y-axis).
        ## Args:
            figure (Figure): A plotly express figure
            transpose (bool, optional): If true then the plot's contents will be rotated 90 degrees clockwise. Defaults to False.
        """
        figure.update_layout(plot_bgcolor = "White", 
                        title = self.plot_parameters.plot_title, 
                        legend_title_text = self.plot_parameters.legend_title,
                        xaxis_tickformat = get_tick_format(self.plot_parameters.x_tick_format),
                        yaxis_tickformat = get_tick_format(self.plot_parameters.y_tick_format),
                        width = self.plot_parameters.width,
                        height = self.plot_parameters.height,
                        font = dict(size = self.plot_parameters.font_size),
                        title_x = 0.0 if self.plot_parameters.title_position == "Left" else 0.5 if self.plot_parameters.title_position == "Center" else 1.0)
        if not transpose:
            figure.update_xaxes(title_text = self.plot_parameters.x_label, showgrid = False)
            figure.update_yaxes(title_text = self.plot_parameters.y_label, griddash = "dot", gridcolor = "LightGrey", rangemode="tozero", zeroline = True)
        else:
            figure.update_xaxes(title_text = self.plot_parameters.y_label, griddash = "dot", gridcolor = "LightGrey")
            figure.update_yaxes(title_text = self.plot_parameters.x_label, showgrid = False, rangemode="tozero", zeroline = True)

def get_tick_format(type: str) -> str:
    """# `get_tick_format`
    Based on the given TickFormat enum value, return the plotly tick format literal for the axes

    ## Args:
        type (TickFormat): A tick format represented by the TickFormat enum

    ## Returns:
        str: The tick format literal used in Plotly
    """
    match type:
        case "Full":
            return "d"
        case "Reduced":
            return ".3"
        case "SI":
            return ".3s"

    return ""