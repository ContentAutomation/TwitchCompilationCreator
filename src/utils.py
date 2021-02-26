import json
import logging
import os
import re
import shutil
from datetime import datetime, timezone, timedelta, time
from typing import Union

import config
from src.APIHandler import APIHandler


def get_date_string(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


# Adds a specific amount of seconds ontop of the given time under consideration of all time/date rules
def time_plus(time: time, timedelta: timedelta) -> time:
    start = datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)
    end = start + timedelta
    return end.time()


# Returns the start and end time of a specific timespan
# hour = last hour, week = last week etc.
def get_start_end_time(timespan: str) -> dict:
    ended_at = datetime.now(timezone.utc).astimezone() - timedelta(hours=2)
    if timespan == "hour":
        started_at = ended_at - timedelta(hours=1)
    elif timespan == "week":
        started_at = ended_at - timedelta(days=7)
    elif timespan == "month":
        started_at = ended_at - timedelta(weeks=4)
    elif timespan != "hour" and timespan != "week" and timespan != "month":
        started_at = ended_at - timedelta(hours=1)
    return dict(started_at=get_date_string(started_at), ended_at=get_date_string(ended_at))


def get_valid_file_name(name: str) -> str:
    return re.sub("[^0-9a-zA-Z]+", "", name)


def get_game_path(folder: str, game: str, output_path: str) -> str:
    date = datetime.now(timezone.utc).astimezone()
    return os.path.join(output_path, "media", get_valid_game_name(game), date.strftime("%Y_%m_%d"), folder)


# Returns the path to the folder of the previous compilation of that game
def get_previous_path(game: str, output_path: str) -> Union[str, None]:
    game_folder = get_valid_game_name(game)
    current_path = get_game_path("", game_folder, output_path)
    # scandir does not guarantee alphabetical order, so sort and reverse to find the newest entry
    entries = sorted(os.scandir(os.path.join(output_path, "media", game_folder)), key=lambda dir: dir.name)
    for entry in reversed(entries):
        # Ignore files (just check dirs)
        if not os.path.isdir(entry):
            continue
        try:
            # samefile will throw if the current directory has not been created yet
            if os.path.samefile(current_path, entry.path):
                continue
        except:
            pass
        return entry
    logging.error("There is no prevoious game path for this game -> return None")
    return None


# Creates all directories which are defined in the config.py
# They will be created in the correct game and date subfolders, they will also get created if the are not there yet
def make_dirs(game: str, output_path: str):
    for directory in config.DIRECTORIES:
        path = get_game_path(config.DIRECTORIES[directory], game, output_path)
        if not os.path.exists(path):
            logging.info(f"Creating following path: {path}")
            os.makedirs(path)
            os.chmod(path, 0o777)


# This removes all Folders that are created by this programm
# Be careful with the use of this it will remove every child folder aswell
def clean_directory(game: str, output_path: str):
    shutil.rmtree(get_game_path(config.DIRECTORIES["raw_clips_dir"], get_valid_game_name(game), output_path))


def load_txt_file(path: str) -> str:
    if os.path.isfile(path):
        with open(path, "r", encoding="utf8") as file:
            return file.read()
    else:
        return ""


def load_json_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        result_json = json.load(f)
        return result_json


def save_txt_file(path: str, data: str):
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)


def save_json_file(path: str, data: dict):
    def obj_dict(obj):
        return obj.__dict__

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=obj_dict)


def load_token() -> str:
    if os.path.isfile("token"):
        with open("token", "r") as infile:
            logging.info("got token from file")
            return infile.read()
    else:
        return APIHandler.get_new_twitch_token()


# Returns a valid game name which is in camelcase and doesnt contain any characters that are not possible in foldernames
def get_valid_game_name(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9]+", " ", name).title().replace(" ", "")
    return name[0].lower() + name[1:]


def get_headers() -> dict:
    headers = {"Client-ID": config.CLIENT_ID, "Authorization": "Bearer " + load_token()}
    logging.info(headers)
    return headers
