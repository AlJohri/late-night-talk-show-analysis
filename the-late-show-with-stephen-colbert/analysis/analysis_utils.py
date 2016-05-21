import os
import pandas as pd

parsed_folder = "../data/parsed/DFXP/"

def create_df():
    ratings = pd.read_csv("../data/imdb_ratings.csv", index_col='episode_number')
    ratings.drop('season', axis=1, inplace=True)
    episode_list = pd.read_csv("../data/imdb_episode_list.csv", parse_dates=['air_date'], index_col='episode_number')
    episode_list.rename(columns={"name": "title"}, inplace=True)
    episode_list.drop('url', axis=1, inplace=True)
    episode_list.drop('season', axis=1, inplace=True)

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