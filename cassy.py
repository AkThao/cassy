import os
from dotenv import load_dotenv
import openai
import speech_recognition as sr
import boto3
import vlc

# Initialisation
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

openai.api_key = OPENAI_API_KEY

# Set up client to communicate with AWS Polly for text to speech
polly_client = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name="eu-west-2").client("polly")


# This will store and track the list of messages that make up the conversation
# We will initialise it with a system message
messages = [
    {
        "role": "system",
        "content": "You are Cassy. You are a friendly, chatty and useful chatbot that can answer questions and provide advice when needed."
    }
]

# Stop word so we can end the conversation without using the keyboard
STOP_WORD = "goodbye"


def speak_response(response):
    speech = polly_client.synthesize_speech(VoiceId="Aria",
                                              OutputFormat="mp3",
                                              Text=response,
                                              Engine="neural")

    with open("response.mp3", "wb") as f:
        f.write(speech["AudioStream"].read())

    p = vlc.MediaPlayer("response.mp3")
    p.play()


def listen_to_voice_input():
    # Obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n> ", end="")
        audio = r.listen(source)

    # Try to transcribe audio using Whisper API through SpeechRecognition module
    try:
        speech_to_text = r.recognize_whisper_api(audio, api_key=openai.api_key)
        return speech_to_text
    except sr.RequestError as e:
        print(f"ERROR: Could not request results from Whisper API. {e}")
        return None


# The conversation loop
# The loop will end when the user says the stop word
# After every message, save the response to the messages array to be included in the next prompt
# This is how the model "remembers" the conversation
while True:
    user_input = listen_to_voice_input()
    print(user_input)
    if (user_input == None):
        break

    user_message = {
        "role": "user",
        "content": user_input,
    }

    messages.append(user_message)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    response = completion.choices[0].message
    messages.append(response)

    print("Cassy: " + response.content)

    speak_response(response.content)

    if (STOP_WORD in user_input.lower()):
        break
