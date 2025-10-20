# emotion_detection.py

import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyzes the emotion of the input text using the Watson NLP EmotionPredict function.
    It includes error handling for blank input and API failures.

    Args:
        text_to_analyze (str): The text to be analyzed for emotions.

    Returns:
        dict: A dictionary containing the detected emotion scores and the dominant emotion, 
              or a dictionary with all None values if the input is blank or the API fails.
    """
    
    # 1. Error Handling for Blank Entries (Simulating status_code 400 requirement)
    # The requirement is to return None values for status_code = 400.
    # We check if the input is blank *before* the API call.
    if not text_to_analyze or text_to_analyze.strip() == "":
        # Directly return the None-filled dictionary for a blank entry (status_code 400 scenario)
        return {
            "anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None,
            "dominant_emotion": None
        }

    # Define the URL and Headers
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Prepare the Input JSON Payload
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    # Send the POST Request and Handle Errors
    try:
        response = requests.post(url, headers=headers, json=input_json)
        
        # Check if the request was unsuccessful (e.g., 404, 500)
        if response.status_code != 200:
            return {
                "anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None,
                "dominant_emotion": None
            }

        # Convert response text into a dictionary
        response_data = response.json()
        
        # Extract Emotion Scores (Path: ['emotionPredictions'][0]['emotion'])
        emotion_scores = response_data['emotionPredictions'][0]['emotion']

        # Extract the required emotion scores
        anger_score = emotion_scores['anger']
        disgust_score = emotion_scores['disgust']
        fear_score = emotion_scores['fear']
        joy_score = emotion_scores['joy']
        sadness_score = emotion_scores['sadness']
        
        # Find the Dominant Emotion
        emotions_map = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        dominant_emotion = max(emotions_map, key=emotions_map.get)

        # Return the result in the specified format
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }

    except requests.exceptions.RequestException:
        # Handle exceptions like connection errors, timeouts, etc.
        pass
    except (KeyError, IndexError):
        # Handle cases where the JSON structure is unexpected
        pass
    
    # Final return of the None dictionary if any error or exception occurs after the input check
    return {
        "anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None,
        "dominant_emotion": None
    }