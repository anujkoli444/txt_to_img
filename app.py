from flask import Flask, request, render_template, jsonify
import requests
import base64

app = Flask(__name__)

# Stability AI API details
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
API_KEY = "sk-MAPKEY"  # Replace with your actual API key

def generate_image(prompt):
    response = requests.post(
        API_URL,
        headers={
            "authorization": f"Bearer {API_KEY}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
        },
    )
    
    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return image_base64
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    image_base64 = None
    prompt = ""
    
    if request.method == "POST":
        prompt = request.form["text"]
        image_base64 = generate_image(prompt)
        if not image_base64:
            return "Error generating image.", 500
    
    return render_template("index.html", image_base64=image_base64, text=prompt)

if __name__ == "__main__":
    app.run(debug=True)
