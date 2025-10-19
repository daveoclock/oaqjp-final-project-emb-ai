# server.py

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector 

app = Flask(__name__)

@app.route("/")
def render_index_page():
    """
    Renders the main page (index.html) of the application.
    """
    return render_template('index.html')

@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Handles the request for emotion detection.
    """
    # 1. Get the text to analyze from the URL query parameter 'textToAnalyze'
    text_to_analyze = request.args.get('textToAnalyze')
    
    # Check if the input text is empty or None
    if not text_to_analyze:
        return "Invalid input. Please provide text to analyze.", 400

    # 2. Call the emotion detection function
    response = emotion_detector(text_to_analyze)

    # Check for errors returned by emotion_detector (e.g., connection failure or None values)
    if response['dominant_emotion'] is None:
        # A specific error handling message based on the dominant_emotion being None
        return f"Error: Could not process the statement or received an unexpected response.", 503

    # 3. Format the output string as requested
    
    output_message = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']}, "
        f"and 'sadness': {response['sadness']}. "
        f"The dominant emotion is **{response['dominant_emotion']}**."
    )

    return output_message

if __name__ == "__main__":
    # Deploy the application on localhost:5000 as requested The debug=True setting is helpful during development
    app.run(host="0.0.0.0", port=5000, debug=True)