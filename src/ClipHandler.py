import logging
import os
from pathlib import Path

import numpy as np
import requests
import streamlink
import tensorflow as tf
from moviepy.editor import VideoFileClip

import config
from src import utils
from src.APIHandler import APIHandler
from src.Clip import Clip
from src.MetadataHandler import MetadataHandler


class ClipHandler:
    clips = []
    retries = 3

    def __init__(self, game: str, asset_path: str, output_path: str):
        self.output_path = output_path
        self.game = game
        self.game_id = APIHandler.get_twitch_game_id(self.game)
        self.raw_clips_dir = utils.get_game_path(config.DIRECTORIES["raw_clips_dir"], self.game, output_path)
        self.compilation_dir = utils.get_game_path(config.DIRECTORIES["compilation_dir"], self.game, output_path)
        self.base_dir = utils.get_game_path("", self.game, output_path)
        self.pagination = ""
        self.clips = []
        self.mdh = MetadataHandler(self.game, asset_path, output_path)
        self.current_length = 0
        self.streamer_blocklist = utils.load_json_file("blocklist.json")["streamers"]

        model_file_path = Path(os.path.join(asset_path, utils.get_valid_game_name(self.game), "game_detection.h5"))

        try:
            self.model = tf.keras.models.load_model(model_file_path)
        except IOError:
            logging.warning(f"Could not load model from {model_file_path}. Programm will proceed without a model -> all clips are considered ingame. You can download a test model from https://github.com/ContentAutomation/TwitchCompilationCreator/releases/latest")
            self.model = None
    

    def get_clips(self, timespan: str, language: str, **kwargs):
        utils.make_dirs(self.game, self.output_path)
        self.get_game_clips(utils.get_headers(), timespan, language, kwargs)
        self.mdh.create_metadata({"clips": self.clips, "number_in_series": None})

    def is_ingame_clip(self, clip: VideoFileClip) -> bool:
        if self.model:
            frames = []
            # clip = VideoFileClip(clip_path)
            for t in range(1, int(clip.duration)):
                frame = clip.get_frame(t)
                resized_frame = tf.keras.preprocessing.image.smart_resize(frame, (224, 224), interpolation="nearest")
                frames.append(resized_frame)
            # predictions[0] = game, predictions[1] = nogame
            predictions = self.model.predict(np.array(frames))
            percentage = np.average(predictions, axis=0)
            clip.close()
            return percentage[0] > 0.8
        else:
            logging.warning("No model for prediction available -> every clip is chosen as valid (ingame)")
            return True

    def get_game_clips(self, headers: dict, timespan: str, language: str, filter_information: dict):
        creator_counts = {}
        times = utils.get_start_end_time(timespan)

        while not self.is_required_length(filter_information):
            if self.pagination is None:
                break
            url = f"https://api.twitch.tv/helix/clips"
            payload = {"game_id": self.game_id, "ended_at": times["ended_at"], "started_at": times["started_at"], "after": self.pagination, "first": 100}
            resp = requests.get(url, headers=headers, params=payload)
            if resp.status_code == 200:
                logging.info("Status Code: 200 -> handling response data now")
                self.handle_response_data(resp.json(), language, creator_counts, filter_information)
                self.retries = 3
            elif resp.status_code == 401:
                self.retries -= 1
                logging.warning(f"Status Code: 401 -> retrying with new token for {self.retries} more times")
                if self.retries > 0:
                    return self.get_game_clips(utils.get_headers(), timespan, language, filter_information)
                else:
                    raise ConnectionRefusedError("Authentication problem occurred. "
                                                 "Couldn't fetch clip data after three tries")
            else:
                logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")

    def is_required_length(self, filter_information: dict) -> bool:
        number_of_clips = filter_information.get("number_of_clips", None)
        min_length = filter_information.get("min_length", None)
        if number_of_clips:
            return len(self.clips) >= number_of_clips
        elif min_length:
            return self.current_length >= min_length
        else:
            logging.warning("number_of_clips/min_length parameter are both not initialized -> is_required_length==True")
            return False

    def handle_response_data(self, resp: dict, language: str, creator_counts: dict, filter_information: dict):
        self.pagination = resp.get("pagination", None).get("cursor", None)
        logging.info(f"New pagination: {self.pagination}")
        data: list = resp["data"]
        max_creator_clips = filter_information.get("max_creator_clips", 2)

        def filter_func(clip):
            broadcaster = clip["broadcaster_id"]
            creator_counts[broadcaster] = creator_counts.get(broadcaster, 0) + 1
            return (
                clip["game_id"] == str(self.game_id)
                and clip["language"].startswith(language)
                and creator_counts[broadcaster] <= max_creator_clips
                and clip["broadcaster_name"] not in self.streamer_blocklist
            )

        data = list(filter(filter_func, data))
        for clip in data:
            if self.is_required_length(filter_information):
                logging.info("Required length reached")
                break
            clip_path = self.download_clip(clip)
            if not clip_path:
                logging.warning("clip_path not available -> will get skipped")
                break
            video_clip = VideoFileClip(clip_path)
            min_clip_duration = filter_information.get("min_clip_duration", 10)
            if video_clip.duration < min_clip_duration:
                logging.warning(f"The Clip is only {video_clip.duration}s long -> will get skipped")
                if os.path.isfile(clip_path):
                    video_clip.close()
                    os.remove(clip_path)
                break
            if self.is_ingame_clip(video_clip):
                current_clip = Clip(**clip)
                logging.info(f"Adding new valid clip: {current_clip.title} by {current_clip.broadcaster_name}")
                current_clip.duration = video_clip.duration
                self.current_length += video_clip.duration
                current_clip.clip_id = "{0:0=3d}".format(len(self.clips))
                self.clips.append(current_clip)
            else:
                logging.info("Clip is not ingame -> remove clip")
                if os.path.isfile(clip_path):
                    video_clip.close()
                    os.remove(clip_path)

    def download_clip(self, clip: dict):
        output_file = os.path.join(self.raw_clips_dir, utils.get_valid_file_name("{0:0=3d}".format(len(self.clips))) + ".mp4")
        try:
            stream = streamlink.streams(clip["url"])["best"]
        except TypeError:
            logging.info("Clip has no broadcaster or displayName -> will be skipped")
            return None
        with open(output_file, "wb") as f, stream.open() as fd:
            while True:
                data = fd.read(1024)
                if not data:
                    break
                f.write(data)
        return output_file
