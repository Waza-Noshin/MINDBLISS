from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from collections import defaultdict

class EmotionTrendScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.name = 'emotion_trend'
        self.app = app_instance
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])

        # Background Color
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light Grey-White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🔵 Circular Logo
        self.logo = Image(
            source="assets/logo_circle.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.logo)

        # 🏷 Tagline
        self.tagline = Label(
            text="Your Journey to Inner Peace and Emotional Well-Being",
            font_size=18,
            font_name="assets/custom_font.ttf",
            color=(0.2, 0.2, 0.5, 1),
            halign="center",
            size_hint=(1, None),
            height=40
        )
        self.layout.add_widget(self.tagline)

        # Title Label
        self.title_label = Label(
            text='Emotion Trend',
            font_size=24,
            color=(0.5, 0.2, 0.7, 1),
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(self.title_label)

        # 🔹 Motivational Quote
        self.quote_label = Label(
            text="Read the graph, grasp the truth, act wisely.",
            font_size=18,
            color=[0.1, 0.1, 0.4, 1],  # Dark Blue
            halign='center',
            size_hint=(1, None),
            height=40
        )
        self.layout.add_widget(self.quote_label)

        # Graph Placeholder
        self.graph_widget = Widget(size_hint=(1, 0.7))
        self.layout.add_widget(self.graph_widget)

        # Back to Home Button
        self.back_to_home_button = Button(
            text='Back to Home',
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1]  # Blue
        )
        self.back_to_home_button.bind(on_press=self.go_home)
        self.layout.add_widget(self.back_to_home_button)

        self.add_widget(self.layout)

        # Emotion data storage
        self.emotion_data = defaultdict(int)

    def _update_rect(self, instance, value):
        """ Update background when screen resizes """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def update_emotion_data(self, emotion):
        """ Update emotion data and redraw the graph """
        self.emotion_data[emotion] += 1
        self.draw_graph()

        # Check for negative emotions more than 4 times
        negative_emotions = ["Stress Detected", "Anxiety Detected", "Depression Detected"]
        negative_count = sum(self.emotion_data[emotion] for emotion in negative_emotions)
        if negative_count > 4:
            self.show_notification()

    def draw_graph(self):
        """ Draw the emotion trend graph using Matplotlib """
        emotions = ["Neutral", "Stress Detected", "Anxiety Detected", "Depression Detected"]
        counts = [self.emotion_data[emotion] for emotion in emotions]

        # Create a bar graph
        plt.figure(figsize=(6, 4))
        plt.bar(emotions, counts, color=['green', 'orange', 'yellow', 'red'])
        plt.title('Emotion Trend Analysis')
        plt.xlabel('Emotions')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)

        # Clear previous graph widget
        self.graph_widget.clear_widgets()

        # Embed the graph into the Kivy app
        graph_canvas = FigureCanvasKivyAgg(plt.gcf())
        self.graph_widget.add_widget(graph_canvas)

    def show_notification(self):
        """ Show a notification if negative emotions are detected more than 4 times """
        notification_popup = Popup(
            title='Professional Help Recommended',
            size_hint=(0.8, 0.4),
            content=Label(
                text="We have noticed you are experiencing negative emotions frequently.\n"
                     "Kindly consider seeking professional help.",
                font_size=18,
                halign='center'
            )
        )
        notification_popup.open()

    def go_home(self, instance):
        """ Navigate back to HomeScreen """
        self.app.sm.current = 'home'