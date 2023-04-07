import openai

with open(".env", "r") as env_file:
    key = env_file.read()
    openai.api_key = key.strip()

# This will store and track the list of messages that make up the conversation
# We will initialise it with a system message
messages = [
    {
        "role": "system",
        "content": "You are a friendly, chatty and useful chatbot that can answer questions and provide advice when needed."
    }
]

# The conversation loop
# The loop will end when the user says "STOP"
# After every message, save the response to the messages array to be included in the next prompt
# This is how the model "remembers" the conversation
while True:
    user_input = input("Prompt: ")
    if (user_input == "STOP"):
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

    print("Response: " + response.content)

