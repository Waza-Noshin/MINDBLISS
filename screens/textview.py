from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
import sys
sys.path.append("E:\\WAZA\\MINDBLISS\\core")
from core.text_analysis import analyze_emotion

class TextViewScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super(TextViewScreen, self).__init__(**kwargs)
        self.app = app_instance

        # Set window background color
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

        # 🏷 Tagline
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
            text="“Your words reveal your emotions.\nWrite freely and let us help you understand.”",
            font_size=16,
            color=(0.1, 0.1, 0.4, 1),
            size_hint=(1, None),
            height=65,
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.layout.add_widget(self.quote_label)

        # 📝 Text Input Box
        self.text_input = TextInput(
            hint_text="Write your thoughts here...",
            size_hint=(0.8, 0.4),  # Reduced width to create 2cm margins
            pos_hint={"center_x": 0.5, "top": 0.6},
            multiline=True,
            font_size=16,
            padding=[10, 10]
        )
        self.layout.add_widget(self.text_input)

        # 🎬 Submit Button
        self.submit_button = Button(
            text="Submit",
            size_hint=(None, None),
            size=(250, 70),
            pos_hint={"center_x": 0.5, "top": 0.3},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.submit_button.bind(on_press=self.analyze_text)
        self.layout.add_widget(self.submit_button)

    def on_emotion_detected(self, emotion):
        # Pass the detected emotion to the ResultScreen
        result_screen = self.manager.get_screen('result')
        result_screen.update_emotion(emotion)
        
    def analyze_text(self, instance):
        user_text = self.text_input.text.strip()
        if not user_text:
            self.show_error("Please enter some text before submitting.")
            return

        # Analyze emotion using the text_analysis.py function
        emotion = analyze_emotion(user_text)
        print(f"📊 Emotion Detected: {emotion}")  # Display emotion in the terminal

        # Navigate to the result screen
        self.manager.get_screen("result").update_emotion(emotion)
        self.manager.current = "result"

    def show_error(self, message):
        # Remove existing error label if any
        if hasattr(self, 'error_label'):
            self.layout.remove_widget(self.error_label)

        # Add new error label
        self.error_label = Label(
            text=message,
            font_size=16,
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 0.2}
        )
        self.layout.add_widget(self.error_label)
        Clock.schedule_once(lambda dt: self.layout.remove_widget(self.error_label), 2)