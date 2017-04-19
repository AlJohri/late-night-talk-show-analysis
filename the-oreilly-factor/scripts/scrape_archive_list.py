#!/usr/bin/env python3

import json
import arrow
import requests
import calendar
import lxml.html

date_format = 'dddd, MMMM D YYYY'

base_params = {
    "action": "tvShowArchive",
    "include": "true",
    "destinationpage": "/pg/jsp/community/tvshowarchiveinclude.jsp",
    "sort": "asc",
}

def parse(html):
    shows = []
    doc = lxml.html.fromstring(html)
    for show in doc.cssselect("td.showBody"):
        try:
            atag = show.cssselect('a')[0]
        except IndexError:
            print("Could not find a tag")
            print(lxml.html.tostring(show))
            continue
        show_url = "https://www.billoreilly.com" + atag.get('href')
        show_id = int(show_url.replace('https://www.billoreilly.com/show?action=viewTVShow&showID=', ''))
        show_date = atag.text + " " + str(year)
        show_parsed_date = arrow.get(show_date, date_format).date().isoformat()
        row = {"id": show_id, "date": show_date, "parsed_date": show_parsed_date, "url": show_url}
        print(row)
        shows.append(row)
    return shows

shows = []

for year in range(2004, 2017+1):
    for month in range(0, 11+1): # 0 Jan, 1 Feb, ... 10 Nov, 11 Dec
        if year == 2004 and month < 10: continue
        if year == 2017 and month > 3: continue
        params = {"year": year, "month": month, **base_params}
        month_name = calendar.month_name[month+1]
        print(f"Downloading {year} {month_name}")
        response = requests.post("https://www.billoreilly.com/show", params=params)
        shows += parse(response.content)

with open('data/archive/archive_list.json', 'w') as f:
    json.dump(shows, f, indent=4)
