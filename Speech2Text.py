import openai
import sounddevice as sd
import keyboard
from scipy.io.wavfile import write
import os

##YOUR OPENAI API KEY HERE
openai.api_key = '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'



# Sampling frequency
freq = 44100  
# Recording duration
duration = 5

while True:
    try:
        if keyboard.is_pressed('a'):
            # Record audio for the given number of seconds
            recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
            print ('record start')
            sd.wait()
            print("record finished")

            write('UserSpeech.wav', freq, recording)  # Save as WAV file
            

            #Transcription
            audio_file= open("UserSpeech.wav", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            print (transcript)
                        
    except Exception as e:
        print(e)
        break  # if user pressed a key other than the given key the loop will break