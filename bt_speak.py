'''
Implements speaking capability for the plant via bluetooth
'''

from gtts import gTTS
# import pygame
import time
# from playsound import playsound
import vlc

# pygame.init()


tts = gTTS("hello, I am raspberry pi 4. This is a test with Google Text to speech (gTTS)")
tts.save("hello.mp3")
# playsound("./hello.mp3")
player = vlc.MediaPlayer("hello.mp3")
player.play()
while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
    time.sleep(1)  # check every second whether audio is still playing

player.stop()
# can use mpg123 on rasp pi to play the file above manually from command line