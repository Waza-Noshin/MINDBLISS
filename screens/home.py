from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

class HomeScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.app = app_instance

        # Set background color
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light pastel blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # **Top Bar with Logo & Welcome Message**
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'top': 1})
        self.logo = Label(
            text="MindBliss", font_size=30, bold=True,
            size_hint=(0.5, 1), color=[0.2, 0.4, 0.6, 1]
        )
        self.welcome_text = Label(
            text="Welcome, Guest", font_size=20,
            size_hint=(0.5, 1), color=[0.2, 0.2, 0.2, 1]
        )
        self.top_bar.add_widget(self.logo)
        self.top_bar.add_widget(self.welcome_text)
        self.add_widget(self.top_bar)

        # **Motivational Quote + Let's Get Started Button**
        self.middle_section = BoxLayout(orientation='vertical', size_hint=(1, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.55})
        self.quote_label = Label(
            text="“Self-analysis is the first step to well-being.\nAct before things become harmful.”",
            font_size=18, bold=True,
            color=[0.1, 0.1, 0.4, 1],  # Dark Blue
            halign='center',
            size_hint=(1, 0.6)
        )
        self.lets_start_button = Button(
            text="Let's Start",
            size_hint=(None, None),
            size=(220, 70),  # Width x Height
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1],  # Deep Blue
            color=[1, 1, 1, 1],  # White text
            bold=True
        )
        self.lets_start_button.bind(on_press=self.go_to_lets_start)
        self.middle_section.add_widget(self.quote_label)
        self.middle_section.add_widget(self.lets_start_button)
        self.add_widget(self.middle_section)

        # **Bottom Navigation Bar**
        self.bottom_nav = GridLayout(cols=4, rows=1, size_hint=(1, 0.1), pos_hint={'bottom': 1})

        motivational_stories_btn = Button(
            text="Motivational\nStories",
            background_color=[0.2, 0.6, 0.8, 1], bold=True,
            color=[1, 1, 1, 1]
        )
        motivational_stories_btn.bind(on_press=self.go_to_motivational_stories)
        self.bottom_nav.add_widget(motivational_stories_btn)

        dear_me_btn = Button(
            text="Dear Me", background_color=[0.2, 0.6, 0.8, 1], bold=True,
            color=[1, 1, 1, 1]
        )
        dear_me_btn.bind(on_press=self.go_to_dear_me)
        self.bottom_nav.add_widget(dear_me_btn)

        emotion_trend_btn = Button(
            text="Emotion\nTrend", background_color=[0.2, 0.6, 0.8, 1], bold=True,
            color=[1, 1, 1, 1]
        )
        emotion_trend_btn.bind(on_press=self.go_to_emotion_trends)
        self.bottom_nav.add_widget(emotion_trend_btn)

        user_profile_btn = Button(
            text="User\nProfile", background_color=[0.2, 0.6, 0.8, 1], bold=True,
            color=[1, 1, 1, 1]
        )
        user_profile_btn.bind(on_press=self.go_to_user_profile)
        self.bottom_nav.add_widget(user_profile_btn)

        self.add_widget(self.bottom_nav)

    def _update_rect(self, instance, value):
        """ Update background size when the window resizes """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def get_logged_in_user(self):
        """ Fetch the latest logged-in user from MongoDB every time it's accessed """
        app = App.get_running_app()
        user = app.users_collection.find_one({"is_logged_in": True})

        if user:
            username = user["username"]
            self.welcome_text.text = f"Welcome, {username}"
        else:
            self.welcome_text.text = "Welcome, Guest"

    def on_pre_enter(self):
        """ Refresh username before the screen is entered """
        self.get_logged_in_user()

    def go_to_lets_start(self, instance):
        """ Navigate to Let's Start Screen """
        self.app.root.current = 'letsstart'

    def go_to_motivational_stories(self, instance):
        """ Navigate to Motivational Stories Screen """
        self.app.root.current = 'motivational_stories'

    def go_to_dear_me(self, instance):
        """ Navigate to Dear Me Screen """
        self.app.root.current = 'dear_me'

    def go_to_emotion_trends(self, instance):
        """ Navigate to Emotion Trends Screen """
        self.app.root.current = 'emotion_trends'

    def go_to_user_profile(self, instance):
        """ Navigate to User Profile Screen """
        self.app.root.current = 'user_profile'