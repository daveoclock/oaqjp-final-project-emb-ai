# emotion_detection.py

import requests
import json

def emotion_detector(text_to_analyze):
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
        
        # Check if the request was unsuccessful
        if response.status_code != 200:
            return {
                "anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None,
                "dominant_emotion": None
            }

        # Convert response text into a dictionary
        response_data = response.json()
        
        # The  path to the emotion scores is ['emotionPredictions'][0]['emotion']
        emotion_scores = response_data['emotionPredictions'][0]['emotion']

        # Extract the required emotion scores
        anger_score = emotion_scores['anger']
        disgust_score = emotion_scores['disgust']
        fear_score = emotion_scores['fear']
        joy_score = emotion_scores['joy']
        sadness_score = emotion_scores['sadness']
        
        # Find the Dominant Emotion
        
        # Create a dictionary of the required emotions and their scores
        emotions_map = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Find the key (emotion name) corresponding to the maximum value (score)
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
        pass # Fall through to return None-filled dictionary
    except (KeyError, IndexError):
        # Handle cases where the JSON structure is unexpected
        pass # Fall through to return None-filled dictionary
    
    # Return dictionary with None values if any error or exception occurs
    return {
        "anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None,
        "dominant_emotion": None
    }