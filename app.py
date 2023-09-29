from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["http://127.0.0.1:5500"])

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    pdf_content = request.json.get('pdf_content')  # You would extract this from the uploaded PDF

    # Make API call to OpenAI GPT-3 (this is a simplified example)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"PDF Content: {pdf_content}\nQuestion: {question}\nAnswer:",
        max_tokens=50
    )

    answer = response.choices[0].text.strip()

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response




