import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import openai

app = Flask(__name__)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key! Set the OPENAI_API_KEY environment variable.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

PRESIDENTS = {
    "lincoln": {
        "name": "Abraham Lincoln",
        "image": "/assets/abraham_lincoln_headshot.png"
    },
    "jefferson": {
        "name": "Thomas Jefferson",
        "image": "/assets/thomas_jefferson_headshot.png"
    },
}

@app.route("/", methods=["GET", "POST"])
def home():
    selected_president = "Abraham Lincoln"
    image_url = "/assets/abraham_lincoln_headshot.png"

    if request.method == "POST":
        president_key = request.form.get("president")
        if president_key in PRESIDENTS:
            selected_president = PRESIDENTS[president_key]["name"]
            image_url = PRESIDENTS[president_key]["image"]

    return render_template("index.html", selected_president=selected_president, image_url=image_url)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Please ask a valid question!"})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
        )
        ai_response = response.choices[0].message.content
    except Exception as e:
        ai_response = f"Error: {str(e)}"

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
