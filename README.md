# Late Night Talk Show Analysis

## Shows

- [The Late Show with Stephen Colbert](./the-late-show-with-stephen-colbert)
- [The Colbert Report](./the-colbert-report)
- [The Daily Show with Jon Stewart](./the-daily-show-with-jon-stewart)
- The Daily Show with Trevor Noah

## Usage

Within each show:

`make data` - download latest data

## TV Show Folder Structure

```
.
├── Makefile
├── README.md
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