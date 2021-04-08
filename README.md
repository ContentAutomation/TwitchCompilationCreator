<p align="center">
    <a href="https://github.com/ContentAutomation"><img src="https://contentautomation.s3.eu-central-1.amazonaws.com/logo.png" alt="Logo" width="150"/></a>
    <br />
    <br />
    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-3C93B4.svg?style=flat" alt="MIT License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <br />
    <a href="https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ"><img src="https://img.shields.io/badge/YouTube-FF0000.svg?style=flat&logo=youtube" alt="Platform: YouTube"></a>
    <a href="https://www.twitch.tv/"><img src="https://img.shields.io/badge/Twitch-9146FF.svg?style=flat&logo=twitch&logoColor=white" alt="Platform: Twitch"></a>
    <a href="https://github.com/tensorflow/tensorflow"><img src="https://img.shields.io/badge/TensorFlow-FF6F00.svg?logo=tensorflow&logoColor=white" alt="Tensorflow"></a>
    <br />
    <a href="https://github.com/pallets/jinja"><img src="https://img.shields.io/badge/templating%20language-jinja2-12A5B8.svg" alt="Jinja"></a>
    <a href="https://github.com/streamlink/streamlink"><img src="https://img.shields.io/badge/stream%20handling-streamlink-8709B8.svg" alt="Streamlink"></a>
    <a href="https://github.com/Zulko/moviepy"><img src="https://img.shields.io/badge/video%20editing-MoviePy-87B812" alt="MoviePy"></a>
    <br />
    <br />
    <i>A fully automated system that transforms Twitch clips into gaming compilations</i>
    <br />
<br />
    <i><b>Authors</b>:
        <a href="https://github.com/ChristianCoenen">Christian C.</a>,
        <a href="https://github.com/DeadlySurprise">Moritz M.</a>,
        <a href="https://github.com/lucaSchilling">Luca S.</a>
    </i>
<br />
    <i><b>Related Projects</b>:
        <a href="https://github.com/ContentAutomation/NeuralNetworks">Neural Networks</a>,
        <a href="https://github.com/ContentAutomation/YouTubeUploader">YouTube Uploader</a>,
        <a href="https://github.com/ContentAutomation/YouTubeWatcher">YouTube Watcher</a>
    </i>
</p>
<hr />

## About
This is our approach of automatically creating compilations of twitch clips (focused on gaming).
We are very interested in YouTube, Twitch and Programming so we started this as an experiment, now a few months later we have to say it worked!

**What did we achieve?**
- We automatically uploaded over 100 videos to [our YouTube channel](https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ) without any human interaction
- [One video](https://www.youtube.com/watch?v=-YCSg11leck) got quite some traction by getting 2155 views and 48 likes at that point we had 0 Subscribers and it was the 8th video of the channel
- All our uploads combined got over 10k views
- We didn't receive a single comment indicating the use of bots

**So why do we publish this now instead of making money with it?**
- We came to the conclusion that we'd need to further optimize the videos to grow the channel which would require sophisticated and computationally expensive neural networks.
- We do not own the copyright of the clips so theoretically somebody could claim the video. To legally monetize the content, we'd need to add value to the clips like funny comments with a good text-to-speech framework.
- The language of some clips is declared as English by Twitch, even though the spoken language is not English. 
  To filter those clips, a computationally expensive neural network for language-detection is required.

It was only an experiment without the direct goal of making money with it. Additionally, we think it is more valuable for us as a reference.
If you are encountering any problems when running the code, feel free to open an [Issue](https://github.com/ContentAutomation/TwitchCompilationCreator/issues) or a [Pull Request](https://github.com/ContentAutomation/TwitchCompilationCreator/pulls) with a possible fix.


## Results
Example Video Screenshot            |  Example Thumbnail
:----------------------------------:|:-------------------------:
![](https://contentautomation.s3.eu-central-1.amazonaws.com/example-screenshot.png)            |  ![](https://contentautomation.s3.eu-central-1.amazonaws.com/example-thumbnail.jpg)

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

### apis.py
This class contains static methods to handle all API request for the Twitch and YouTube API.

### clip.py
This dataclass is used to convert json data from the Twitch API to Clip objects. This makes the data easier accessible within the python code.

### clip_handler.py
This class determines which Twitch clips the compilation will be made of and process them.
It will do the following:
- call the Twitch API to get the clip metadata
- check if clips are ingame by using a neural network
- process 100 clip metadata at a time and fetch more metadata if necessary
- download the clips one-by-one

### compilation.py
This class will use the clips from the ClipHandler to create a compilation of all clips with a logo and the name of the clip creator as overlay.
It will do the following:
- load all clips based on the metadata file
- create an overlay text for each clip
- composite all clips with their text and the logo
- compress the audio of the compilation so the sound is equaly high for the whole compilation
- render the finished compilation

### metadata.py
This class will handle/create all metadata that is needed for a YouTube upload.
It will do the following:
- handle the loading, saving, and storage of the metadata
- on every first load it will refresh the metadata. If clips got deleted in the raw_clips_dir it will remove them automatically from the metadata
- use a template to create YouTube title and description based on the metadata_config of the game and the metadata of that specific compilation
- create a thumbnail using a frame of one of the clips, a random emoji, the number of the playlists_items, a basic half transparent overlay, and the game logo

### parser.py
This script is only for the ArgumentParser that will be used in the main.py.
It simplifies the usage of the script by defining default values for every parameter aswell as types and help information.
All parameters are optional so the script runs without parameters but they all work and can be used. To read more about this checkout the [Run Parameters section](#run-parameters).

### utils.py
As the name indicates this script offers only utility functions.
Those functions are used in basically every other script or class.
It contains functions performing the following tasks:
- formatting a string into the correct string format
- adding any amount of seconds on top of a datetime.time value
- getting start and end datetimes for a given timespan (e.g. last hour, last week, ...)
- get a valid filename which removes all characters that may conflict with file handling operations
- get the full path to the game folder in our own directory structure for a given game
- get the full path of the previous compilation of a given game
- create our directory structure 
- delete the whole directory structure
- saving and loading txt aswell as json files

## Run Parameters
All of these parameters are optional and a default value will be used if they are not defined. 
You can also get these definitions by running ```main.py --help```

```
-h, --help            show this help message and exit
-g GAME, --game GAME  
                      Declares for which game the compilation should be created. It uses fortnite as default
-ap ASSET_PATH, --asset_path ASSET_PATH
                      Path to the assets folder. If not declared it uses './assets' as default
-noc NUMBER_OF_CLIPS, --number_of_clips NUMBER_OF_CLIPS
                      How many clips should be used. For most use cases -ml will fit better since the length of clips can be between 1-60 seconds so a -noc 5 compilation could be 5 or 300 seconds long
-ts {day,week,month}, --timespan {day,week,month}
                      ['hour', 'day', 'week', 'month'] - timespan from when the clips should be taken. Default is week
-la LANGUAGE, --language LANGUAGE
                      Language of the clips. Default is en
-ml MIN_LENGTH, --min_length MIN_LENGTH
                      Length of the compilation in seconds. Default is 360 (6 minutes)
-mcc MAX_CREATOR_CLIPS, --max_creator_clips MAX_CREATOR_CLIPS
                      Number of clips used from a single creator. Default is 2
-mcd MIN_CLIP_DURATION, --min_clip_duration MIN_CLIP_DURATION
                      Minimal clip length. Default is 10
-o OUTPUT_PATH, --output_path OUTPUT_PATH
                      Output path - default is './TwitchClips'. This should not start with a '/', otherwise it will use it as an absolute path


```
