#!/usr/bin/env python3

import sys; sys.path.append("../lib")
import re, csv

with open('data/imdb_episode_list.csv') as f:
    reader = csv.DictReader(f)
    episodes = [row for row in reader]

# verify that the last episode number = the number of rows for each season
for season_number in range(1, 3):
    print(f'verifying season {season_number}')
    season_episodes = [x for x in episodes if x['season'] == str(season_number)]
    assert len(season_episodes) == int(season_episodes[-1]['episode_number'])

trump_mentions = []

for i, episode in enumerate(episodes):
    file_index = str(i+1).zfill(4)
    filepath = f'data/parsed/DFXP/CBS_COLBERT_{file_index}_CONTENT_CIAN_caption_DFXP.txt'
    try:
        with open(filepath) as f:
            num_trump_mentions = count = sum(len(re.findall(r'\btrump\b', line, flags=re.IGNORECASE)) for line in f)
    except FileNotFoundError:
        print(f'captions not found for {filepath}')
        continue

    trump_mentions.append({
        "season": episode['season'],
        "episode_number": episode['episode_number'],
        "air_date": episode['air_date'],
        "count": num_trump_mentions
    })

    print(episode['air_date'], num_trump_mentions)

with open('data/trump_mentions.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['season', 'episode_number', 'air_date', 'count'])
    writer.writeheader()
    writer.writerows(trump_mentions)
