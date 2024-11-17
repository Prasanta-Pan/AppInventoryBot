import json
import pprint
# Load conversation history from a JSON file
with open('ContextAndExample.json', 'r') as file:
    conversation_history = json.load(file)

# Now you can pass this conversation history to the OpenAI API as the messages parameter.
# Example of how you might use it in an API call:
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=conversation_history
# )

# Print out the conversation history (optional)
for message in conversation_history:
    print(f"{message['role']}: {message['content']}\n")

# pprint.pprint(conversation_history)