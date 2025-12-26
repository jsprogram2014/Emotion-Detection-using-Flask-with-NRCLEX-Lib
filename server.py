"""
Executing this function initiates the application of emotion
detection to be executed over the Flask channel and deployed on
localhost:5000.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Initialize Flask with explicit folder paths for your structure
app = Flask(__name__)

@app.route('/')
def main_app():
    """
    Renders the main application page.
    """
    return render_template('index.html')

@app.route('/emotionDetector')
def emotion_detects():
    """
    Analyzes the text and returns a nicely formatted HTML string
    to be displayed in the user's browser.
    """
    text_to_analysis = request.args.get('textToAnalyze')

    # 1. Safety Check: Handle empty input
    if not text_to_analysis:
        return "<b style='color:red;'>Invalid text! Please try again.</b>"

    # 2. Run the analysis (Supports 5, 8, or 10 emotions dynamically)
    analysed_text_dict = emotion_detector(text_to_analysis)

    # 3. Check for valid results
    if analysed_text_dict['dominant_emotion'] == 'None':
        return "<b style='color:red;'>Could not detect emotion. Please try a longer sentence.</b>"

    # 4. Extract Dominant Emotion & Scores
    dominant_emotion = analysed_text_dict.pop('dominant_emotion')
    
    # Format the scores: "Joy: 0.95, Anger: 0.00"
    # We filter out any 0.0 scores to keep the UI clean (optional)
    score_list = [
        f"<b>{key.capitalize()}</b>: {value:.2f}" 
        for key, value in analysed_text_dict.items() 
        if value > 0  # Only show relevant emotions
    ]
    
    # If all scores are 0 (but dominant was set by fallback), show all
    if not score_list:
        score_list = [f"{key.capitalize()}: {value:.2f}" for key, value in analysed_text_dict.items()]

    formatted_scores = ", ".join(score_list)

    # 5. Return the "Good Looking" HTML String
    # This uses <br> for new lines and <b> for bold text
    return (
        f"The dominant emotion is <b>{dominant_emotion.upper()}</b>.<br>"
        f"<div style='margin-top: 10px; font-size: 0.9em; color: #555;'>"
        f"Analysis breakdown: {formatted_scores}"
        f"</div>"
    )

if __name__ == '__main__':
    # Run on 0.0.0.0 for Render compatibility
    app.run(host='0.0.0.0', port=5000)