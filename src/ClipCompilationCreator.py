from src import utils
from src.MetadataHandler import MetadataHandler
import config

from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, TextClip, afx
from moviepy.tools import subprocess_call
import logging
import os


class ClipCompilationCreator:
    def __init__(self, game: str, asset_path: str, output_path: str):
        self.output_path = output_path
        self.game = game
        self.raw_clips_dir = utils.get_game_path(config.DIRECTORIES["raw_clips_dir"], self.game, output_path)
        self.compilation_dir = utils.get_game_path(config.DIRECTORIES["compilation_dir"], self.game, output_path)
        self.overlay = os.path.join(asset_path, str(self.game), "watermark.png")
        self.mdh = MetadataHandler(self.game, asset_path, output_path)
        self.metadata = self.mdh.get_metadata()
        self.target_res = (1920, 1080)
        self.compressor_settings = dict(threshold="-12dB", ratio=9, attack=200, release=1000)

    def create_compilation(self):
        clips = self.load_clips()
        logging.info(f"Creating compilation from {len(clips)} clips")
        composite_clips = list(self.composite_clips(clips).values())
        compilation = concatenate_videoclips(composite_clips)
        raw_audio_path = os.path.join(self.compilation_dir, "output.base.mp4")
        final_audio_path = os.path.join(self.compilation_dir, "output.mp4")
        self.mdh.create_thumbnail(self.metadata["clips"][-2])
        compilation.write_videofile(raw_audio_path, audio_codec="aac")

        if self.compressor_settings:
            logging.info("Compressing compilation audio")
            self.ffmpeg_compress_audio(raw_audio_path, final_audio_path)
            os.remove(raw_audio_path)
        else:
            os.rename(raw_audio_path, final_audio_path)

        self.mdh.create_youtube_description()
        self.mdh.create_youtube_title()

    def write_clips(self):
        clips = self.load_clips()
        logging.info(f"Creating edited individual clips from {len(clips)} clips")
        composite_clips = self.composite_clips(clips)

        for idx, (clip_id, clip) in enumerate(composite_clips.items()):
            logging.info(f"Clip {clip_id} of {len(clips)}")
            raw_audio_path = os.path.join(self.compilation_dir, f"clip_{clip_id}.base.mp4")
            final_audio_path = os.path.join(self.compilation_dir, f"clip_{clip_id}.mp4")
            clip.write_videofile(raw_audio_path, audio_codec="aac")

            if self.compressor_settings:
                logging.info("Compressing clip audio")
                self.ffmpeg_compress_audio(raw_audio_path, final_audio_path)
                os.remove(raw_audio_path)
            else:
                os.rename(raw_audio_path, final_audio_path)

    def composite_clips(self, clips: dict):
        try:
            watermark = ImageClip(self.overlay).set_position((0.7, 0.1), relative=True)
        except FileNotFoundError:
            logging.warning("No watermark found -> video will be created without watermark")
            watermark = None

        # Requires metadata about the clip
        txts = self.generate_clip_text(self.metadata)

        composite_clips = {}
        for clip_id, clip in clips.items():
            composition = []
            duration = clip.duration
            composition.append(clip)

            if watermark:
                composition.append(watermark.set_duration(duration))
            composition.append(txts[clip_id].set_duration(duration))
            composite_clips[clip_id] = CompositeVideoClip(composition, size=self.target_res)
        return composite_clips

    def generate_clip_text(self, metadata: dict) -> dict:
        txt_clips = {}
        for clip in metadata["clips"]:
            txt = TextClip(
                f"Creator: {clip['broadcaster_name']}",
                fontsize=60,
                font="Myriad Pro",
                stroke_color="black",
                stroke_width=2,
                color="white",
            ).set_position(("center", "bottom"))
            txt_clips[clip["clip_id"]] = txt
        return txt_clips

    def load_clips(self) -> dict:
        clips = {}
        for data in self.metadata["clips"]:
            clip_path = os.path.join(self.raw_clips_dir, f"{data['clip_id']}.mp4")
            if os.path.isfile(clip_path):
                clip_res = self.target_res[
                    ::-1
                ]
                # VideoFileClip uses height x width instead of the reverse for some reason
                # audio_normalize can't handle videos without sound
                # if a clip has no audio, it will get added without sound and doesn't need audio normalization
                try:
                    clips[data["clip_id"]] = VideoFileClip(clip_path, target_resolution=clip_res).afx(
                        afx.audio_normalize
                    )
                except ZeroDivisionError:
                    logging.warning("Can't normalize clip because it has no Audio -> will be added without audio")
                    clips[data["clip_id"]] = VideoFileClip(clip_path, target_resolution=clip_res)
        return clips

    def ffmpeg_compress_audio(self, file: str, output: str):
        threshold = self.compressor_settings["threshold"]
        ratio = self.compressor_settings["ratio"]
        attack = self.compressor_settings["attack"]
        release = self.compressor_settings["release"]
        cmd = [
            "ffmpeg",
            "-i",
            file,
            "-c:v",
            "copy",  # Copy video to avoid re-encoding
            "-af",
            f"acompressor=threshold={threshold}:ratio={ratio}:attack={attack}:release={release}",
            output,
        ]

        subprocess_call(cmd)
