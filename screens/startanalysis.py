from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

class StartAnalysisScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance

        # Main Layout
        self.layout = BoxLayout(orientation='vertical', spacing=30, padding=[50, 50])

        # Set background color
        with self.layout.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light pastel blue
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Motivational Quote
        self.quote_label = Label(
            text="Timely cure is better than treating later.\nSelf-care is more important.",
            font_size=22,
            italic=True,
            halign='center',
            color=[0.2, 0.2, 0.4, 1]
        )
        self.layout.add_widget(self.quote_label)

        # Start Analysis Button
        self.start_button = Button(
            text="Start the Analysis",
            size_hint=(0.6, None),
            height=70,
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1]
        )
        self.start_button.bind(on_press=self.go_to_facial_analysis)
        self.layout.add_widget(self.start_button)

        # Add layout to screen
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_to_facial_analysis(self, instance):
        """ Navigate to the facial analysis screen """
        self.app.root.current = "facialview"