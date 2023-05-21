import openai
import sounddevice as sd
import keyboard
from scipy.io.wavfile import write
import threading
from decouple import config


##YOUR OPENAI API KEY HERE
openai.api_key = config('openai_api_key')

freq = 44100  # Sampling frequency
recording = None
is_recording = False

print("------PRESS 'A' TO START THE RECORDING-----------")


def start_recording():
    global recording
    global is_recording
    is_recording = True
    print('Record start')
    recording = sd.rec(int(10 * freq), samplerate=freq, channels=2)
    
def stop_recording():
    global is_recording
    is_recording = False
    print('Record stop')
    sd.wait()
    write('UserSpeech.wav', freq, recording)  # Save as WAV file

    #Transcription
    audio_file= open("UserSpeech.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print ("User transcript audio", transcript.text)

    #Module conversationnal
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as an tsundere girlfriend."},
            {"role": "user", "content": transcript.text}
        ]
    )

    print(response['choices'][0]['message']['content'])


def on_press_a(e):
    if not is_recording:
        threading.Thread(target=start_recording).start()
    
def on_release_a(e):
    if is_recording:
        stop_recording()

keyboard.on_press_key('a', on_press_a)
keyboard.on_release_key('a', on_release_a)

keyboard.wait()

            