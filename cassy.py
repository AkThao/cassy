import os
from dotenv import load_dotenv
import openai
import speech_recognition as sr
import boto3
from playsound import playsound
from datetime import datetime

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
        "content": "You are Cassy. You are a friendly chatbot that can answer questions and provide advice when needed."
    }
]

# Stop word so we can end the conversation without using the keyboard
STOP_WORD = "goodbye"

# Intro message for the start of the program
INTRO_MESSAGE = "Hi! I'm Cassy, a friendly chatbot designed to answer questions and provide advice. How can I help you today?"


def speak_message(response):
    speech = polly_client.synthesize_speech(VoiceId="Aria",
                                              OutputFormat="mp3",
                                              Text=response,
                                              Engine="neural")

    with open("response.mp3", "wb") as f:
        f.write(speech["AudioStream"].read())

    playsound("response.mp3")


def listen_to_voice_input():
    # Obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("\n> ", end="")
        audio = r.listen(source)

    # Try to transcribe audio using Whisper API through SpeechRecognition module
    try:
        speech_to_text = r.recognize_whisper_api(audio, api_key=openai.api_key)
        return speech_to_text
    except sr.RequestError as e:
        print(f"ERROR: Could not request results from Whisper API. {e}")
        return None


def send_message():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    response = completion.choices[0].message

    return response


def log_user_input(user_msg):
    with open("conversations.log", "a") as f:
        f.write(f"\n\n> {user_msg}")


def log_cassy_response(response):
    with open("conversations.log", "a") as f:
        f.write(f"\nCassy: " + response)


def save_user_input(user_input):
    user_message = {
        "role": "user",
        "content": user_input,
    }

    messages.append(user_message)


# The conversation loop
# The loop will end when the user says the stop word
# After every message, save the response to the messages array to be included in the next prompt
# This is how the model "remembers" the conversation
with open("conversations.log", "a") as f:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write(f"\n\n__________\n{dt_string}\n")

log_cassy_response(INTRO_MESSAGE)
speak_message(INTRO_MESSAGE)

while True:
    user_input = listen_to_voice_input()
    if (user_input == ""):
        continue
    save_user_input(user_input)
    log_user_input(user_input)
    print(user_input)

    response = send_message()
    messages.append(response)
    print("Cassy: " + response.content)

    log_cassy_response(response.content)
    speak_message(response.content)

    if (STOP_WORD in user_input.lower()):
        break
