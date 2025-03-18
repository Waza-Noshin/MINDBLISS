from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivyagg')  # Ensure correct backend
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
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

        # Graph Container
        self.graph_widget = BoxLayout(size_hint=(1, 0.7))
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
        """ Draw the emotion trend graph using Matplotlib and ensure rendering """
        emotions = ["Neutral", "Stress Detected", "Anxiety Detected", "Depression Detected"]
        counts = [self.emotion_data[emotion] for emotion in emotions]

        # Clear any previous figure
        plt.close('all')

        # Create a new figure
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(emotions, counts, color=['green', 'orange', 'yellow', 'red'])
        ax.set_title('Emotion Trend Analysis')
        ax.set_xlabel('Emotions')
        ax.set_ylabel('Frequency')
        ax.set_xticklabels(emotions, rotation=45)

        # Clear previous widgets in graph container
        self.graph_widget.clear_widgets()

        # Add Matplotlib graph to the Kivy layout
        graph_canvas = FigureCanvasKivyAgg(fig)
        self.graph_widget.add_widget(graph_canvas)

        print("Graph updated successfully!")  # Debugging statement


    def show_notification(self):
        """ Show a notification if negative emotions are detected more than 4 times """
        content = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10])
        content.add_widget(Label(
            text="We have noticed you are experiencing negative emotions frequently.\n"
                 "Kindly consider seeking professional help.",
            font_size=16,
            halign='center'
        ))

        close_button = Button(text="OK", size_hint=(1, None), height=40)
        popup = Popup(title="Professional Help Recommended", content=content, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)

        popup.open()

    def go_home(self, instance):
        """ Navigate back to HomeScreen """
        self.app.sm.current = 'home'
