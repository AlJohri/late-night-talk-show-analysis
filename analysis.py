import os
import pandas as pd

from settings import PARSED_FOLDER

kind = "DFXP"
parsed_folder = PARSED_FOLDER.format(kind=kind)

def create_df():
    ratings = pd.read_csv("data/ratings.csv", index_col='number')
    episode_list = pd.read_csv("data/episode_list.csv", parse_dates=['airdate'], index_col='number')
    episode_list.rename(columns={"name": "title"}, inplace=True)
    episode_list.drop('url', axis=1, inplace=True)

    subtitles = []
    for parsed_filename in os.listdir(parsed_folder):
        parsed_path = parsed_folder + parsed_filename
        with open(parsed_path) as f:
            text = f.read()
            subtitles.append({"filename": parsed_filename, "text": text})
    subtitles = pd.DataFrame(subtitles)
    subtitles['number'] = subtitles.filename.str.replace("CBS_COLBERT_", "") \
                                            .str.replace("_CONTENT_CIAN_caption_DFXP.txt", "").astype(int)
    subtitles.drop('filename', axis=1, inplace=True)
    subtitles.set_index('number', inplace=True)

    episodes = pd.concat([ratings, episode_list, subtitles], axis=1).reset_index()

    return episodes
