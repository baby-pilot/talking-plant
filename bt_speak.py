'''
Implements speaking capability for the plant via bluetooth
'''

from gtts import gTTS
import time
import vlc
from datetime import datetime

tts = gTTS("hello, I am raspberry pi 4. This is a test with Google Text to speech (gTTS)")
tts.save("hello.mp3")
# setup VLC player
player = vlc.MediaPlayer("hello.mp3")
player.play()
while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
    time.sleep(1)  # check every second whether audio is still playing

player.stop()  # Stop player when playback complete
# can use mpg123 on rasp pi to play the file above manually from command line

class BTSpeaker:
    def generateAndPlay(self, message) -> None:
        filename = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.mp3"
        tts = gTTS(message)
        tts.save(filename)
        self.playFromFile(filename)
        
    def playFromFile(self, filename) -> None:
        player = vlc.MediaPlayer(filename)
        player.play()
        while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
            time.sleep(1)  # check every second whether audio is still playing
        player.stop()  # Stop player when playback complete
        # can use mpg123 on rasp pi to play the file above manually from command line