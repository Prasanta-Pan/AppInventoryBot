from flask import Flask, jsonify, request

import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'set-your-own-key'


# Define the system message with SQL Query Helper instructions
sql_query_helper_system_message = {
    "role": "system",
    "content": (
        "You are an expert SQL generator. Your job is to generate SQL queries based on user requests. "
        "The queries should be tailored to the 'application_inventory' database, which has the following schema:\n\n"
        "- Name (string): The name of the application.\n"
        "- Description (string): A description of the application.\n"
        "- Division (string): The division where the application belongs.\n"
        "- Sites (string): The locations where the application is deployed.\n"
        "- Owner (string): The owner of the application.\n"
        "- Components (string): The components of the application.\n"
        "- Technology (string): The technologies used by the application.\n"
        "- Version (string): The version of the application.\n"
        "- Effective Date (string): The date when the application became effective.\n"
        "- EOL (string): The End of Life date for the application.\n"
        "- Interface (string): The systems that interface with the application.\n"
        "- Medium (string): The communication medium used in the interface.\n\n"
        
        "Here are a few examples of how to convert user queries into SQL queries:\n\n"
        
        "1. User query: 'Which applications are using Java?'\n"
        "   SQL query: SELECT Name, Description FROM application_inventory WHERE Technology LIKE '%Java%';\n\n"
        
        "2. User query: 'What is the End of Life for XMS?'\n"
        "   SQL query: SELECT EOL FROM application_inventory WHERE Name = 'XMS';\n\n"
        
        "3. User query: 'List the owners of all applications in Europe.'\n"
        "   SQL query: SELECT Name, Owner FROM application_inventory WHERE Sites LIKE '%Europe%';\n\n"
        
        "4. User query: 'Which applications are deployed in Europe?'\n"
        "   SQL query: SELECT Name, Sites FROM application_inventory WHERE Sites LIKE '%Europe%';\n\n"
        
        "5. User query: 'Show me applications with an EOL after 2025.'\n"
        "   SQL query: SELECT Name, EOL FROM application_inventory WHERE EOL > '2025';\n\n"
        
        "When generating SQL queries, follow these principles:\n"
        "- Use the correct table and column names as per the schema.\n"
        "- Ensure that conditions in WHERE clauses match the user’s intent (e.g., use LIKE for partial matches).\n"
        "- Format dates in YYYY-MM-DD format.\n"
        "- Only return the columns necessary to answer the user’s query."
    )
}
# Define a route for the default URL
@app.route('/')
def home():
        # Combine the system message (role/instructions) with the user's query
    user_message = {"role": "user", "content": "What is the End of Life for XMS?"}
    
    # Send the system instructions and user query in the same request to OpenAI's API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  # Use GPT-4 or another model
        messages=[sql_query_helper_system_message, user_message],  # System message + user query
        max_tokens=150,
        temperature=0.5
    )
    
    # Extract and return the generated SQL query from the response
    return response['choices'][0]['message']['content'].strip()

    # return "Welcome to the API server!"


# Define a route for a sample API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, this is your API response!',
        'status': 'success'
    }
    return jsonify(data)

# Define an API endpoint that accepts POST requests
@app.route('/api/post_data', methods=['POST'])
def post_data():
    if request.is_json:
        input_data = request.get_json()
        response = {
            'received_data': input_data,
            'message': 'Data received successfully!'
        }
        return jsonify(response), 201
    else:
        return jsonify({'error': 'Invalid data format. Please send JSON.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
