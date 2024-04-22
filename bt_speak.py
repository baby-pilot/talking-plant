'''
Implements speaking capability for the plant via bluetooth
'''

from gtts import gTTS
tts = gTTS("hello, I am raspberry pi 4. This is a test with Google Text to speech (gTTS)")
tts.save("hello.mp3")

# use mpg123 on rasp pi to play the file above