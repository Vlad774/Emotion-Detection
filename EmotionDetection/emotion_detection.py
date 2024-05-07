import requests
import json

def emotion_detector(text_to_analyse):
    # Check if the text to analyze is blank
    if not text_to_analyse.strip():
        # Return None for all emotion scores if the text is blank
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    data = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=data, headers=headers)

    # Check for successful response
    if response.status_code != 200:
        # If there's an error, return None for all emotion scores
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    formatted_response = json.loads(response.text)
    emotions = formatted_response.get('emotionPredictions', [])

    # Initialize emotion scores dictionary
    emotion_scores = {
        'anger': 0,
        'disgust': 0,
        'fear': 0,
        'joy': 0,
        'sadness': 0
    }

    # Update emotion scores from the list of emotions
    for prediction in emotions:
        for emotion, score in prediction['emotion'].items():
            emotion_scores[emotion] = max(emotion_scores[emotion], score)

    # Find the dominant emotion
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    # Add dominant emotion to the result
    emotion_scores['dominant_emotion'] = dominant_emotion

    return emotion_scores
