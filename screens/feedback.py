from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import smtplib


class FeedbackScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])

        # Background Color
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
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

        # 📌 Motivational Quote
        self.quote_label = Label(text="Give me the right feedback at the right time.\n     It helps us to improve.",
        font_size=18, color=(0.1, 0.1, 0.4, 1))
        self.layout.add_widget(self.quote_label)

        # 📝 Feedback Text Box
        self.feedback_input = TextInput(hint_text="Enter your feedback (max 100 words)...", size_hint=(1, None), height=100, multiline=True)
        self.layout.add_widget(self.feedback_input)

        # ✉ Send Feedback Button
        self.send_button = Button(text="Send Feedback", size_hint=(0.5, None), height=50, pos_hint={"center_x": 0.5}, background_color=[0.2, 0.6, 0.8, 1])
        self.send_button.bind(on_press=self.send_feedback)
        self.layout.add_widget(self.send_button)

        # 🏠 Back to Home Button
        self.back_to_home_button = Button(text="Back to Home", size_hint=(0.5, None), height=50, pos_hint={"center_x": 0.5}, background_color=[0.2, 0.6, 0.8, 1])
        self.back_to_home_button.bind(on_press=self.go_home)
        self.layout.add_widget(self.back_to_home_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """ ✅ Fix: Update background when screen resizes """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def send_feedback(self, instance):
        sender_email = "your-email@gmail.com"
        sender_password = "your-app-password"

        message = f"Subject: MindBliss Feedback\n\n{self.feedback_input.text}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, "developermindbliss@gmail.com", message)
            server.quit()
            print("✅ Feedback Sent Successfully!")
        except smtplib.SMTPAuthenticationError:
            print("❌ SMTP Authentication Failed! Check your email/password settings.")

    def go_home(self, instance):
        self.app.sm.current = "home"
