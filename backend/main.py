from flask import Flask,request,jsonify render_template
import requests
from bs4 import BeautifulSoup
import re
from together import Together
import os

os.environ["TOGETHER_API_KEY"] = "your together api key"
# Initialize the Together client
client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.js')

# Check if the input is a URL
def is_url(input_data):
    return input_data.startswith('http://') or input_data.startswith('https://')

# Fetch the title heading from a URL
def fetch_title_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('title')
    return title_tag.text if title_tag else "No title found"

#preprocess the input data
def preprocess_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    return text

#function to query the Llama3
def call_llama3_model(preprocessed_data, prompt):
    # Prepare the payload for the API call
    response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    messages=[{"role": "system", "content": preprocessed_data}, {"role": "user", "content": prompt}],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>"],
    stream=False
    )

    # Extract the response content
    content = ""
    for choice in response.choices:
        content += choice.message.content

    return content

# Route to handle the User Query
app.route('/submit', methods=['GET', 'POST'])
def queryHandle():
        if request.method == 'POST':
        #Placeholder Data Input that's entered by user
        data_input = request.form.get['input']
    
        if is_url(data_input):
            content = fetch_title_from_url(data_input)
        else:
            content = data_input
        
        preprocessed_data = preprocess_text(content)
        prompt= "Is this news fake or real give me answer in only boolean return Real or Fake"
        response_data = call_llama3_model(preprocessed_data, prompt)
        return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
