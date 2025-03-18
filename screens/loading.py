from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 🌈 Background Color (Soft Blue)
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light pastel blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🌟 Layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])

        # 🔵 Circular Logo (Centered)
        self.logo = Image(
            source="assets/logo_circle.png",  # Use the circular logo
            size_hint=(None, None),
            size=(200, 200),  # Adjust size as needed
            pos_hint={"center_x": 0.5, "center_y": 0.55}  # Centered
        )
        self.add_widget(self.logo)

        # 🏷 Loading Text (Centered Below Logo & Bold)
        self.loading_text = Label(
            text="Loading...",
            font_size=20,
            bold=True,  # Bold text
            color=(0.2, 0.2, 0.5, 1),
            size_hint=(None, None),
            height=40,
            pos_hint={"center_x": 0.5, "center_y": 0.4}  # Positioned below the logo
        )
        self.add_widget(self.loading_text)

        # 🎬 Automatically switch to Welcome screen after 2 seconds
        Clock.schedule_once(self.switch_to_welcome,10)

    def _update_rect(self, instance, value):
        """Update background rectangle and logo position."""
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def switch_to_welcome(self, dt):
        """Switch to the Welcome screen."""
        self.manager.current = 'welcome'