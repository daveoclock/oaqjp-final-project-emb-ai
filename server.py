# server.py
"""Flask server for the Emotion Detection application."""

from flask import Flask, render_template, request

# The import path assumes the structure EmotionDetection/emotion_detection.py
from EmotionDetection.emotion_detection import emotion_detector

APP = Flask(__name__)

@APP.route("/")
def render_index_page():
    """Renders the main HTML page (index.html) for the application."""
    return render_template('index.html')

@APP.route("/emotionDetector")
def emotion_detector_route():
    """
    Handles the request for emotion detection.

    Retrieves text from the query parameters, calls the emotion_detector, 
    and returns a formatted output string or an error message.
    """
    # Use snake_case for local variable names
    text_to_analyze = request.args.get('textToAnalyze')

    # The emotion_detector handles blank input by returning a dictionary
    # where 'dominant_emotion' is None.
    response_data = emotion_detector(text_to_analyze)

    # Error Handling: Check for None from blank input or API failure.
    if response_data['dominant_emotion'] is None:
        # Returns the error message with a 400 Bad Request status code.
        return "Invalid text! Please try again!", 400

    # Format the successful output string using HTML <b> tags for bolding.
    output_message = (
        f"For the given statement, the system response is "
        f"'anger': {response_data['anger']}, "
        f"'disgust': {response_data['disgust']}, "
        f"'fear': {response_data['fear']}, "
        f"'joy': {response_data['joy']}, "
        f"and 'sadness': {response_data['sadness']}. "
        f"The dominant emotion is <b>{response_data['dominant_emotion']}</b>."
    )

    return output_message

if __name__ == "__main__":
    # Deploy the application on localhost:5000 as requested
    APP.run(host="0.0.0.0", port=5000, debug=True)
