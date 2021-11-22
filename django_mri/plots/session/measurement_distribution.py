"""
Creates a Bokeh plot visualizing monthly session acqusition counts by
measurement definition.
"""
from datetime import datetime
from typing import List, Tuple

import pandas as pd
from bokeh.models import (ColumnDataSource, FactorRange, FuncTickFormatter,
                          GlyphRenderer, HoverTool, Legend, LinearAxis,
                          Range1d)
from bokeh.palettes import Category20_20
from bokeh.plotting import Figure, figure
from django.db.models import QuerySet

TITLE = "Monthly Session Acquisition Counts by Measurement Definition"
FIGURE_KWARGS = {
    "title": TITLE,
    "x_axis_label": "Month",
    "y_axis_label": "Count",
    "plot_height": 400,
    "plot_width": 1500,
    "toolbar_location": "above",
}
QUERYSET_FIELDS = "time", "measurement__title"
COLUMN_NAMES = "Time", "Measurement"
CUMULATIVE_AXIS_KWARGS = {
    "axis_label": "Cumulative Sum",
    "y_range_name": "cumulative_y_range",
}
STACK_HOVER_TOOLTIPS = [
    ("Acquisition", "$name"),
    ("Month", "@x_range"),
    ("Count", "@$name"),
]
LINE_HOVER_TOOLTIPS = [
    ("Month", "@x_range"),
    ("Monthly", "@total"),
    ("Total", "@cumulative"),
]
LINE_HOVER_KWARGS = {
    "names": ["cumulative_line"],
    "tooltips": LINE_HOVER_TOOLTIPS,
    "line_policy": "nearest",
}
TICK_FORMATTER_JS = """
        let i = index + 1
        if ([3, 6, 9].includes(i % 12))
        {
            return tick;
        }
        else
        {
            return "";
        }
        """
CUMULATIVE_LINE_KWARGS = {
    "x": "x_range",
    "y": "cumulative",
    "line_color": "grey",
    "line_width": 1.5,
    "alpha": 0.75,
    "y_range_name": "cumulative_y_range",
    "name": "cumulative_line",
}
ACQUISITION_SUFFIX = " MRI Acquisition"
GROUPING = ["Year", "Month", "Measurement"]
BAR_STACK_KWARGS = {"width": 1, "x": "x_range"}
LEGEND_KWARGS = {
    "location": (0, -30),
    "label_text_font_size": "8pt",
    "glyph_width": 12,
    "glyph_height": 12,
    "spacing": 1,
    "padding": 2,
}


def parse_dataframe(values: List[Tuple[datetime, str]]) -> QuerySet:
    df = pd.DataFrame(values, columns=COLUMN_NAMES)
    # Convert None to string so that they will be kept in count.
    df["Measurement"] = df["Measurement"].astype(str)
    # Remove 'MRI Acquisition' from definition titles.
    df["Measurement"] = df["Measurement"].str.replace(ACQUISITION_SUFFIX, "")
    # Create Year and Month columns convenience.
    df["Year"] = df["Time"].dt.year
    df["Month"] = df["Time"].dt.month
    return df


def calculate_counts(df: pd.DataFrame) -> pd.Series:
    # Calculate monthly counts per measurement definition.
    counts = df.groupby(GROUPING).count()
    # Create a MultiIndex to reindex counts by.
    year_range = range(df["Year"].min(), df["Year"].max() + 1)
    month_range = range(1, 13)
    measurements = list(df["Measurement"].unique())
    index = pd.MultiIndex.from_product(
        [year_range, month_range, measurements], names=GROUPING,
    )
    return counts.reindex(index, fill_value=0).squeeze()


def parse_x_range(counts: pd.Series) -> List[Tuple[str, str]]:
    # Create the x-axis range for easy visual representation.
    month_tuples = counts.groupby(["Year", "Month"]).last().index.values
    return [tuple(str(unit) for unit in t) for t in month_tuples]


def create_source(counts: pd.Series) -> ColumnDataSource:
    # Create source dataframe with total and cumulative counts.
    data = counts.unstack()
    data["total"] = data.sum(axis=1)
    data["cumulative"] = data["total"].cumsum()
    data["x_range"] = parse_x_range(counts)
    return ColumnDataSource(data=data)


def plot_bar_stack(
    p: Figure, source: ColumnDataSource, df: pd.DataFrame
) -> List[GlyphRenderer]:
    # Plot bar stack.
    measurements = list(df["Measurement"].unique())
    n_measurements = len(measurements)
    color = list((Category20_20 * 2)[:n_measurements])
    if "None" in measurements:
        color[measurements.index("None")] = "black"
    bar_stack = p.vbar_stack(
        **BAR_STACK_KWARGS, stackers=measurements, color=color, source=source,
    )
    stack_hover = HoverTool(
        renderers=bar_stack, tooltips=STACK_HOVER_TOOLTIPS,
    )
    p.add_tools(stack_hover)
    # Customize left y-axis range.
    p.y_range.start = 0
    max_count = bar_stack[0].data_source.data["total"].max() + 1
    p.y_range.end = max_count
    # Create a legend.
    kwargs = LEGEND_KWARGS.copy()
    if len(measurements) == 1:
        kwargs["location"] = (0, 250)
    legend = Legend(
        items=[
            (measurement, [bar_stack[i]])
            for i, measurement in enumerate(measurements)
        ],
        **kwargs,
    )
    p.add_layout(legend, "right")
    return bar_stack


def add_cumulative_axis(p: Figure, source: ColumnDataSource):
    # Create right y-axis for cumulative line.
    cumulative_top = source.data["cumulative"].max() * 1.1
    p.extra_y_ranges = {
        "cumulative_y_range": Range1d(start=0, end=cumulative_top)
    }
    cumulative_axis = LinearAxis(**CUMULATIVE_AXIS_KWARGS)
    p.add_layout(cumulative_axis, "right")


def plot_cumulative_line(p: Figure, source: ColumnDataSource) -> GlyphRenderer:
    # Plot cumulative line.
    cumulative_line = p.line(**CUMULATIVE_LINE_KWARGS, source=source)
    line_hover = HoverTool(**LINE_HOVER_KWARGS)
    p.add_tools(line_hover)
    return cumulative_line


def customize_figure(p: Figure):
    # Remove grid.
    p.xgrid.grid_line_color = None
    # Remove some ticks from the x-axis to prevent overlap.
    p.xaxis.formatter = FuncTickFormatter(code=TICK_FORMATTER_JS)


def plot_measurement_by_month(queryset: QuerySet) -> Figure:
    # Calculate measurement counts by month.
    values = list(queryset.values_list(*QUERYSET_FIELDS))
    df = parse_dataframe(values)
    counts = calculate_counts(df)
    source = create_source(counts)
    # Create bokeh figure.
    x_range = FactorRange(*source.data["x_range"], group_padding=0)
    p = figure(x_range=x_range, **FIGURE_KWARGS)
    add_cumulative_axis(p, source)
    plot_bar_stack(p, source, df)
    plot_cumulative_line(p, source)
    customize_figure(p)
    return p
