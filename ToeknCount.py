import tiktoken

# Global variable to store the system message
system_message = None

# Load system message from an external text file during server startup
def load_system_message():
    global system_message
    try:
        with open('ContextAndExample.txt', 'r') as file:
            system_message = file.read()
        print("System message loaded successfully.")
    except FileNotFoundError:
        print("System message file not found. Please check the path.")
        system_message = ""  # Set to an empty string if the file is not found

# Load the system message before counting tokens
load_system_message()

# Check if the system message is loaded and not empty
if system_message:
    # Load the tokenizer for GPT-4
    tokenizer = tiktoken.encoding_for_model("gpt-4")

    # Count the number of tokens
    token_count = len(tokenizer.encode(system_message))

    print(f"Number of tokens: {token_count}")
else:
    print("No valid system message to tokenize.")
