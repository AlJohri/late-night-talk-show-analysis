#!/usr/bin/env python3

import re
import json
import calendar
import arrow
import lxml.html
import pandas as pd

from blessings import Terminal
t = Terminal()

pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 200)

def month_to_number(x):
    for num, month in enumerate(calendar.month_abbr):
        if not month: continue
        if month in x:
            return num

def parse_table(title, table):
    m1 = re.match(r"Late-night ratings, ([\w\.]+) (\d+)(?:\s)?(?:–|-)(?:\s)?(\d+), (\d{4})", title)
    if m1:
        month = str(month_to_number(m1.groups()[0])).zfill(2)
        year = m1.groups()[-1]
        start_date = f"{year}-{month}-{m1.groups()[1].zfill(2)}"
        end_date = f"{year}-{month}-{m1.groups()[2].zfill(2)}"
        print(t.green(f"{start_date} {end_date}"))
    else:
        m2 = re.match(r"Late-night ratings, ([\w\.]+) (\d+)(?:\s)?(?:–|-)(?:\s)?([\w\.]+) (\d+), (\d{4})", title)
        if m2:
            month1 = str(month_to_number(m1.groups()[0])).zfill(2)
            month2 = str(month_to_number(m1.groups()[2])).zfill(2)
            year = m1.groups()[-1]
            start_date = f"{year}-{month1}-{m1.groups()[1].zfill(2)}"
            end_date = f"{year}-{month2}-{m1.groups()[3].zfill(2)}"
            print(t.green(f"{start_date} {end_date}"))
        else:
            print(title)
            import pdb; pdb.set_trace()

    headers = [header.text_content().replace('\xa0', '') for header in table.cssselect("tbody tr:first-child td strong")]

    assert len(headers) == 6
    assert headers[0] == 'Show'
    assert headers[1] == 'Net'

    # m1 = re.match(r'Adults 18-49, (\d+/\d+)(?:\s)?(?:–|-)(?:\s)?(\d+/\d+)', headers[2])
    # if m1:
    #     start_date, end_date = m1.groups()
    # else:
    #     m2 = re.match(r'Adults 18-49, (\d+/\d+)(?:\s)?(?:–|-)(?:\s)?(\d+)', headers[2])
    #     if m2:
    #         start_date, half_end_date = m2.groups()
    #         start_date = "/".join([x.zfill(2) for x in start_date.split('/')])
    #         end_date = start_date.partition('/')[0] + '/' + half_end_date.zfill(2)
    #     else:
    #         m3 = re.match(r'Adults 18-49 wk of (\d+/\d+)(?:\s)?(?:–|-)(?:\s)?(\d+)', headers[2])
    #         if m3:
    #             start_date, half_end_date = m3.groups()
    #             start_date = "/".join([x.zfill(2) for x in start_date.split('/')])
    #             end_date = start_date.partition('/')[0] + '/' + half_end_date.zfill(2)
    #         else:
    #             raise Exception(t.red(f'unable to parse date for {headers[2]}'))

    # start_date = year + '-' + start_date.replace('/', '-')
    # end_date = year + '-' + end_date.replace('/', '-')

    assert len(start_date) == 10
    assert len(end_date) == 10

    # print("DATES", start_date, end_date)

    headers[0] = 'show'
    headers[1] = 'network'
    headers[2] = 'adults_18_49_week'
    headers[3] = 'viewers_week'
    headers[4] = 'adults_18_49_season'
    headers[5] = 'viewers_season'

    results = [{headers[i]: cell.text_content() for i, cell in enumerate(row.cssselect("td"))} for row in table.cssselect("tbody tr:not(:first-child)")
        if " p.m." not in row.cssselect("td")[0].text_content() and
           " a.m." not in row.cssselect("td")[0].text_content() and
           row.cssselect("td")[0].text_content().strip() != ""]

    headers.append('start_date')
    headers.append('end_date')
    for result in results:
        result['show'] = result['show'].replace(' – R', '').replace(' –R', '').replace(' -R', '')
        result['start_date'] = start_date
        result['end_date'] = end_date

    return headers, results

with open('data/entries.json') as f:
    entries = json.load(f)

all_results = []

for entry in entries:
    print(t.bold_white(entry['title']))
    print(entry['link'])
    if 'Late-night ratings, ' not in entry['title']:
        print('Invalid title, skipping...')
        continue
    assert len(entry['content']) == 1
    doc = lxml.html.fromstring(entry['content'][0]['value'])
    if not doc.cssselect('table'):
        print(t.yellow('No table found, skipping...'))
        continue
    table = doc.cssselect('table')[0]
    try:
        headers, results = parse_table(entry['title'], table)
    except Exception as e:
        print(e)
        print(t.yellow('Error parsing table, skipping...'))
        continue
    current_df = pd.DataFrame(results, columns=headers)
    print(current_df)
    all_results += results

last_headers = headers

df = pd.DataFrame(all_results, columns=last_headers).sort_values(by=['start_date', 'show'])
print(df)
print()

df.to_csv('ratings.csv', index=False)