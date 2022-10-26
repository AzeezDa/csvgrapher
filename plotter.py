from turtle import bgcolor
import pandas as pd
from numpy import int64
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass

pd.options.plotting.backend = "plotly"

@dataclass
class PlotParameters:
    xlabel: str
    ylabel: str
    legend_title: str
    title: str

class Plotter():
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(file_name)

        self.columns = self.data.columns.to_list()

        self.uniques = dict()
        for c in self.columns:
            self.uniques[c] = self.data[c].unique()

    def get_columns(self) -> list[str]:
        return self.columns

    def get_uniques_in(self, name: str) -> list[str]:
        return [] if name == '' else [str(x) for x in self.uniques[name]]

    def get_line_fig(self, x: str, y: str, col_graph: str, graphs, params: PlotParameters):
        df = self.data[self.data[col_graph].isin(graphs)]

        fig = px.line(df, x = x, y = y, color=col_graph)

        setup_fig_look(fig, params)

        return fig

    def get_bar_fig(self, label: str, value: str, filter:str, include_labels: list[str], filtered: list[str], orientation: str, params: PlotParameters):
        if self.data.dtypes[label] == int64:
            include_labels = [int64(x) for x in include_labels]
        
        if self.data.dtypes[filter] == int64:
            filtered = [int64(x) for x in filtered]

        df = self.data[self.data[label].isin(include_labels) & self.data[filter].isin(filtered)]
        df[filter] = df[filter].astype(str)
        df[label] = df[label].astype(str)

        if orientation == "v":
            fig = px.bar(df, x=label, y=value, color=filter)
        else:
            fig = px.bar(df, x=value, y=label, color=filter, orientation=orientation)
            params.xlabel, params.ylabel = params.ylabel, params.xlabel
        
        setup_fig_look(fig, params)

        return fig

    def get_pie_fig(self, label: str, value:str, filter: str, includes: list[str], filtered: list[str], params: PlotParameters):
        if self.data.dtypes[label] == int64:
            includes = [int64(x) for x in includes]
        
        if self.data.dtypes[filter] == int64:
            filtered = [int64(x) for x in filtered]

        df = self.data[self.data[label].isin(includes) & self.data[filter].isin(filtered)]
        df[filter] = df[filter].astype(str)

        fig = px.pie(df, values=value, names=label)
        fig.update_layout(title = params.title, legend_title_text = params.legend_title)
        
        return fig

def setup_fig_look(fig, params: PlotParameters):
    fig.update_layout(plot_bgcolor = "White", title = params.title, legend_title_text = params.legend_title, yaxis_tickformat = "%d")
    fig.update_xaxes(title_text = params.xlabel, showgrid = False)
    fig.update_yaxes(title_text = params.ylabel, griddash = "dot", gridcolor = "LightGrey", rangemode="tozero", zeroline = True)

    return fig