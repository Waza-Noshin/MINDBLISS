from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.app import App
import re  # For email validation

# Import the backend
from backend import backend

# Email validation regex
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

class SignupScreen(Screen):
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
        self.add_signup_form()
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
            text="Create your Account",
            font_size=18,
            color=(0.2, 0.2, 0.5, 1),
            halign="center",
            size_hint=(1, None),
            height=40
        )
        self.layout.add_widget(self.tagline)

    def add_signup_form(self):
        # Username input
        self.username_input = TextInput(
            hint_text="Username",
            size_hint=(0.8, None),
            height=40,
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.username_input)

        # Email input
        self.email_input = TextInput(
            hint_text="Email",
            size_hint=(0.8, None),
            height=40,
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.email_input)

        # Password input
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.8, None),
            height=40,
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.password_input)

        # Confirm password input
        self.confirm_password_input = TextInput(
            hint_text="Confirm Password",
            password=True,
            size_hint=(0.8, None),
            height=40,
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.confirm_password_input)

        # Signup button
        self.signup_button = Button(
            text="Signup",
            size_hint=(0.5, None),
            height=40,
            pos_hint={"center_x": 0.5},
            background_color=[0.2, 0.6, 0.8, 1]
        )
        self.signup_button.bind(on_press=self.register_user)
        self.layout.add_widget(self.signup_button)

        # 🟡 "Already have an account? Login" button
        self.login_button = Button(
            text="Already have an account? Login",
            size_hint=(0.5, None),
            height=40,
            pos_hint={"center_x": 0.5},
            background_color=[0.5, 0.5, 0.5, 1]  # Light grey
        )
        self.login_button.bind(on_press=self.go_to_login)
        self.layout.add_widget(self.login_button)

    def register_user(self, instance):
        """ Register a new user using MongoDB """
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        if not username or not email or not password or not confirm_password:
            self.tagline.text = "Please fill in all fields."
            return

        if not re.match(EMAIL_REGEX, email):
            self.tagline.text = "Please enter a valid email address."
            return

        if password != confirm_password:
            self.tagline.text = "Passwords do not match."
            return

        # ✅ DEBUG: Check MongoDB insertion
        try:
            success = backend.register_user(username, email, password)
            if success:
                self.tagline.text = "Account created successfully!"
                self.app.sm.current = 'login'
            else:
                self.tagline.text = "Username or email already exists."
        except Exception as e:
            self.tagline.text = "Error registering user. Check backend!"
            print("[ERROR] Signup Failed:", e)

    def go_to_login(self, instance):
        """ Navigate to login screen """
        self.app.sm.current = 'login'

    def _update_rect(self, instance, value):
        """Update background rectangle position."""
        self.rect.size = instance.size
        self.rect.pos = instance.pos