"""
reddit_export_userdata: Export userdata of one or several reddit accounts.
"""
import logging
import time
import argparse
import praw
import collections
import csv
from pathlib import Path
from yaml import load, Loader


logger = logging.getLogger()
start_time = time.time()


# TODO Add config file validation.
def validate_config(config, args):
    return True


def read_config(config_file):
    try:
        with open(config_file, "r") as f:
            config = load(f, Loader=Loader)
    except Exception as e:
        logger.error(e)
    return config


def reddit_connect(user):
    try:
        reddit = praw.Reddit(
            client_id=user["client_id"],
            client_secret=user["client_secret"],
            user_agent="reddit_export_userdata.py script",
            username=user["username"],
            password=user["password"],
        )
        return reddit
    except Exception as e:
        logger.error(f"Couldn't extract data for user {user['username']}: {e}.")


def create_dict(data):
    content = []
    for x in data:
        if not isinstance(x, praw.models.Comment):
            content.append(
                {
                    "Title": x.title,
                    "URL reddit": f"https://www.reddit.com{x.permalink}",
                    "URL old.reddit": f"https://old.reddit.com{x.permalink}",
                    "Link URL": x.url,
                    "Text": x.selftext,
                    "Author": str(x.author),
                    "Type": "Submission",
                }
            )
        else:
            content.append(
                {
                    "Title": x.link_title,
                    "URL reddit": f"https://www.reddit.com{x.permalink}",
                    "URL old.reddit": f"https://old.reddit.com{x.permalink}",
                    "Link URL": x.link_url,
                    "Text": x.body,
                    "Author": str(x.author),
                    "Type": "Comment",
                }
            )
    return content


def extract_data(reddit, user_config):
    username = reddit.user.me().name
    user_data = []
    if "upvoted" in user_config:
        logger.info("Exporting upvoted content.")
        logger.debug(f"Extracting upvoted content for user {username}")
        data = reddit.user.me().upvoted(limit=None)
        user_data += create_dict(data)
        for item in user_data:
            item.update({"Action": "Upvoted"})
    if "saved" in user_config:
        logger.info("Exporting saved content.")
        logger.debug(f"Extracting saved content for user {username}")
        data = reddit.user.me().saved(limit=None)
        user_data += create_dict(data)
        for item in user_data:
            item.update({"Action": "Saved"})
    if "submissions" in user_config:
        logger.info("Exporting submitted content.")
        logger.debug(f"Extracting submitted content for user {username}")
        data = reddit.user.me().submissions.new(limit=None)
        user_data += create_dict(data)
        for item in user_data:
            item.update({"Action": "Submitted"})

    # Add data owner in list of dict.
    for item in user_data:
        item.update({"reddit_export_userdata Username": username})
    return user_data


def export_data(filename, extension, data):
    filename = filename + "." + extension
    # CSV format : all data fields with header.
    if extension == "csv":
        with open(filename, "w") as f:
            writer = csv.DictWriter(
                f, fieldnames=data[0].keys(), delimiter=";", quoting=csv.QUOTE_MINIMAL
            )
            writer.writeheader()
            writer.writerows(data)
    # TXT format : only urls, in a archivebox-compatible format (list of urls).
    elif extension == "txt":
        with open(filename, "w") as f:
            for i in data:
                f.write(i["reddit URL"] + "\n")
                f.write(i["old.reddit URL"] + "\n")
                if i["link URL"]:
                    f.write(i["link URL"] + "\n")


def main():
    args = parse_args()
    config = read_config(args.config_file)
    # Check if config is valid with the selected arguments.
    if not validate_config(config, args):
        raise Exception("Config is not valid.")

    # Get options from CLI arguments and/or config file.
    separate_export = args.separate_export or config["options"]["separate_export"]
    archivebox_export = args.archivebox_export or config["options"]["archivebox_export"]

    complete_data = []
    for user in config["users"]:
        logger.info(f"Exporting data for {user['username']}.")
        reddit = reddit_connect(user)
        user_config = user["exports"]
        complete_data += extract_data(reddit, user_config)

    # Export in a folder called "Exports".
    export_folder_name = "Exports"
    timestamp = int(time.time())
    Path(export_folder_name).mkdir(parents=True, exist_ok=True)
    # Separate export, one file per user.
    if separate_export:
        # Split complete_data by users.
        data = collections.defaultdict(list)
        for submission in complete_data:
            data[submission["reddit_export_userdata Username"]].append(submission)

        split_complete_data = list(data.values())
        for complete_data in split_complete_data:
            username = complete_data[0]["reddit_export_userdata Username"]
            if archivebox_export:
                filename = f"{export_folder_name}/reddit_export_userdata_{username}_archivebox_{timestamp}"
                export_data(filename, "txt", complete_data)
            else:
                filename = f"{export_folder_name}/reddit_export_userdata_{username}_{timestamp}"
                export_data(filename, "csv", complete_data)
    # Global export.
    else:
        if archivebox_export:
            filename = (
                f"{export_folder_name}/reddit_export_userdata_archivebox_{timestamp}"
            )
            export_data(filename, "txt", complete_data)
        else:
            filename = f"{export_folder_name}/reddit_export_userdata_{timestamp}"
            export_data(filename, "csv", complete_data)

    logger.info("Runtime : %.2f seconds." % (time.time() - start_time))


def parse_args():
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(
        description="reddit_export_userdata. Exports userdata of one or several reddit accounts."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-a",
        "--archivebox_export",
        help="Export only a list of urls (old.reddit, www.reddit and external links) in order to be used with archivebox.",
        dest="archivebox_export",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--separate_export",
        help="Export data in separate files for each reddit users.",
        dest="separate_export",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--config_file",
        help='Path to the config file (default: "config.yaml")',
        type=str,
        default="config.yaml",
    )
    parser.set_defaults(boolean_flag=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
