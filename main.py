import openai
from decouple import config

openai.api_key = config('openai_api_key')


response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as an tsundere girlfriend."},
            {"role": "user", "content": "how are you baby ?"}
        ]
    )

print(response['choices'][0]['message']['content'])
