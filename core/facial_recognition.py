import cv2
import time
import numpy as np
from deepface import DeepFace

# Step 1: Capture video frames using OpenCV
def capture_video(duration=10):
    """
    Captures video from the webcam for a specified duration.
    Args:
        duration (int): Duration in seconds to capture video.
    Returns:
        frames (list): List of captured frames.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open camera.")

    frames = []
    start_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit early
            break

    cap.release()
    cv2.destroyAllWindows()
    return frames


# Step 2: Analyze emotions using DeepFace
def analyze_emotions(frames):
    """
    Analyzes emotions in the captured frames using DeepFace.
    Args:
        frames (list): List of frames to analyze.
    Returns:
        avg_emotion (dict): Average emotion scores across all frames.
    """
    emotions = []
    for frame in frames:
        try:
            # Analyze the frame for emotions
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions.append(result[0]['emotion'])
        except Exception as e:
            print(f"Error analyzing frame: {e}")

    # Aggregate emotions across all frames
    avg_emotion = {emotion: float(np.mean([e[emotion] for e in emotions])) for emotion in emotions[0].keys()}
    return avg_emotion


# Step 3: Smooth and threshold emotion scores
def smooth_emotion_scores(emotion_scores, threshold=10.0):
    """
    Smooths and thresholds emotion scores to reduce noise.
    Args:
        emotion_scores (dict): Raw emotion scores.
        threshold (float): Minimum score for an emotion to be considered.
    Returns:
        smoothed_scores (dict): Smoothed and thresholded emotion scores.
    """
    smoothed_scores = {emotion: max(0, score - threshold) for emotion, score in emotion_scores.items()}
    total = sum(smoothed_scores.values())
    if total > 0:
        smoothed_scores = {emotion: (score / total) * 100 for emotion, score in smoothed_scores.items()}
    return smoothed_scores


# Step 4: Detect mental state (stress, anxiety, depression)
def detect_mental_state(avg_emotion):
    """
    Detects mental state based on average emotion scores.
    Args:
        avg_emotion (dict): Average emotion scores.
    Returns:
        mental_state (dict): Detected mental state scores.
    """
    stress = avg_emotion['angry'] + avg_emotion['fear']
    anxiety = avg_emotion['fear'] + avg_emotion['sad']
    depression = avg_emotion['sad'] + avg_emotion['neutral']

    mental_state = {
        'stress': float(stress),
        'anxiety': float(anxiety),
        'depression': float(depression)
    }
    return mental_state


# Step 5: Main function to integrate everything
def main():
    """
    Main function to capture video, analyze emotions, and detect mental state.
    """
    print("Starting facial emotion recognition...")

    # Step 1: Capture video for 6-10 seconds
    print("Capturing video for 10 seconds...")
    frames = capture_video(duration=10)

    # Step 2: Analyze emotions
    print("Analyzing emotions...")
    avg_emotion = analyze_emotions(frames)
    print("Raw Emotion Scores:", avg_emotion)

    # Step 3: Smooth and threshold emotion scores
    smoothed_emotion = smooth_emotion_scores(avg_emotion, threshold=10.0)
    print("Smoothed Emotion Scores:", smoothed_emotion)

    # Step 4: Detect mental state
    mental_state = detect_mental_state(smoothed_emotion)
    print("Detected Mental State:", mental_state)

    # Step 5: Move to the next screen (e.g., display results)
    print("Analysis complete. Moving to the next screen...")
    # Implement your logic here to display results or move to the next screen


# Run the program
if __name__ == "__main__":
    main()