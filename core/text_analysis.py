import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_emotion(text):
    """
    Analyze the emotion of the given text using VADER sentiment analysis.
    
    Args:
        text (str): The input text to analyze.
    
    Returns:
        str: The detected emotion based on the sentiment score.
    """
    sentiment_score = sia.polarity_scores(text)['compound']

    if sentiment_score <= -0.5:
        return "Depression Detected"
    elif -0.2 >= sentiment_score > -0.5:
        return "Stress Detected"
    elif 0.2 >= sentiment_score > -0.2:
        return "Anxiety Detected"
    else:
        return "Positive/Neutral Emotion"

# For standalone testing
if __name__ == "__main__":
    print("Enter text to analyze emotion (type 'exit' to stop)\n")
    while True:
        user_input = input("Enter your text: ")
        if user_input.lower() == 'exit':
            break
        print("📊 Emotion Detected:", analyze_emotion(user_input))