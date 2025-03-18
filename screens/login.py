from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.app import App

# Import the backend
from backend import backend

class LoginScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance  
        self.setup_ui()

    def setup_ui(self):
        # Background color
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light blue pastel
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])
        self.add_logo_and_tagline()
        self.add_login_form()
        self.add_widget(self.layout)

    def add_logo_and_tagline(self):
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

        # Tagline
        self.tagline = Label(
            text="Login to Continue...",
            font_size=18,
            color=(0.2, 0.2, 0.5, 1),
            halign="center",
            size_hint=(1, None),
            height=40
        )
        self.layout.add_widget(self.tagline)

    def add_login_form(self):
        # Username input
        self.username_input = TextInput(
            hint_text="Username",
            size_hint=(0.8, None),
            height=40,
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.username_input)

        # Password input
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.8, None),
            height=40,
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.password_input)

        # Login button
        self.login_button = Button(
            text="Login",
            size_hint=(0.5, None),
            height=40,
            pos_hint={"center_x": 0.5},
            background_color=[0.2, 0.6, 0.8, 1]
        )
        self.login_button.bind(on_press=self.authenticate_user)
        self.layout.add_widget(self.login_button)

        # Signup link
        signup_layout = BoxLayout(size_hint=(1, None), height=30, spacing=10)
        signup_layout.add_widget(Label(
            text="Don't have an Account?",
            size_hint=(0.7, None),
            color=(0.2, 0.2, 0.5, 1),
            height=30
        ))
        self.signup_button = Button(
            text="Signup",
            size_hint=(0.3, None),
            height=30,
            background_color=[0.2, 0.6, 0.8, 1]
        )
        self.signup_button.bind(on_press=self.go_to_signup)
        signup_layout.add_widget(self.signup_button)
        self.layout.add_widget(signup_layout)

    def authenticate_user(self, instance):
        """ Authenticate user credentials using MongoDB """
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.tagline.text = "Please enter both fields."
            return

        user_id = backend.login_user(username, password)
        if user_id:
            # Store the user's credentials in the app instance
            self.app.set_user_credentials(username, password)

            # Navigate to HomeScreen
            self.app.sm.current = 'home'
            # Clear input fields after login
            self.username_input.text = ""
            self.password_input.text = ""
        else:
            self.tagline.text = "Invalid username or password."

    def go_to_signup(self, instance):
        """ Navigate to Signup Screen """
        self.app.sm.current = 'signup'

    def _update_rect(self, instance, value):
        """Update background rectangle and circle position."""
        self.rect.size = instance.size
        self.rect.pos = instance.pos