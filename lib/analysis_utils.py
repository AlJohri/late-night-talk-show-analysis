import pandas as pd

import bokeh.charts
from bokeh.plotting import figure
from bokeh.models import HoverTool, BoxSelectTool, ColumnDataSource
bokeh.charts.defaults.width = 950
bokeh.charts.defaults.height = 400

def plot_interactive_timeseries(x, y, data, title, hover_cols=None):
    hover_cols = hover_cols or list(data.columns)
    df = data[hover_cols].dropna(axis=0, how='any')
    source = ColumnDataSource(df)

    tooltips = []
    for col in df.columns:
        df[col].dtype
        if df[col].dtype == pd.np.dtype('datetime64[ns]'):
            # TODO: fix air_date is off by a day 
            # tz_localize('US/Eastern')
            source.add(df[col].map(lambda x: x.strftime('%x')), col + "_str")
            tooltips.append([col, "@" + col + "_str"])
        elif df[col].dtype == pd.np.dtype('float64'):
            tooltips.append([col, "@" + col + "{1.11}"])
        else:
            tooltips.append([col, "@" + col])
    
    p = figure(
        plot_width=bokeh.charts.defaults.width,
        plot_height=bokeh.charts.defaults.height,
        x_axis_type="datetime",
        title=title)

    p.axis[1].formatter.use_scientific = False

    hover = HoverTool(tooltips=tooltips)

    p.circle(x=x, y=y, line_width=2, source=source, size=5)
    p.add_tools(hover)
    p.toolbar.logo = None

    return p
