'''
Implements speaking capability for the plant via bluetooth
'''

from gtts import gTTS
import pygaame
import time

pygame.init()


tts = gTTS("hello, I am raspberry pi 4. This is a test with Google Text to speech (gTTS)")
tts.save("hello.mp3")
alert_sound = pygame.mixer.Sound("hello.mp3")
alert_sound.play()

# wait for sound to finish playing
time.sleep(alert_sound.get_length())

# use mpg123 on rasp pi to play the file above