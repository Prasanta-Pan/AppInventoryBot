from flask import Flask, request, jsonify, render_template
import sqlite3
import time
import openai
import os
import re

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = None

# Global variable to store the system message
system_message = None

# Global variable to cache the database connection
db_connection = None

# Global database file name
db_file = 'app_data.db'

import configparser
import openai

# Load external configurations
def load_configs(config_file="config.ini"):
    # Read API key from the config file
    config = configparser.ConfigParser()
    config.read(config_file)
    
    openai.api_key = config.get("openai", "api_key", fallback=None)
    #print(f"API key: {openai.api_key}")

    if not openai.api_key:
        print("ERROR: API key is missing in the configurati`    on file. Program will exit.")
        raise SystemExit(1)  # Exits with a non-zero status code


# Load system message from an external text file during server startup
def load_system_message():
    global system_message
    try:
        with open('ContextAndExample.txt', 'r') as file:
            system_message = file.read()
        print("System message loaded successfully.")
    except FileNotFoundError:
        print("System message file not found. Please check the path.")

# Function to initialize the SQLite database during server startup
def init_db():
    global db_connection  # Use the global variable to cache the connection

    try:
        # Check if the database file exists and delete it
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"Existing database '{db_file}' deleted.")

        # Load the startup script from file
        with open('application_inventory.sql', 'r') as file:
            startup_script = file.read()

        # Initialize the connection if it's not already cached
        if db_connection is None:
            db_connection = sqlite3.connect(db_file, check_same_thread=False)
            print("Database connection initialized and cached.")

        cursor = db_connection.cursor()

        # Execute the startup script
        cursor.executescript(startup_script)
        db_connection.commit()
        print("Startup script executed successfully.")

        # Verify data by running a sample query to check if data is loaded
        cursor.execute('SELECT * FROM application_inventory LIMIT 5')
        rows = cursor.fetchall()

        if rows:
            print("Sample data loaded successfully. Here are some records:")
            for row in rows:
                print(row)
        else:
            print("No data found in application_inventory table.")

    except (sqlite3.Error, FileNotFoundError) as e:
        print(f"SQLite init error: {e}")

    finally:
        # Only close the cursor, leave the connection open for reuse
        if cursor:
            cursor.close()

# Function to retrieve or update data from the cached database connection
def execute_sql_and_format_the_result(query):
    global db_connection
    cursor = None  # Initialize cursor to avoid potential NameError
    results = []

    try:
        # Ensure the database connection is initialized
        if db_connection is None:
            db_connection = sqlite3.connect(db_file, check_same_thread=True)
            print("Database connection initialized and cached.")

        cursor = db_connection.cursor()

        # Detect the query type by inspecting the first word of the query
        query_type = query.strip().split()[0].upper()

        # Check if the query is a SELECT or a non-SELECT type
        if query_type == 'SELECT':
            # Execute the SELECT query
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]  # Get column names

            # Format the result rows
            for row in rows:
                formatted_row = ", ".join(
                    f'{col_name} :=> "{col_value}"'
                    for col_name, col_value in zip(column_names, row)
                )
                results.append(formatted_row)

            return "\n".join(results) if results else "No data found."

        elif query_type in ('INSERT', 'UPDATE'):
            # Execute non-SELECT queries
            cursor.execute(query)
            db_connection.commit()

            # Return the affected rows information
            affected_rows = cursor.rowcount
            return f"{query_type} OK, {affected_rows} row(s) affected"

        else:
            # Raise an exception for unsupported query types
            raise ValueError(f"Unsupported query type: {query_type}")

    finally:
        # Close only the cursor, keep the database connection open for reuse
        if cursor:
            cursor.close()

