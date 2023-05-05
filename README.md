# CASSY - Chatty And Smart SYstem

Cassy is a chatbot built entirely around voice interactivity. It is based on the OpenAI language model gpt3.5, which is the same model that forms the basis of ChatGPT.

Cassy combines three independent subsystems:

1. Speech-to-text: A Python speech recogniser module records voice input from the microphone then passes it to OpenAI's Whisper model to transcribe the input to English text.
1. Chat completion: The text from the voice input is used to construct a message, which is then passed to gpt3.5 and a response is received in a similarly formatted message.
1. Text-to-speech: Amazon's Polly cloud service is used to create a realistic human voice output from the gpt3.5 response message, which is then played using the Python VLC module.

This runs in an infinite loop, which keeps the conversation going until the user's message contains the stop word "goodbye", at which point the conversation and therefore, the program, ends.


### Dependencies

---

* boto3 1.26.108 - enables communication with Amazon AWS services
* openai 0.27.4 - need at least version 0.27.0 to use the ChatCompletion and Audio.transcribe API endpoints
* python-vlc 3.0.18121 - used to play the audio file containing the language model's response
* python-dotenv 1.0.0 - to read API keys from a local .env file
* SpeechRecognition 3.10.0 - used to record audio input from microphone
* PyAudio 0.2.13 - used by SpeechRecognition module (requires portaudio to be installed on macOS - can install through homebrew)
* Python 3.9.16 - the OpenAI API endpoints used in this project do not work with Python versions below 3.7


### Instructions to run

---

1. Set up a Python virtual environment with all the above dependencies
2. Set up an OpenAI account and get an API key
3. Set up an AWS account, create an IAM user, add the polly:SynthesizeSpeech permission to that user and generate API keys for the user
4. Copy .env.example to an .env file (must be in the same directory as cassy.py) and put all the API keys in there
5. With the virtual environment activated, run `python3 cassy.py`
