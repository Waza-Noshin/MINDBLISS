from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import time
import threading
import sys
sys.path.append("E:\\WAZA\\MINDBLISS\\core") 
from core.voice_recognition import record_audio, predict_emotion, extract_features, MODEL_PATH, SAMPLE_RATE, DURATION
import joblib

class VoiceViewScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super(VoiceViewScreen, self).__init__(**kwargs)
        self.app = app_instance
        self.analysis_time = 10  # 10-second countdown
        self.start_time = None
        self.is_recording = False

        Window.clearcolor = (0.9, 0.9, 1, 1)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])
        self.add_widget(self.layout)

        # 🔵 Circular Logo
        self.logo = Image(
            source="assets/logo_circle.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        self.layout.add_widget(self.logo)

        # 🏷 Tagline (Different Font)
        self.tagline = Label(
            text="Your Journey to Inner Peace and Emotional Well-Being",
            font_size=18,
            font_name="assets/custom_font.ttf",  # Ensure this points to the correct font file
            color=(0.2, 0.2, 0.5, 1),
            halign="center",
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(self.tagline)

        # 📜 Motivational Quote (Updated for Voice)
        self.quote_label = Label(
            text="“Your voice carries your emotions.\nSpeak freely and let us help you understand.”",
            font_size=16,
            color=(0.1, 0.1, 0.4, 1),
            size_hint=(1, None),
            height=65,
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.layout.add_widget(self.quote_label)

        # 🎤 Microphone Image (Initially Hidden)
        self.mic_image = Image(
            source="assets/mic.png",  # Replace with your microphone icon
            size_hint=(None, None),
            size=(160, 160),
            pos_hint={"center_x": 0.5, "top": 0.6},
            opacity=0
        )
        self.layout.add_widget(self.mic_image)

        # 🎬 Start Button
        self.start_button = Button(
            text="Start Analysis",
            size_hint=(None, None),
            size=(250, 70),
            pos_hint={"center_x": 0.5, "top": 0.3},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.start_button.bind(on_press=self.start_voice_analysis)
        self.layout.add_widget(self.start_button)

        # ⏳ Countdown Below Microphone (Initially Hidden)
        self.countdown_label = Label(
            text="10",
            font_size=24,
            bold=True,
            color=(0.2, 0.2, 0.4, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={"center_x": 0.5, "top": 0.15},
            opacity=0
        )
        self.layout.add_widget(self.countdown_label)

        # 🔜 Move Further Button (Initially Hidden)
        self.move_further_button = Button(
            text="Move Further",
            size_hint=(None, None),
            size=(250, 70),
            pos_hint={"center_x": 0.5, "top": 0.1},
            background_color=(0.2, 0.5, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True,
            disabled=True
        )
        self.move_further_button.opacity = 0
        self.move_further_button.bind(on_press=self.go_to_textview)
        self.layout.add_widget(self.move_further_button)

    def on_emotion_detected(self, emotion):
        # Pass the detected emotion to the ResultScreen
        result_screen = self.manager.get_screen('result')
        result_screen.update_emotion(emotion)
        
    def start_voice_analysis(self, instance):
        # Hide the start button and show the microphone image
        self.start_button.opacity = 0
        self.mic_image.opacity = 1
        self.countdown_label.opacity = 1

        # Start the countdown
        self.start_time = time.time()
        Clock.schedule_interval(self.update_countdown, 1)

        # Start recording in a separate thread
        self.is_recording = True
        threading.Thread(target=self.record_and_analyze).start()

    def update_countdown(self, dt):
        elapsed_time = time.time() - self.start_time
        remaining_time = int(self.analysis_time - elapsed_time)
        self.countdown_label.text = str(remaining_time)

        if elapsed_time >= self.analysis_time:
            Clock.unschedule(self.update_countdown)
            self.countdown_label.text = "Done!"
            self.is_recording = False
            self.enable_move_further()

    def record_and_analyze(self):
        # Record audio for the specified duration
        record_audio(filename="real_time_audio.wav")

        # Extract features and predict emotion
        feature = extract_features("real_time_audio.wav")
        if feature is not None:
            model = joblib.load(MODEL_PATH)  # Load trained SVM model
            prediction = model.predict([feature])[0]  # Predict emotion
            print(f"🎤 Detected Emotion: {prediction}")  # Display result in terminal
        else:
            print("[ERROR] Failed to extract features from recorded audio.")

    def enable_move_further(self):
        # Show the "Move Further" button
        self.move_further_button.opacity = 1
        self.move_further_button.disabled = False

    def go_to_textview(self, instance):
        # Navigate to the TextViewScreen
        self.manager.current = "textview"