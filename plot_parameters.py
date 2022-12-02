from dataclasses import dataclass
from enum import Enum

class Position(Enum):
    """# `Position`
    An enum class that stores a horisontal position:
    - `LEFT = 0`
    - `CENTER = 1`
    - `RIGHT = 2`
    """
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class TickFormat(Enum):
    """# `TickFormat`
    An enum class that stores a plot tick format:
    - `AUTO = 0`, e.g. 10k
    - `FULL = 1`, e.g. 10000
    - `SI = 2`, e.g. 1e+4
    - `REDUCED = 3`, e.g. 10.0 (maximum of 2 decimals)
    """
    AUTO = 0
    FULL = 1
    SI = 2
    REDUCED = 3

class PlotType(Enum):
    """# `PlotType`
    An enum class that stores a type of plot among:
    - `LINE = 0`
    - `BAR = 1`
    - `PIE = 2`
    """
    LINE = 0
    BAR = 1
    PIE = 2

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
    title_position: Position
    x_tick_format: TickFormat
    y_tick_format: TickFormat
