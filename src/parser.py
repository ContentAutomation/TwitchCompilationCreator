import argparse


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        "--game",
        type=str,
        default="fortnite",
        help="declares for which game the compilation should be created it uses fortnite as default",
        required=False,
    )
    parser.add_argument(
        "-ap",
        "--asset_path",
        type=str,
        default="assets",
        help="assets path if not declared it uses assets as default",
        required=False,
    )
    parser.add_argument(
        "-noc",
        "--number_of_clips",
        type=int,
        default=None,
        help="how many clips should be used but its better to use min_length instead",
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
        help="language of the clips. Default is en",
        required=False,
    )
    parser.add_argument(
        "-ml",
        "--min_length",
        type=int,
        default=360,
        help="length of the compilation. Default is 360 which are 6 minutes",
        required=False,
    )
    parser.add_argument(
        "-mcc",
        "--max_creator_clips",
        type=int,
        default=2,
        help="amount of clips used from a single creator. Default is 2",
        required=False,
    )
    parser.add_argument(
        "-mcd",
        "--min_clip_duration",
        type=int,
        default=10,
        help="miminal amount of seconds a clip should have. Default is 10",
        required=False,
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        default="TwitchClips",
        help="output path - default is TwitchClips. This should not start with a / otherwise it will use it as absolute path",
        required=False,
    )
    return parser
