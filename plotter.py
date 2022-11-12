import pandas as pd
from numpy import int64
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass

pd.options.plotting.backend = "plotly"
COLORS = px.colors.qualitative.Plotly

@dataclass
class PlotParameters:
    xlabel: str
    ylabel: str
    width: int
    height: int
    font_size: int
    legend_title: str
    title: str
    title_position: str
    xaxis_ticks: str
    yaxis_ticks: str
    b_show_legend: bool
    b_multicoloured: bool

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

    def get_line_fig(self, x: str, y: str, col_graph: str, graphs: list[str], params: PlotParameters):
        df = self.data.loc[self.data[col_graph].isin(graphs)]

        fig = px.line(df, x = x, y = y, color=col_graph)

        if not graphs:
            setup_fig_look(fig, params)
            return fig

        
        L = len(COLORS)
        ymax = max(df[y])

        yld = []
        for i, g in enumerate(graphs):
            ylasts = df.loc[df[col_graph] == g]
            ylast = ylasts.iloc[-1, df.columns.get_loc(y)]
            yld.append([g, COLORS[i%L], ylast/ymax])

        yld.sort(reverse=True, key=lambda x: x[2])
        
        ratio = float(params.width)/params.height
        dy = (params.font_size + 8) / params.height
        for i in range(len(yld)):
            if i > 1 and abs(yld[i-1][2] - yld[i][2]) < dy:
                cdy = yld[i-1][2] - yld[i][2]
                for j in range(i, len(yld)):
                    yld[j][2] -= 1.01*dy-cdy

            font = {"color": yld[i][1]}
            fig.add_annotation(font=font, 
                               x=max(1.008, 1+(ratio-1)/(40*ratio)), y=yld[i][2], 
                               xref="x domain", yref="paper",
                               ax=1, ay = 0, xanchor="left", yanchor="middle",
                               text=yld[i][0], showarrow=False)

        setup_fig_look(fig, params)

        margin = max(map(len, graphs))
        fig.update_layout(showlegend=False, margin=dict(r=params.width/15+margin*6))

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
            fig.update_layout(xaxis={'categoryorder':'total descending'})
        else:
            fig = px.bar(df, x=value, y=label, color=filter, orientation=orientation)
            params.xlabel, params.ylabel = params.ylabel, params.xlabel
            fig.update_layout(yaxis={'categoryorder':'total descending'})
        
        setup_fig_look(fig, params, orientation != "v")
        fig.update_layout(barmode="stack", showlegend = params.b_show_legend)
        
        if params.b_multicoloured:
            fig.update_traces(marker_color = COLORS)

        return fig

    def get_pie_fig(self, label: str, value:str, filter: str, includes: list[str], filtered: list[str], params: PlotParameters):
        if self.data.dtypes[label] == int64:
            includes = [int64(x) for x in includes]
        
        if self.data.dtypes[filter] == int64:
            filtered = [int64(x) for x in filtered]

        df = self.data[self.data[label].isin(includes) & self.data[filter].isin(filtered)]
        df[filter] = df[filter].astype(str)

        fig = px.pie(df, values=value, names=label)
        fig.update_traces(textinfo = "label+percent", textposition="outside")
        fig.update_layout(title = params.title, legend_title_text = params.legend_title, showlegend=False)
        
        return fig

def setup_fig_look(fig, params: PlotParameters, transpose = False):


    fig.update_layout(plot_bgcolor = "White", 
                      title = params.title, 
                      legend_title_text = params.legend_title,
                      xaxis_tickformat = get_tick_format(params.xaxis_ticks),
                      yaxis_tickformat = get_tick_format(params.yaxis_ticks),
                      title_x = 0.0 if params.title_position == "Left" else 0.5 if params.title_position == "Center" else 1.0)
    if not transpose:
        fig.update_xaxes(title_text = params.xlabel, showgrid = False)
        fig.update_yaxes(title_text = params.ylabel, griddash = "dot", gridcolor = "LightGrey", rangemode="tozero", zeroline = True)
    else:
        fig.update_xaxes(title_text = params.xlabel, griddash = "dot", gridcolor = "LightGrey")
        fig.update_yaxes(title_text = params.xlabel, showgrid = False, rangemode="tozero", zeroline = True)

    return fig

def get_tick_format(type: str):
    match type:
        case "Full":
            return "d"
        case "Reduced":
            return ".3"
        case "SI":
            return ".3s"

    return ""