<p align="center">
    <a href="https://github.com/ContentAutomation"><img src="https://contentautomation.s3.eu-central-1.amazonaws.com/logo.png" alt="Logo" width="150"/></a>
    <br />
    <br />
    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-3C93B4.svg?style=flat" alt="MIT License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <br />
    <br />
    <i>Implementation of a System that creates Compilations from Twitch clips fully automated </i>
    <br />
<br />
    <i><b>Authors</b>:
        <a href="https://github.com/ChristianCoenen">Christian Coenen</a>,
        <a href="https://github.com/DeadlySurprise">Moritz Mundhenke</a>,
        <a href="https://github.com/lucaSchilling">Luca Schilling </a>
    </i>
</p>
<hr />

This is our approach of automatically creating compilations of twitch clips(focused on gaming).
We are very interested in YouTube, Twitch and Programming so we started this as an experiment, now a few months later we have to say it worked!

What did we achieve?
- We automatically uploaded over 100 videos to youtube without any interaction from us
- One video went kind of viral by getting 2155 views and 48 likes at that point we had 0 Subscribers and it was the 8th video of the channel
- Summarized over all videos we got over 10k views
- Not a single comment asked if we are a bot channel or any similar

So why do we publish this now instead of making money with it?
- We come to the conclusion even though optimizing the clip selection by using a rating neural network would be possible it would be quiet expensive.
- We do not own the copyright of the clips so theoretically somebody could claim the video. To monetize this we would have needed to add some own work to the clips to use them legally. Maybe by commentating with a good text-to-speech framework.
- The language of some clips is declared as english by twitch but is not english so for this we would have needed to use a language-detection ai which is also quiet expensive.

Since this was only an experiment and we are all students without any income we ended it here and made it public as a reference and maybe somebody will continue our work.
If you are interested in that feel free to message us via github.