# Call OpenAI API 
def process_conversation_with_openai(conversation_history):
    try:
        # Start the timer
        start_time = time.time()

        # Call OpenAI's Chat Completion API with conversation history and specific LLM parameters
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Specify the model
            messages=conversation_history,  # Pass the conversation history
            temperature=0.5,  # Adjust the creativity level of the model
            max_tokens=300,  # Limit the response length
            n=1,  # Number of completions to generate
            stop=None,  # You can specify stop sequences, or leave None for default behavior
            top_p=1.0,  # Nucleus sampling (1.0 means no filtering)
            frequency_penalty=0.0,  # Penalize new tokens based on frequency
            presence_penalty=0.0  # Penalize tokens that appear in the context
        )
        
        # Calculate and print the response time
        response_time = time.time() - start_time
        print(f"API response time: {response_time:.2f} seconds")

        # Extract the assistant's reply
        assistant_message = response['choices'][0]['message']['content']

        # Add the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})
        # Return the updated conversation history
        return conversation_history

    except Exception as e:
        print(f"Error processing conversation with OpenAI: {e}")
        return None
    
# Extract SQL statements from LLM response    
def extract_sql_statement(response):
    # Define a regex pattern to extract SQL statements
    pattern = r'(SELECT.*?;|UPDATE.*?;|INSERT.*?;)'
    
    # Find all occurrences of the pattern in the response
    sql_queries = re.findall(pattern, response, re.DOTALL)
    
    # Check if any SQL queries were found; if not, raise an exception
    if not sql_queries:
        raise ValueError("No SQL queries found in the response.")
    
    return sql_queries

    
# API to handle user message and send it along with system message to OpenAI API
@app.route('/chatbot', methods=['POST'])
def chatbot():
    global system_message

    try:
        # Get the user message from the request body as plain text
        user_message = request.data.decode('utf-8').strip()
        if not user_message:
            return "Error: No message provided", 400
    
        # Initialize conversation history
        conversation_history = []
        
        # Add the system context message to the conversation history
        conversation_history.append({"role": "system", "content": system_message})

        # Get system msg to be logged
        truncated_content = conversation_history[0]['content'][:150] + ('...' if len(conversation_history[0]['content']) > 150 else '')
        # log system msg
        print(f"#### Msg: System - {truncated_content}")
        # Add the user message with the instruction to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # log user msg
        print(f"#### Msg: user - {user_message}")

        # Pass the conversation history to the OpenAI API to generate SQL
        conversation_history = process_conversation_with_openai(conversation_history)

        # Extract the assistant's SQL query from the updated conversation history
        assistant_message = conversation_history[-1]['content']

         # log assistent msg
        print(f"#### Msg: Assistent - {assistant_message}")
        # Extract SQL queries
        try:
            # Extract the SQL to be executed
            sql_stmts = extract_sql_statement(assistant_message)
            # Initialize `result` outside the loop to accumulate all query results
            result = "Please find the database execution resutls as below\n"

            for sql in sql_stmts:
                # Execute the generated SQL against the database
                query_result = execute_sql_and_format_the_result(sql)
                
                # Append formatted query and result for each SQL statement
                result += f"### SQL ###\n{sql}\n### Result ###\n{query_result}\n\n"
                
            # Add the accumulated result of all SQL queries to the conversation history
            conversation_history.append({
                "role": "user", 
                "content": result
            })
            # Log SQL result
            print(f"#### Msg: user - {result}")
        except ValueError as e:
           return f"{assistant_message}", 200, {'Content-Type': 'text/plain'}

        # Pass the conversation history to the OpenAI API to get user-friendly response
        conversation_history = process_conversation_with_openai(conversation_history)
        # Log final response from LLM
        print(f"##### Msg: Assistent - {conversation_history[-1]['content']}")
        # Print conversation history
        # print_conversation_history(conversation_history)
        # Return the final user-friendly response as plain text
        return conversation_history[-1]['content'], 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        return f"Error: {str(e)}", 500, {'Content-Type': 'text/plain'}

# Print conversation history
def print_conversation_history(conversation_history):
    print("Conversation history:\n")
    for i, message in enumerate(conversation_history):
        # Truncate only the first message if it exceeds 150 characters
        if i == 0:
            truncated_content = message['content'][:150] + ('...' if len(message['content']) > 150 else '')
        else:
            truncated_content = message['content']  # Keep the full content for other messages
        
        print(f"Message {i+1}: {message['role']} - {truncated_content}")

# API to render a chat window (frontend)
@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    # Load external configs during boot
    load_configs()
    # Load the system message once when the server starts
    load_system_message()

    # Initialize the database and cache the connection
    init_db()

    # Start the server
    app.run(debug=True)
