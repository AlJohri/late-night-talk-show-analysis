import os
import pandas as pd

parsed_folder = "../data/parsed/DFXP/"

def create_df():

    ratings = pd.read_csv("../data/imdb_ratings.csv", index_col=['season', 'episode_number'])
    episode_list = pd.read_csv("../data/imdb_episode_list.csv", parse_dates=['air_date'], index_col=['season', 'episode_number'])
    episode_list.rename(columns={"name": "title"}, inplace=True)
    episode_list.drop('url', axis=1, inplace=True)
    episode_list.drop('air_date', axis=1, inplace=True)
    episode_list.drop('title', axis=1, inplace=True)
    episode_list.drop('description', axis=1, inplace=True)
    metadata = pd.read_csv("../data/comedy_central_metadata.csv", thousands=",", index_col=['season_number', 'episode_airing_order'])
    metadata.drop('episode_number', axis=1, inplace=True)
    metadata.index.rename(['season', 'episode_number'], inplace=True)
    metadata['air_date'] = pd.to_datetime(metadata.air_date, unit='s')
    metadata['publish_date'] = pd.to_datetime(metadata.publish_date, unit='s')
    episodes = pd.concat([ratings, episode_list, metadata], axis=1).reset_index()
    
    # subtitles = []
    # for parsed_filename in os.listdir(parsed_folder):
    #     parsed_path = parsed_folder + parsed_filename
    #     with open(parsed_path) as f:
    #         text = f.read()
    #         subtitles.append({"filename": parsed_filename, "text": text})
    # subtitles = pd.DataFrame(subtitles)
    # subtitles['episode_number'] = subtitles.filename.str.replace("CBS_COLBERT_", "") \
    #                                         .str.replace("_CONTENT_CIAN_caption_DFXP.txt", "").astype(int)
    # subtitles.drop('filename', axis=1, inplace=True)
    # subtitles.set_index('episode_number', inplace=True)

    episodes = pd.concat([ratings, episode_list, metadata], axis=1).reset_index()

    return episodes