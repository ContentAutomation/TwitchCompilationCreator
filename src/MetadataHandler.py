import logging
import os
import random
from datetime import time, timedelta

from jinja2 import Environment, FileSystemLoader
from moviepy.editor import ImageClip, CompositeVideoClip, VideoFileClip, TextClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate

import config
from src import Clip
from src import utils
from src.APIHandler import APIHandler


class MetadataHandler:
    def __init__(self, game: str, asset_path: str, output_path: str):
        self.output_path = output_path
        self.game = game
        self.asset_path = asset_path
        self.descriptions_dir = utils.get_game_path(config.DIRECTORIES["descriptions_dir"], self.game, output_path)
        self.compilation_dir = utils.get_game_path(config.DIRECTORIES["compilation_dir"], self.game, output_path)
        self.raw_clips_dir = utils.get_game_path(config.DIRECTORIES["raw_clips_dir"], self.game, output_path)
        self.metadata_config = None
        self.metadata = None
        self.env = Environment(loader=FileSystemLoader(os.path.join(self.asset_path, "templates")), trim_blocks=True, lstrip_blocks=True)

    def create_metadata(self, data: dict):
        logging.info("Saving metadata.json")
        utils.save_json_file(os.path.join(self.compilation_dir, "metadata.json"), data)

    def get_metadata_config(self) -> dict:
        if self.metadata_config:
            return self.metadata_config
        else:
            logging.info("Loading metadata_config.json")
            self.metadata_config = utils.load_json_file(
                os.path.join(self.asset_path, utils.get_valid_game_name(self.game), "metadata_config.json")
            )
            return self.metadata_config

    def get_metadata(self) -> dict:
        if self.metadata:
            return self.metadata
        else:
            logging.info("Loading metadata.json")
            self.metadata = utils.load_json_file(os.path.join(self.compilation_dir, "metadata.json"))
            # If the metadata is still a list this means its an older version of metadata and will be automatically converted
            if type(self.metadata) is list:
                logging.warning("metadata.json was still in the old format -> will be converted")
                self.metadata = {"clips": self.metadata, "number_in_series": None}
                self.create_metadata(self.metadata)
            self.refresh_metadata()
            return self.metadata

    # Refreshing the metadata.json so it only contains metadata from clips that are still in the raw_clips folder
    # This will always be called whenever the metadata.json gets loaded from the harddrive
    # If you manually delete a clip you dont have to do anything to the metadata.json it will automatically be updated
    def refresh_metadata(self):
        logging.info("Refreshing Metadata")
        updated_clips = []
        metadata = self.get_metadata()
        clips = metadata["clips"]
        for data in clips:
            if os.path.isfile(os.path.join(self.raw_clips_dir, data["clip_id"] + ".mp4")):
                updated_clips.append(data)
        new_metadata = {"clips": updated_clips, "number_in_series": self.get_number_in_series()}
        self.create_metadata(new_metadata)
        self.metadata = new_metadata

    def get_youtube_description(self) -> str:
        return utils.load_txt_file(os.path.join(self.compilation_dir, "description_yt.txt"))

    def get_instagram_description(self, clip: Clip) -> str:
        return utils.load_txt_file(
            os.path.join(self.descriptions_dir, utils.get_valid_file_name(f"{str(clip.clip_id)}{clip.id}.txt"))
        )

    def get_youtube_title(self) -> str:
        return utils.load_txt_file(os.path.join(self.compilation_dir, "title_yt.txt"))

    # Returns the current number of videos in a specified yt playlist, if no video is in the playlist it will default to 1
    def get_number_in_series(self) -> int:
        metadata = self.get_metadata()
        metadata_config = self.get_metadata_config()
        if not metadata["number_in_series"]:
            playlist_id = metadata_config.get("playlist_id", None)
            return APIHandler.get_yt_playlist_size(playlist_id) + 1 if playlist_id else 1
        else:
            return metadata["number_in_series"]

    # Created a youtube description based on the defined metadata_config and the compilation metadata
    def create_youtube_description(self):
        logging.info("Creating yt description")
        metadata = self.get_metadata()
        metadata_config = self.get_metadata_config()
        clips = metadata["clips"]
        start_time = time(minute=0, second=0, microsecond=0)
        for clip in clips:
            clip["start_time"] = start_time.strftime("%M:%S")
            start_time = utils.time_plus(start_time, timedelta(seconds=round(clip["duration"])))
        template = self.env.get_template("template_yt.txt")
        metadata_config["top_line"] = metadata_config["top_line"].replace("1", str(metadata["number_in_series"]))
        utils.save_txt_file(
            os.path.join(self.compilation_dir, "description_yt.txt"),
            template.render(
                episode_number=metadata["number_in_series"],
                clips=clips,
                config=metadata_config,
                game_uc=metadata_config["game"].upper(),
                channel_name_stripped=metadata_config["channel_name"].replace(" ", ""),
            ),
        )

    def create_youtube_title(self):
        logging.info("Creating yt title")
        metadata = self.get_metadata()
        metadata_config = self.metadata_config
        template = self.env.get_template("template_yt_title.txt")
        utils.save_txt_file(
            os.path.join(self.compilation_dir, "title_yt.txt"),
            template.render(episode_number=metadata["number_in_series"], config=metadata_config),
        )

    # Loads a random emoji from the assets/emoji folder which will be used for the thumbnail
    def get_emoji(self) -> ImageClip:
        emoji = random.choice(os.listdir(os.path.join(self.asset_path, "emojis")))
        return (
            ImageClip(os.path.join(self.asset_path, "emojis", emoji))
            .fx(resize, 2.0)
            .fx(rotate, -25)
            .set_position(("right", "top"), relative=True)
        )

    def get_number_textclip(self) -> TextClip:
        metadata = self.get_metadata()
        return TextClip(
            f"#{metadata['number_in_series']}",
            fontsize=130,
            font="Arial-Bold",
            color="gold4",
        ).set_position((0.04, 0.8), relative=True)

    def get_thumbnail_base(self, clip: Clip) -> ImageClip:
        clip_path = os.path.join(self.raw_clips_dir, f"{clip['clip_id']}.mp4")
        video = VideoFileClip(clip_path)
        thumbnail_base = video.get_frame(round(clip["duration"] / 2))
        video.close()
        return resize(ImageClip(thumbnail_base), [1280, 720])

    def create_thumbnail(self, clip: Clip):
        logging.info("Creating yt thumbnail")
        thumbnail_base = self.get_thumbnail_base(clip)
        emoji = self.get_emoji()
        overlay = ImageClip(os.path.join(self.asset_path, "overlay_thumbnail.png")).set_opacity(0.8)
        number = self.get_number_textclip()
        try:
            logo = (
                ImageClip(os.path.join(self.asset_path, utils.get_valid_game_name(self.game), "game_logo.png"))
                .fx(resize, 1.3)
                .set_position((0.04, 0.6), relative=True)
            )
        except FileNotFoundError:
            logging.warning("No game_logo in associated asset folder -> thumbnail will be created without logo")
            logo = None
        thumbnail = [
            thumbnail_base.set_duration(None),
            emoji.set_duration(None),
            overlay.set_duration(None),
            number.set_duration(None),
        ]
        if logo:
            thumbnail.append(logo.set_duration(None))
        thumbnail_result = CompositeVideoClip(thumbnail, size=[1280, 720])
        thumbnail_result.save_frame(os.path.join(self.compilation_dir, "thumbnail.png"), t=0, withmask=True)
