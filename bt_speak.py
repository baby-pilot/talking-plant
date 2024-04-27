'''
Implements speaking capability for the plant via bluetooth
'''

from gtts import gTTS
from enum import Enum
import time
import vlc
from datetime import datetime

# ## --------------------------------------  Generate scripts  ---------------------------------------------
# tts = gTTS("hello, I am raspberry pi 4. This is a test with Google Text to speech (gTTS)")
# tts.save("hello.mp3")

water_alert = gTTS("Hey this is your plant speaking, please water me.")
water_alert.save("water_alert.mp3")

uv_alert = gTTS("Hey, it's me again, can you please move me, I need some sunshine.")
uv_alert.save("uv_alert.mp3")

defense_alert = gTTS("It's me, plant, you gotta defend me, I'll be eaten!")
defense_alert.save("defense_alert.mp3")

## ------------------------------------------------------------------------------------------------------

# can use mpg123 on rasp pi to play the file above manually from command line
class AlertMode(Enum):
    NEED_WATER = "water_alert.mp3"
    NEED_UV = "uv_alert.mp3"
    NEED_DEFENSE = "defense_alert.mp3"


def generateAndPlay(message) -> None:
    filename = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.mp3"
    tts = gTTS(message)
    tts.save(filename)
    playFromFile(filename)
    
def playFromFile(filename) -> None:
    player = vlc.MediaPlayer(filename)
    player.play()
    while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
        time.sleep(1)  # check every second whether audio is still playing
    player.stop()  # Stop player when playback complete
    # can use mpg123 on rasp pi to play the file above manually from command line

def speak(mode: AlertMode):
    audio_file = mode.value
    # setup VLC player
    print(audio_file)
    player = vlc.MediaPlayer(audio_file)
    print("file opened", audio_file)
    player.play()
    while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
        print("playing")
        time.sleep(1)  # check every second whether audio is still playing

    player.stop()  # Stop player when playback complete
    player.release()
# can use mpg123 on rasp pi to play the file above manually from command line

def speak_test():
    player = vlc.MediaPlayer("uv_alert.mp3")
    time.sleep(3)
    player.play()
    while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
        print("playing")
        time.sleep(1)  # check every second whether audio is still playing

    player.stop()  # Stop player when playback complete
    player.release()