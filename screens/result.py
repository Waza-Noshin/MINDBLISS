from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from collections import defaultdict

class ResultScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
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

        # � Tagline
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
            text="“Whether what emotion is detected, your next step against this for a positive impact is what really matters.”",
            font_size=16,
            color=(0.1, 0.1, 0.4, 1),
            size_hint=(1, None),
            height=65,
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.layout.add_widget(self.quote_label)

        # 📊 Final Emotion Display
        self.final_emotion_label = Label(
            text="Final Emotion: ",
            font_size=24,
            bold=True,
            color=(0.2, 0.2, 0.4, 1),
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.5}
        )
        self.layout.add_widget(self.final_emotion_label)

        # 😊 Emoji Display
        self.emoji_label = Label(
            text="",
            font_name="assets/NotoColorEmoji-Regular.ttf",
            font_size=50,
            size_hint=(1, None),
            height=100,
            pos_hint={"center_x": 0.5, "top": 0.4}
        )
        self.layout.add_widget(self.emoji_label)

        # 🎬 Show Recommendations Button
        self.recommendations_button = Button(
            text="Show Recommendations",
            size_hint=(None, None),
            size=(300, 70),
            pos_hint={"center_x": 0.5, "top": 0.2},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.recommendations_button.bind(on_press=self.show_recommendations)
        self.layout.add_widget(self.recommendations_button)

        # Dictionary to store emotions and their counts
        self.emotion_counts = defaultdict(int)

    def update_emotion(self, emotion):
        # Update the count for the detected emotion
        self.emotion_counts[emotion] += 1

        # Calculate the final emotion based on the most frequently occurring emotion
        final_emotion = self.calculate_final_emotion()

        # Update the final emotion label
        self.final_emotion_label.text = f"Final Emotion: {final_emotion}"

        # Update emoji based on the final emotion
        if "Depression" in final_emotion:
            self.emoji_label.text = "😔"
        elif "Stress" in final_emotion:
            self.emoji_label.text = "😫"
        elif "Anxiety" in final_emotion:
            self.emoji_label.text = "😰"
        else:
            self.emoji_label.text = "😊"

    def calculate_final_emotion(self):
        # Find the emotion with the highest count
        final_emotion = max(self.emotion_counts, key=self.emotion_counts.get)
        return final_emotion
    
    def reset_emotion_counts(self):
        self.emotion_counts = defaultdict(int)  # Reset counts
        self.final_emotion_label.text = "Final Emotion: "
        self.emoji_label.text = ""

    def start_new_session(self):
        result_screen = self.manager.get_screen('result')
        result_screen.reset_emotion_counts()
        self.manager.current = 'home'  # Navigate to home screen

    def show_recommendations(self, instance):
        # Navigate to the appropriate recommendation screen based on the final emotion
        final_emotion = self.final_emotion_label.text
        if "Depression" in final_emotion:
            self.manager.current = "reco_depression"
        elif "Stress" in final_emotion:
            self.manager.current = "reco_stress"
        elif "Anxiety" in final_emotion:
            self.manager.current = "reco_anxiety"