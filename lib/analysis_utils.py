import os
import pandas as pd

import bokeh.charts
from bokeh.plotting import figure
from bokeh.models import HoverTool, BoxSelectTool, ColumnDataSource
bokeh.charts.defaults.width = 950
bokeh.charts.defaults.height = 400

parsed_folder = "../data/parsed/DFXP/"

def create_df():
    ratings = pd.read_csv("../data/imdb_ratings.csv", index_col='episode_number')
    episode_list = pd.read_csv("../data/imdb_episode_list.csv", parse_dates=['air_date'], index_col='episode_number')
    episode_list.rename(columns={"name": "title"}, inplace=True)
    episode_list.drop('url', axis=1, inplace=True)

    subtitles = []
    for parsed_filename in os.listdir(parsed_folder):
        parsed_path = parsed_folder + parsed_filename
        with open(parsed_path) as f:
            text = f.read()
            subtitles.append({"filename": parsed_filename, "text": text})
    subtitles = pd.DataFrame(subtitles)
    subtitles['episode_number'] = subtitles.filename.str.replace("CBS_COLBERT_", "") \
                                            .str.replace("_CONTENT_CIAN_caption_DFXP.txt", "").astype(int)
    subtitles.drop('filename', axis=1, inplace=True)
    subtitles.set_index('episode_number', inplace=True)

    episodes = pd.concat([ratings, episode_list, subtitles], axis=1).reset_index()

    return episodes

def plot_interactive_timeseries(x, y, data, title):

    hover_cols = ['episode_number', 'title', 'air_date', 'rating', 'rating_count']

    df = data[hover_cols].dropna(axis=0, how='any')

    p = figure(
        plot_width=bokeh.charts.defaults.width,
        plot_height=bokeh.charts.defaults.height,
        x_axis_type="datetime",
        title=title)

    hover = HoverTool(tooltips=[
                ("Episode", "@number"),
                ("Title", "@title"),
                ("Air Date", "@air_date_str"),
                ("Rating", "@rating{1.11}"),
                ("Rating Count", "@rating_count{1.11}")])

    source = ColumnDataSource(df[hover_cols])
    source.add(df.air_date.map(lambda x: x.strftime('%x')), 'air_date_str')
    p.circle(x=x, y=y, line_width=2, source=source, size=5)
    p.add_tools(hover)
    p.logo = None

    return p