## Table of content
- [Results](#results)
- [Setup](#setup)
- [Script Explanations](#script-explanations)
    - [APIHandler](#apihandlerpy)
    - [Clip](#clippy)
    - [ClipHandler](#cliphandlerpy)
    - [MetadataHandler](#metadatahandlerpy)
    - [ClipCompilationCreator](#clipcompilationcreatorpy)
    - [parser.py](#parserpy)
    - [utils.py](#utilspy)
- [Run Parameters](#run-parameters)

## Results
Example Video Screenshot            |  Example Thumbnail
:----------------------------------:|:-------------------------:
![](https://github.com/ContentAutomation/Twitch-Clip-Compilation-Creator/blob/READMEImages/assets/READMEImages/example-screenshot.png)            |  ![](https://github.com/ContentAutomation/Twitch-Clip-Compilation-Creator/blob/READMEImages/assets/READMEImages/example-thumbnail.jpg)

### Example Description
```html
[Fortnite] Twitch Highlights #10 | Fails, Satisfying/Funny Moments & Epic Wins!

🔔 SUBSCRIBE FOR MORE FORTNITE FAILS/WINS!
https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ?sub_confirmation=1

Welcome back to episode 10 of Daily Gaming Highlights | Fortnite!
We have some insane clips this episode.
If you liked and enjoyed the video be sure to leave a like and subscribe for more Fortnite content!
We upload a Fortnite video every monday once a week.
Also be sure to comment letting us know which your favorite clip was 😄

Featured Playlists:
• Daily Gaming Highlights: https://www.youtube.com/playlist?list=PLhOg0bYb-2IKbbV4rHerrtlWArm14bXdI
• Fortnite Highlights: https://www.youtube.com/playlist?list=PLhOg0bYb-2IICWc4MB-ZetkKGMTSvanye

🎬Featured clips/streamers:
Streamer1: https://clips.twitch.tv/AwkwardProtectiveDoritosChip
Streamer2: https://clips.twitch.tv/WimpyGleamingTTours

00:00 Streamer1
00:11 Streamer2

Golden Gorilla does not have the copyrights for the used clips.
If you are within a video and would like to get it removed please email us:
highlightsforgaming@gmail.com

#GoldenGorilla #Fortnite #Fails #FunnyMoments #EpicMoments #Wins #EpicWins
#fortnitebattleroyale #season4 #twitch
```

## Setup
This project requires [Poetry](https://python-poetry.org/) to install the required dependencies.
Check out [this link](https://python-poetry.org/docs/) to install Poetry on your operating system.

Make sure you have installed [Python](https://www.python.org/downloads/) 3.8 or higher! Otherwise Step 3 will let you know that you have no compatible Python version installed.

1. Clone/Download this repository
2. Navigate to the root of the repository
3. Run ```poetry install``` to create a virtual environment with Poetry
4. Follow the [twitch api docs](https://dev.twitch.tv/docs/authentication#registration) until you get your own CLIENT_ID and CLIENT_SECRET
5. Follow the [youtube data api docs](https://developers.google.com/youtube/v3/getting-started) until you receive an API key
6. Insert your Twitch(CLIENT_ID, CLIENT_SECRET) and your YouTube(API_KEY) into the config.py it should look like the following
<br>
<span style="color:red">HINT: The example keys do not work</span>.

```python
# For the Twitch API
CLIENT_ID = "o42tebpdzmj5z811iycgcpmd82on24"
CLIENT_SECRET = "owdgx64t1dodleiuo49e5rg7rvk5iq"

# For the YoutTube API
API_KEY = "h5UYdzJHeZNWLTgGteh0J68k7icp9jp9vPJlbzF"
```
7. Run ```poetry run python main.py``` to run the program. Alternatively you can run ```poetry shell``` followed by ```python main.py```
8. Enjoy :)

## Script Explanations

### APIHandler.py
This class contains static methods to handle all API request for the Twitch and YouTube API.

### Clip.py
This dataclass is used to convert json data from twitch into our own class.
It defines all type hint and enables us to use the data a lot easier in other methods.

### ClipHandler.py
This class is built to handle all of the twitch clips.
It will do the following:
- call the Twitch API to get clip metadata
- check if clips are ingame by using a neural network
- process 100 clip metadata at a time and fetch more metadata if necessary
- download the clips one-by-one

### MetaDataHandler.py
This class will handle/create all metadata that is needed for a youtube upload.
It will do the following:
- handle the loading and saving of the metadata
- maintain the metadata so it only has to be loaded once per run of the script
- on every first load it will refresh the metadata if clips got deleted in the raw_clips_dir it will remove them automatically from the metadata aswell
- use a template to create yt title and yt description based on the metadata_config of the game and the metadata of that specific compilation
- create a thumbnail using frame of one of the clips, a random emoji, the number of the playlists_items, a basic half transparent overlay and the game logo

### ClipCompilationCreator.py
This class will use the clips from the ClipHandler to create a compilation of all clips with a logo and the name of the clip creator as overlay.
It will do the following:
- load all clips based on the metadata file
- create an overlay text for each clip
- composite all clips with their text and the logo
- compress the audio of the compilation so the sound is equaly high for the whole compilation
- render the finished compilation

### parser.py
This script is only for the ArgumentParser that will be used in the main.py.
It makes the usage of the script easy by defining default values for every parameter aswell as types and help information.
All parameters are optional so the script runs without parameters but they all work and can be used to read more about this checkout the [Run Parameters section](#run-parameters).

### utils.py
As the name indicated this script offers only utility functions.
Those functions are used in basically every other script or class.
There are functions for the following in there:
- formatting a string into the correct string format
- adding any amount of seconds on top of a datetime.time value
- getting start and end datetimes for a given timespan e.g. last hour last week etc.
- get a valid filename which removes all characters that may conflict with file handling operations
- get the full path to the game folder in our own directory structure for a given game
- get the full path of the previous compilation of a given game
- create our directory structure 
- delete the whole directory structure
- saving and loading txt aswell as json files

## Run Parameters
All of these parameters are optional and a default value will be used if not they are not defined. 
You can also get these definitions by running ```main.py --help```

##### -h, --help
show this help message and exit

##### -g GAME, --game GAME  
declares for which game the compilation should be created it uses fortnite as default

##### -ap ASSET_PATH, --asset_path ASSET_PATH
assets path if not declared it uses assets as default
  
##### -noc NUMBER_OF_CLIPS, --number_of_clips NUMBER_OF_CLIPS
how many clips should be used but its better to use min_length instead
 
##### -ts {day,week,month}, --timespan {day,week,month}
['hour', 'day', 'week', 'month'] - timespan from when the clips should be taken. Default is week
  
##### -la LANGUAGE, --language LANGUAGE
language of the clips. Default is en
  
##### -ml MIN_LENGTH, --min_length MIN_LENGTH
length of the compilation. Default is 360 which are 6 minutes
  
##### -mcc MAX_CREATOR_CLIPS, --max_creator_clips MAX_CREATOR_CLIPS
amount of clips used from a single creator. Default is 2
  
##### -mcd MIN_CLIP_DURATION, --min_clip_duration MIN_CLIP_DURATION
miminal amount of seconds a clip should have. Default is 10
  
##### -o OUTPUT_PATH, --output_path OUTPUT_PATH
output path - default is TwitchClips. This should not start with a / otherwise it will use it as absolute path
