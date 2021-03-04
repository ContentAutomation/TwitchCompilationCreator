import argparse


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        "--game",
        type=str,
        default="fortnite",
        help="Declares for which game the compilation should be created. It uses fortnite as default",
        required=False,
    )
    parser.add_argument(
        "-ap",
        "--asset_path",
        type=str,
        default="assets",
        help="Path to the assets folder. If not declared it uses './assets' as default",
        required=False,
    )
    parser.add_argument(
        "-noc",
        "--number_of_clips",
        type=int,
        default=None,
        help="How many clips should be used. For most use cases -ml will fit better since the length of clips can be between 1-60 seconds so a -noc 5 compilation could be 5 or 300 seconds long",
        required=False,
    )
    parser.add_argument(
        "-ts",
        "--timespan",
        type=str,
        default="week",
        choices=["day", "week", "month"],
        help="['hour', 'day', 'week', 'month'] - timespan from when the clips should be taken. Default is week",
        required=False,
    )
    parser.add_argument(
        "-la",
        "--language",
        type=str,
        default="en",
        help="Language of the clips. Default is en",
        required=False,
    )
    parser.add_argument(
        "-ml",
        "--min_length",
        type=int,
        default=360,
        help="Length of the compilation in seconds. Default is 360 (6 minutes)",
        required=False,
    )
    parser.add_argument(
        "-mcc",
        "--max_creator_clips",
        type=int,
        default=2,
        help="Number of clips used from a single creator. Default is 2",
        required=False,
    )
    parser.add_argument(
        "-mcd",
        "--min_clip_duration",
        type=int,
        default=10,
        help="Minimal clip length. Default is 10",
        required=False,
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        default="TwitchClips",
        help="Output path - default is './TwitchClips'. This should not start with a '/', otherwise it will use it as an absolute path",
        required=False,
    )
    return parser
