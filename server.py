"""
Flask application for emotion detection.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def analyze_emotion():
    """
    Analyze the emotion of a statement.

    Returns:
        JSON: Emotion analysis result.
    """
    data = request.get_json()
    statement = data.get('statement', '')

    if not statement:
        return jsonify({"error": "Field is blank. Please enter emotion"}), 400

    emotions = emotion_detector(statement)
    response = {
        "anger": emotions.get("anger", 0),
        "disgust": emotions.get("disgust", 0),
        "fear": emotions.get("fear", 0),
        "joy": emotions.get("joy", 0),
        "sadness": emotions.get("sadness", 0),
        "dominant_emotion": emotions.get("dominant_emotion", "")
    }
    return jsonify(response)

@app.route("/")
def render_index_page():
    """
    Render the index page.

    Returns:
        HTML: Index page template.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
