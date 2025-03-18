import os
import librosa
import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Constants
DATASET_PATH = "E:\\WAZA\\MINDBLISS\\assets\\archive" 
MODEL_PATH = "ravdess_emotion_svm.pkl"
SAMPLE_RATE = 22050
DURATION = 10

# Emotion mapping (modify based on your dataset labels)
EMOTION_MAP = {
    "03": "Stress",
    "04": "Anxiety",
    "05": "Depression"
}

# Function to extract features from an audio file
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=DURATION, sr=SAMPLE_RATE)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        mel = librosa.feature.melspectrogram(y=y, sr=sr)
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        return np.hstack([np.mean(mfcc, axis=1), np.mean(chroma, axis=1), np.mean(mel, axis=1), np.mean(contrast, axis=1)])
    except Exception as e:
        print(f"[ERROR] Failed to extract features from {file_path}: {e}")
        return None

# Load dataset and extract features
def load_dataset():
    X, y = [], []
    for folder in os.listdir(DATASET_PATH):  # Assuming dataset is divided into emotion-labeled folders
        label = folder[:2]  # Extract the first two digits as the emotion label (e.g., "03", "04")
        if label in EMOTION_MAP:
            folder_path = os.path.join(DATASET_PATH, folder)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                features = extract_features(file_path)
                if features is not None:
                    X.append(features)
                    y.append(label)
    return np.array(X), np.array(y)

# Train the model
X, y = load_dataset()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svm_model = SVC(kernel="linear", probability=True)
svm_model.fit(X_train, y_train)

# Evaluate the model
y_pred = svm_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(svm_model, MODEL_PATH)
print(f"Model saved as {MODEL_PATH}")
