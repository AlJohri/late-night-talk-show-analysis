#!/usr/bin/env python3

import re, json, arrow, csv

with open('data/imdb_episode_list.csv') as f:
    reader = csv.DictReader(f)
    episodes = [row for row in reader]

# verify that the last episode number = the number of rows for each season
for season_number in range(1, 5):
    print(f'verifying season {season_number}')
    season_episodes = [x for x in episodes if x['season'] == str(season_number)]
    assert len(season_episodes) == int(season_episodes[-1]['episode_number'])

episodes_as_dict = {(e['season'], e['episode_number']):e for e in episodes}

trump_mentions = []

with open('data/nbc_metadata.json') as f:
    metadata = json.load(f)

    for k,v in metadata.items():
        id_ = k
        season_number = v['attributes']['seasonNumber']
        episode_number = v['attributes']['episodeNumber']
        title = v['attributes']['title']
        air_date = v['attributes']['airdate']
        print(id_, season_number, episode_number, air_date, title)

        if not season_number or not episode_number:
            print(f'skipping {id_}...')
            continue

        try:
            with open(f'data/parsed/{id_}.txt') as f:
                num_trump_mentions = count = sum(len(re.findall(r'\btrump\b', line, flags=re.IGNORECASE)) for line in f)
        except FileNotFoundError as e:
            print(f"skipping {id_}...")

        trump_mentions.append({
            "season": season_number,
            "episode_number": episode_number,
            "air_date": air_date,
            "count": num_trump_mentions
        })

        print(air_date, num_trump_mentions)

with open('data/trump_mentions.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['season', 'episode_number', 'air_date', 'count'])
    writer.writeheader()
    writer.writerows(trump_mentions)
