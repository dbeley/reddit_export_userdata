# reddit_export_userdata

Export userdata from your reddit accounts.

You can export all or any of the following:
- Own comments and submissions
- Saved comments and submissions
- Upvoted comments and submissions

For each one of your accounts, you have to create a reddit script API key and secret API key (see https://www.reddit.com/prefs/apps > new app > script).

## Requirements

- praw
- pyyaml

## Installation

```
git clone https://github.com/dbeley/reddit_export_userdata
cd reddit_export_userdata
pip install praw pyyaml
python reddit_export_userdata.py -h
```

## Configuration

For configuration, open the `config.example.yaml` file to see an example.

```
# Rename this file config.yaml.
users:
    # The four following fields are mandatory.
    - username: username1
      password : password1
      client_id : client_id1
      client_secret : client_secret1
      # At least one export option has to be set.
      exports:
          # Comments made by user.
          - comments
          # Submissions made by user.
          - submissions
          # Submission and comments saved by user.
          - saved
          # Submission and comments upvoted by user.
          - upvoted
    - username: username2
      password : password2
      client_id : client_id2
      client_secret : client_secret2
      exports:
          - saved
options:
    # Each user will have a separate export file.
    separate_export: true
    # Will only export list of urls instead of csv files.
    archivebox_export: true
```

By default, the script search for a `config.yaml` config file, but you can use the `-c/--config_file` argument to use another config file.


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
