from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Check if the input is a URL
def is_url(input_data):
    return input_data.startswith('http://') or input_data.startswith('https://')

# Fetch the title heading from a URL
def fetch_h1_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('title')
    return title_tag.text if title_tag else "No title found"

# Route to handle the User Query
@app.route('/')
def queryHandle():
        #Placeholder Data Input that's entered by user
        data_input = "https://www.bbc.com/news/live/cnk4jdwp49et"
        
        if is_url(data_input):
            content = fetch_h1_from_url(data_input)
        else:
            content = data_input
        
        return render_template_string('''
            <h1>Data send by User</h1>
            <p>{{ content }}</p>
        ''', content=content)

if __name__ == "__main__":
    app.run(debug=True)
