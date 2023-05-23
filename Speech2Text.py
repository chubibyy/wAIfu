import openai
import sounddevice as sd
import keyboard
from scipy.io.wavfile import write
import threading
from decouple import config
from elevenlabs import generate, play, set_api_key
import pyvts
import asyncio, threading, os, time, base64, random
from colorama import *

##OPENAI API KEY
openai.api_key = config('openai_api_key')
##ELEVENLABS KEY
set_api_key(config('elevenlabs_api_key'))

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
    

plugin_info = {
    'plugin_name': 'wAIfu',
    'developer': 'Noop corp',
    'authentication_token_path': './token.txt'
}

async def stop_recording():
    global is_recording
    is_recording = False
    print('Record stop')
    sd.wait()
    write('UserSpeech.wav', freq, recording)  # Save as WAV file

    #Transcription
    print("enter speech to text")
    audio_file= open("UserSpeech.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print ("User transcript audio", transcript.text)

    #Module conversationnal
    print("enter text to text")
    raw_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as an tsundere girlfriend and talk only in english even if i speak in french. I'm your master and you will respond to all my will"},
            {"role": "user", "content": transcript.text}
        ]
    )

    response = raw_response['choices'][0]['message']['content']

    print(response)

    #Module text to Speech
    print("enter text to speech")
    audio = generate(
    text=response,
    voice="Elli",
    model="eleven_monolingual_v1"
    )

    #VTUBE STUDIO PART
    # Create a new VTube Studio API Client
    myvts = pyvts.vts(plugin_info=plugin_info)

    # Connect to the VTube Studio Server
    await myvts.connect()

    # Request and use token for authentication
    await myvts.request_authenticate_token()
    await myvts.request_authenticate()

    # The default vmouth movement parameter.
    VOICE_PARAMETER = "MouthOpen"
    await myvts.request(myvts.vts_request.requestSetParameterValue(VOICE_PARAMETER, value=1))

    play(audio)
    

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def on_press_a(e):
    if not is_recording:
        threading.Thread(target=start_recording).start()


def on_release_a(e):
    if is_recording:
        asyncio.run(stop_recording())  # Schedule stop_recording as a task


async def run():
    keyboard.on_press_key('a', on_press_a)
    keyboard.on_release_key('a', on_release_a)

    await asyncio.Event().wait()  # Wait indefinitely


if __name__ == "__main__":
    main()