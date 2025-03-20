import os

import openai
from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI API


@app.route('/', methods=['GET', 'POST'])
def index():
    key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=key)

    if request.method == 'POST':
        president = request.form['president']
        user_input = request.form['message']

        # Generate AI response based on president and user input
        response = openai.chat.completions.create(
            model="gpt-4",  # You can also use "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": f"You are answering as {president}."},
                {"role": "user", "content": user_input},
            ]
        )

        ai_response = response.choices[0].message.content
        return jsonify({'response': ai_response, 'president': president})

    return render_template_string(open_html())


def open_html():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Chatbot with President Selection</title>
        <style>
            body { font-family: Arial, sans-serif; }
            select, button { padding: 10px; font-size: 16px; }
            #chatbox { width: 100%; height: 400px; border: 1px solid #ccc; padding: 10px; overflow-y: scroll; margin-bottom: 20px; }
            #user-input { width: 80%; padding: 10px; }
            #send-btn { padding: 10px; }
            .message { margin: 10px 0; }
            .user-message { color: blue; text-align: right; }
            .ai-message { color: green; }
            #back-btn { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>AI Chatbot with President Interaction</h2>

        <div id="president-selection">
            <h3>Select a President:</h3>
            <form id="president-form" method="POST">
                <label for="president">Choose a President:</label>
                <select id="president" name="president">
                    <option value="George Washington">George Washington</option>
                    <option value="Abraham Lincoln">Abraham Lincoln</option>
                    <option value="Theodore Roosevelt">Theodore Roosevelt</option>
                    <option value="Franklin D. Roosevelt">Franklin D. Roosevelt</option>
                    <option value="John F. Kennedy">John F. Kennedy</option>
                </select>
                <button type="button" id="start-chat">Start Chat</button>
            </form>
        </div>

        <div id="chatbox-container" style="display:none;">
            <h3>Chat with <span id="selected-president"></span></h3>
            <div id="chatbox"></div>
            <input type="text" id="user-input" placeholder="Ask a question...">
            <button id="send-btn">Send</button>
            <button id="back-btn" onclick="window.location.reload();">Back to Select President</button>
        </div>

        <script>
            document.getElementById('start-chat').addEventListener('click', function() {
                var president = document.getElementById('president').value;
                document.getElementById('president-selection').style.display = 'none';
                document.getElementById('chatbox-container').style.display = 'block';
                document.getElementById('selected-president').textContent = president;
            });

            document.getElementById('send-btn').addEventListener('click', function() {
                const userInput = document.getElementById('user-input').value;
                if (userInput) {
                    appendMessage(userInput, 'user');

                    fetch('/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: 'message=' + encodeURIComponent(userInput) + '&president=' + encodeURIComponent(document.getElementById('selected-president').textContent)
                    })
                    .then(response => response.json())
                    .then(data => {
                        appendMessage(data.response, 'ai');
                    });
                }
            });

            function appendMessage(message, sender) {
                const chatbox = document.getElementById('chatbox');
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.classList.add(sender === 'user' ? 'user-message' : 'ai-message');
                messageDiv.textContent = message;
                chatbox.appendChild(messageDiv);
                document.getElementById('user-input').value = '';
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
