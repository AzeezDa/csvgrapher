from dataclasses import dataclass

@dataclass
class PlotParameters:
    """# `PlotParameters`
    A dataclass that stores the settings from the Qt window. This is passed into the other classes in the program.
    """
    x_axis: str
    y_axis: str
    based_on: str
    based_on_list: list[str]
    plot_type: str
    multicoloured_bar: bool
    vertical_bar: bool
    plot_title: str
    x_label: str
    y_label: str
    legend_title: str
    show_legend: bool
    width: int
    height: int
    font_size: int
    title_position: str
    x_tick_format: str
    y_tick_format: str
    enable_x_ticks: bool
    enable_y_ticks: bool
    x_ticks: int
    y_ticks: int