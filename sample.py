from gtts import gTTS
from playsound import playsound


def voice_play():
    with open("my.txt") as f:
        with open("sentiment.txt") as g:
            line1 = f.readlines()
            line2 = g.readlines()
            with open("playback.txt", "w") as f1:
                f1.writelines(line1)
                f1.write(' ')
                f1.writelines(line2)
                f1.write('  thank you')

    file = open("playback.txt", "r").read().replace("\n", " ")
    language = 'en'
    speech = gTTS(text=str(file), lang=language, slow=False)
    a = 'trial.mp3'
    speech.save(a)
    playsound(a)
