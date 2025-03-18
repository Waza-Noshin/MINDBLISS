import os
import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf
from sklearn.svm import SVC
import joblib
import random

# Constants
SAMPLE_RATE = 48000  # Ensure this matches your microphone's supported rate
DURATION = 3  # Record duration in seconds
DATASET_PATH = r"C:\Users\DELL\Desktop\final\archive (7)"  # Update with your dataset path
MODEL_PATH = "svm_emotion_model.pkl"  # Path to save/load trained model

# Emotion Mapping
EMOTION_MAP = {3: "Stress", 4: "Anxiety", 5: "Depression"}

# Function to extract audio features
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=3.0)
        
        # Extract multiple audio features
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)  # More MFCCs
        chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)

        return np.hstack([mfcc, chroma, mel, contrast, tonnetz])  # Use multiple features
    except Exception as e:
        print(f"[ERROR] Feature extraction failed: {e}")
        return None

# Function to load dataset and extract features
def load_dataset():
    X, y = [], []
    emotion_mapping = {3: "Stress", 4: "Anxiety", 5: "Depression"}
    emotion_samples = {"Stress": [], "Anxiety": [], "Depression": []}  # Store features separately

    for root, _, files in os.walk(DATASET_PATH):
        for file in files:
            if file.endswith(".wav"):
                parts = file.split("-")
                if len(parts) > 2:
                    try:
                        emotion = int(parts[2])
                        if emotion in emotion_mapping:
                            feature = extract_features(os.path.join(root, file))
                            if feature is not None:
                                emotion_samples[emotion_mapping[emotion]].append((feature, emotion_mapping[emotion]))
                    except ValueError:
                        print(f"[WARNING] Skipping invalid filename: {file}")

    # Balance samples (limit stress samples to match smallest category)
    min_samples = min(len(emotion_samples["Stress"]), len(emotion_samples["Anxiety"]), len(emotion_samples["Depression"]))
    balanced_X, balanced_y = [], []

    for emotion, samples in emotion_samples.items():
        random.shuffle(samples)
        selected_samples = samples[:min_samples]  # Keep equal samples
        for feature, label in selected_samples:
            balanced_X.append(feature)
            balanced_y.append(label)

    print(f"[INFO] Balanced Dataset: Stress={min_samples}, Anxiety={min_samples}, Depression={min_samples}")

    return np.array(balanced_X), np.array(balanced_y)

# Train the SVM model
def train_svm():
    print("[INFO] Loading dataset and extracting features...")
    X, y = load_dataset()

    if len(X) == 0:
        print("[ERROR] No training data available.")
        return

    unique, counts = np.unique(y, return_counts=True)
    class_distribution = dict(zip(unique, counts))
    print(f"[INFO] Training Data Class Distribution: {class_distribution}")

    model = SVC(kernel='linear', probability=True)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("[INFO] Model training completed and saved.")

# Record real-time audio
def record_audio(filename="real_time_audio.wav"):
    print("[INFO] Recording for 10 seconds...")

    # Set the correct device index and channels
    sd.default.device = 1  # Replace with the correct device index
    sd.default.channels = 1  # Use 1 for mono, 2 for stereo

    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, recording, SAMPLE_RATE)

    print("[INFO] Recording saved.")

# Predict emotion from recorded voice
def predict_emotion():
    if not os.path.exists(MODEL_PATH):
        print("[INFO] No trained model found. Training new model...")
        train_svm()

    model = joblib.load(MODEL_PATH)  # Load trained SVM model
    record_audio()

    feature = extract_features("real_time_audio.wav")  # Extract features from recorded audio
    if feature is not None:
        prediction = model.predict([feature])[0]  # Predict emotion
        print(f"\n🎤 Detected Emotion: {prediction}")  # Display result
    else:
        print("[ERROR] Failed to extract features from recorded audio.")

# Main function to run the prediction
if __name__ == "__main__":
    print("[INFO] Starting voice recognition script...")
    predict_emotion()
    print("[INFO] Script execution completed.")