import random
from pydub import AudioSegment
from pydub.playback import play
# from pygame import mixir


def playaudio():
    song = AudioSegment.from_mp3("alert.mp3")
    print('[PLAYING] playing sound using pydub')
    play(song)
    print('[DONE] playing alert done')


while True:
    random_int = int(random.choice(["1","1","1","1","2"]))
    if random_int == 2:
        print(f"Choice:  {random_int}")
        playaudio()


