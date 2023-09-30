from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS

# Load environment variables
load_dotenv("key.env")

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["http://127.0.0.1:5500", "http://127.0.0.1:5000"])


# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    pdf_content = request.json.get('pdf_content')  # You would extract this from the uploaded PDF
    context_note = "Note: When referring to 'Page X', it means the Xth page of the given PDF content."

    # Prepare the prompt
    prompt_text = f"{context_note}\nPDF Content: {pdf_content}\nQuestion: {question}\nAnswer:"

    # Print the prompt to the terminal for debugging
    print(f"Sending the following prompt to OpenAI: {prompt_text}")
    print(f"Received PDF content: {pdf_content}")
    print(f"Received question: {question}")


    # Make API call to OpenAI GPT-3.5 (this is a simplified example)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{context_note}\nPDF Content: {pdf_content}"},  # Include context_note here
        {"role": "user", "content": f"Question: {question}"}
    ]
    )


    answer = response['choices'][0]['message']['content'].strip()


    return jsonify({"answer": answer})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(debug=True)





