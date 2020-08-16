# reddit_export_userdata

Automatically export userdata from your reddit accounts.

You can export all or any of the following:
- own comments and submissions
- saved comments and submissions
- upvoted comments and submissions

For each one of your accounts, you have to create a reddit script api key and secret key (see https://www.reddit.com/prefs/apps > new app > script).

## Requirements

- praw
- pyyaml

## Installation

```
pip install -r requirements.txt
```

## Configuration

All the configuration happens in a yaml config file. Open the config.example.yaml to see an example on how to fill it.

## Run

```
python reddit_export_userdata.py
```

## Help

```
python reddit_export_userdata.py -h
```

```
usage: reddit_export_userdata.py [-h] [--debug] [-a] [-s] [-c CONFIG_FILE]

reddit_export_userdata. Exports userdata of one or several reddit accounts.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -a, --archivebox_export
                        Export only urls (old.reddit and www.reddit) in order
                        to be used by archivebox.
  -s, --separate_export
                        Export data in separate files for each reddit users.
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Path to the config file (default: "config.yaml")
```
