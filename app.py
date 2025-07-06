import os
import time
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["screenshot"]
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        time.sleep(5)
        signal = analyze_screenshot(path)

        return render_template("index.html", signal=signal)

    return "Upload failed"

def analyze_screenshot(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return "Unable to read image"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    candle_zone = gray[int(height*0.4):int(height*0.6), :]
    avg_brightness = np.mean(candle_zone)

    if avg_brightness > 127:
        return "PUT"
    else:
        return "CALL"

if __name__ == "__main__":
    app.run(debug=True)
