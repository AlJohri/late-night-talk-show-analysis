# Late Night Talk Show Analysis

## Shows

- [The Late Show with Stephen Colbert](./the-late-show-with-stephen-colbert) | [Notebook](http://nbviewer.jupyter.org/gist/AlJohri/3825066ecfa4688c87f61c1a250aa778)
- [The Colbert Report](./the-colbert-report) | [Notebook](http://nbviewer.jupyter.org/gist/AlJohri/cfcad84b3922922fef837d45c19b31df)
- [The Daily Show with Jon Stewart](./the-daily-show-with-jon-stewart) | [Notebook](http://nbviewer.jupyter.org/gist/AlJohri/31ce93ae800552e844448d80cc7353fe)
- [The Daily Show with Trevor Noah](./the-daily-show-with-trevor-noah)


## Setup

```
mkvirtualenv -p python3 -a "$(pwd)" -r requirements.txt late-night-talk-show-analysis
```

## Usage

Within each show:

`make data` - download latest data

## TV Show Folder Structure

```
.
├── Makefile
├── README.md
├── analysis
│   ├── analysis.ipynb
├── data
│   ├── parsed
│   │   └── DFXP
│   └── raw
│       └── DFXP
└── scripts
    └── *
```

- The `data/parsed/DFXP` folder contains parsed subtitles as `.txt` files.
- The `data/raw/DFXP` contains raw subtitles in the [Timed Text Markup Language](https://en.wikipedia.org/wiki/Timed_Text_Markup_Language) (TTML) previously referred to as the Distribution Format Exchange Profile (DFXP) format.
- The `Makefile` is the entry point for each show. The main command is `make data`.

## Setup

`pip install -r requirements.txt`
