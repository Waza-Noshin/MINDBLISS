from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle

Builder.load_string('''
<ForgotPasswordScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Image:
            source: 'assets/logo.png'
            size_hint: (0.5, 0.5)
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'Your Journey to Inner Peace and Emotional Well-Being'
            font_name: 'assets/custom_font.ttf'  # Replace with your font
            font_size: 14
            size_hint_y: None
            height: 30

        Label:
            text: 'Forgot Password?'
            font_size: 18
            size_hint_y: None
            height: 30

        TextInput:
            id: email
            hint_text: 'Enter your email'
            size_hint_y: None
            height: 40

        Button:
            text: 'Reset Password'
            size_hint_y: None
            height: 40
            on_release: app.root.current = 'login'

        Button:
            text: 'Back to Login'
            size_hint_y: None
            height: 30
            background_color: (0, 0, 0, 0)  # Transparent background
            color: (0, 0.5, 1, 1)  # Blue text
            on_release: app.root.current = 'login'
''')

class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # Light Grey-White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """ Update background when screen resizes """
        self.rect.size = instance.size
        self.rect.pos = instance.pos