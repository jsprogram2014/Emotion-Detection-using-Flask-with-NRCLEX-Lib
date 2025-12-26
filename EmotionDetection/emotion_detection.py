from nrclex import NRCLex
from textblob import TextBlob  # Import TextBlob for the backup check

def emotion_detector(text_to_analyze):
    # 1. Run the advanced NRCLex analysis
    emotion_obj = NRCLex(text_to_analyze)
    raw_scores = emotion_obj.raw_emotion_scores
    
    # 2. Define the full list of emotions we want to track
    required_emotions = [
        'anger', 'disgust', 'fear', 'joy', 'sadness', 
        'anticipation', 'surprise', 'trust',
        'positive', 'negative'
    ]
    
    # Initialize dictionary with zeros
    final_dict = {key: 0.0 for key in required_emotions}
    
    # 3. Calculate scores
    total_score = sum(raw_scores.get(key, 0) for key in required_emotions)
    
    if total_score > 0:
        for key in required_emotions:
            if key in raw_scores:
                final_dict[key] = raw_scores[key] / total_score

    # 4. Check for Dominant Emotion
    if all(value == 0 for value in final_dict.values()):
        # --- BACKUP PLAN: If NRCLex fails (returns all 0s), use TextBlob ---
        blob = TextBlob(text_to_analyze)
        polarity = blob.sentiment.polarity  # Returns float between -1.0 and 1.0
        
        if polarity > 0:
            final_dict['dominant_emotion'] = 'positive'
            final_dict['positive'] = polarity
            final_dict['joy'] = polarity / 2  # Give it a bit of joy too
        elif polarity < 0:
            final_dict['dominant_emotion'] = 'negative'
            final_dict['negative'] = abs(polarity)
        else:
            final_dict['dominant_emotion'] = 'None'
    else:
        # Standard logic: Filter out generic 'positive/negative' to find the specific emotion
        emotions_only = {k: v for k, v in final_dict.items() if k not in ['positive', 'negative']}
        
        # If we have specific emotions (like Joy or Fear), pick the strongest one
        if any(v > 0 for v in emotions_only.values()):
            final_dict['dominant_emotion'] = max(emotions_only, key=emotions_only.get)
        else:
            # Otherwise, fall back to just 'positive' or 'negative'
            final_dict['dominant_emotion'] = max(final_dict, key=final_dict.get)

    return final_dict