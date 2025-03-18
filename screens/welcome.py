from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation

class WelcomeScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance  # Store app instance

        # 🌈 Background Color (Soft Blue)
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light pastel blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🌟 Layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])

        # 🔵 Circular Logo
        self.logo = Image(
            source="assets/logo_circle.png",  # Use the circular logo
            size_hint=(None, None),
            size=(200, 200),  # Adjust size as needed
            pos_hint={"center_x": 0.5}
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
            height=40
        )
        self.layout.add_widget(self.tagline)

        # 🎉 Welcome Text (Appears First)
        self.welcome_text = Label(
            text="Welcome to MindBliss",
            font_size=30,
            bold=True,
            color=(0.2, 0.2, 0.6, 1),
            opacity=0,  # Initially Hidden
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.welcome_text)

        # 💬 Motivational Quote (Appears After Welcome Text)
        self.quote = Label(
            text="",
            font_size=18,
            italic=True,
            color=(0.4, 0.4, 0.8, 1),
            opacity=0,  # Initially Hidden
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.quote)

        # ⏳ Get Started Button (Appears Last)
        self.get_started_button = Button(
            text="Get Started",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1],
            opacity=0,  # Initially Hidden
            disabled=True  # Initially Disabled
        )
        self.get_started_button.bind(on_press=self.go_to_next_screen)
        self.layout.add_widget(self.get_started_button)

        self.add_widget(self.layout)

        # 🎬 Schedule Animations
        Clock.schedule_once(self.show_welcome_text, 1)
        Clock.schedule_once(self.show_quote, 8)
        Clock.schedule_once(self.show_get_started_button, 10)
        

    def _update_rect(self, instance, value):
        """Update background rectangle and logo position."""
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def show_welcome_text(self, dt):
        """Fade in the welcome text first."""
        anim = Animation(opacity=1, duration=1)
        anim.start(self.welcome_text)
        Clock.schedule_once(self.fade_welcome_text, 2)

    def fade_welcome_text(self, dt):
        """Fades out the welcome text after 2 seconds."""
        anim = Animation(opacity=0, duration=1)
        anim.start(self.welcome_text)

    def show_quote(self, dt):
        """Displays a motivational quote after the welcome text disappears."""
        self.quote.text = "Every day is a new beginning!\n    Take a deep breath and start."
        anim = Animation(opacity=1, duration=1)
        anim.start(self.quote)

    def show_get_started_button(self, dt):
        """Shows and enables the Get Started button."""
        anim = Animation(opacity=1, duration=1)
        anim.start(self.get_started_button)
        self.get_started_button.disabled = False

    def go_to_next_screen(self, instance):
        """Redirects the user to the correct screen based on authentication status."""
        if self.is_user_logged_in():
            self.manager.current = 'home'  # Redirect to Home if logged in
        else:
            self.manager.current = 'login'  # Otherwise, go to Login

    def is_user_logged_in(self):
        """Checks if a user is logged in (handled via app_instance)."""
        return self.app_instance.is_user_logged_in()

    def auto_redirect(self, dt):
        """Automatically redirects if the user is already logged in."""
        if self.is_user_logged_in():
            self.manager.current = 'home'