from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from deepface import DeepFace
import cv2
import numpy as np
import time
from kivy.graphics.texture import Texture

class FacialViewScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super(FacialViewScreen, self).__init__(**kwargs)
        self.app = app_instance
        self.capture = None
        self.is_analyzing = False
        self.analysis_time = 10
        self.detected_emotions = []
        self.start_time = None

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

        # 📜 Motivational Quote
        self.quote_label = Label(
            text="“Self-analysis is the first step to well-being.\n  Act before things become harmful.”",
            font_size=16,
            color=(0.1, 0.1, 0.4, 1),
            size_hint=(1, None),
            height=65,
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.layout.add_widget(self.quote_label)

        # 📷 Camera Feed (Increased Size, 2cm margin)
        self.image_widget = Image(
            size_hint=(0.9, 0.6),  # Increased size (90% width, 60% height)
            pos_hint={"center_x": 0.5, "top": 0.7}  # Adjusted position for 2cm margin
        )
        self.image_widget.opacity = 0
        self.layout.add_widget(self.image_widget)

        # ⏳ Countdown Below Camera Feed (Fixed Position)
        self.countdown_label = Label(
            text="10",
            font_size=24,
            bold=True,
            color=(0.2, 0.2, 0.4, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={"center_x": 0.5, "top": 0.15}  # Placed below the camera feed
        )
        self.layout.add_widget(self.countdown_label)

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
        self.start_button.bind(on_press=self.start_camera)
        self.layout.add_widget(self.start_button)

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
        self.move_further_button.bind(on_press=self.go_to_voice_analysis)
        self.layout.add_widget(self.move_further_button)
    def on_emotion_detected(self, emotion):
        # Pass the detected emotion to the ResultScreen
        result_screen = self.manager.get_screen('result')
        result_screen.update_emotion(emotion)
        
    def start_camera(self, instance):
        self.start_button.opacity = 0
        self.image_widget.opacity = 1

        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("⚠ Error: Unable to access camera")
            return

        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
        self.start_time = time.time()
        Clock.schedule_interval(self.check_capture_duration, 1)

    def update_frame(self, dt):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 0)  # Flip the frame vertically
                buf = frame.tobytes()  # Convert the frame to bytes
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image_widget.texture = texture
            else:
                print("⚠ Failed to capture frame.")

    def check_capture_duration(self, dt):
        elapsed_time = time.time() - self.start_time
        remaining_time = int(self.analysis_time - elapsed_time)
        self.countdown_label.text = str(remaining_time)

        if elapsed_time >= self.analysis_time:
            Clock.unschedule(self.check_capture_duration)
            self.countdown_label.text = "Done!"
            self.start_emotion_analysis()

    def start_emotion_analysis(self):
        self.detected_emotions = []
        Clock.schedule_interval(self.run_emotion_analysis, 0.2)
        Clock.schedule_once(self.enable_move_further, 1)

    def run_emotion_analysis(self, dt):
        if not self.capture or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions = result[0]['emotion']
            self.detected_emotions.append(emotions)
        except Exception as e:
            print(f"⚠ Emotion analysis failed: {e}")

    def enable_move_further(self, dt):
        if not self.detected_emotions:
            final_emotion = "Unknown"
        else:
            avg_emotions = {key: np.mean([d[key] for d in self.detected_emotions]) for key in self.detected_emotions[0]}
            if avg_emotions['angry'] + avg_emotions['fear'] > 40:
                final_emotion = "Stress"
            elif avg_emotions['fear'] + avg_emotions['sad'] > 40:
                final_emotion = "Anxiety"
            elif avg_emotions['sad'] + avg_emotions['neutral'] > 40:
                final_emotion = "Depression"
            else:
                final_emotion = "Neutral"

        print(f"✅ Final Detected Emotion: {final_emotion}")
        self.move_further_button.opacity = 1
        self.move_further_button.disabled = False

    def go_to_voice_analysis(self, instance):
        if self.capture:
            self.capture.release()
            self.capture = None
        self.manager.current = "voiceview"