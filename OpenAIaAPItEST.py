import openai

# Replace 'your-api-key-here' with your actual OpenAI API Secret Key
openai.api_key = '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'

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
        
        "2. User query: 'What is the purpose of XMS?'\n"
        "   SQL query: SELECT Description FROM application_inventory WHERE Name = 'XMS';\n\n"
        
        "3. User query: 'List the owners of all applications in Europe.'\n"
        "   SQL query: SELECT Name, Owner FROM application_inventory WHERE Sites LIKE '%urope%';\n\n"
        
        "4. User query: 'Which applications are deployed in Europe?'\n"
        "   SQL query: SELECT Name, Sites FROM application_inventory WHERE Sites LIKE '%europe%';\n\n"
        
        "5. User query: 'Show me applications with an EOL after 2025.'\n"
        "   SQL query: SELECT Name, EOL FROM application_inventory WHERE EOL > '2025';\n\n"
        
        "When generating SQL queries, follow these principles:\n"
        "- Use the correct table and column names as per the schema.\n"
        "- Ensure that conditions in WHERE clauses match the user’s intent (e.g., use LIKE for partial matches).\n"
        "- Format dates in YYYY-MM-DD format.\n"
        "- Only return the columns necessary to answer the user’s query."
    )
}

# Define the user message
user_message = { 
    "role": "user", 
    "content": "Which are the application XMS is interfacing with and communication mechanism ?"
}

# Send the system instructions and user query in the same request to OpenAI's API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",  # Use GPT-4 or another model
    messages=[sql_query_helper_system_message, user_message],  # System message + user query
    max_tokens=150,
    temperature=0.5
)

# Print the response from OpenAI
print(response['choices'][0]['message']['content'])
