from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import webbrowser

class RecoDepressionScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super(RecoDepressionScreen, self).__init__(**kwargs)
        self.app = app_instance  # Pass the app instance
        self.setup_ui()

    def setup_ui(self):
        # Set window background color
        Window.clearcolor = (0.9, 0.9, 1, 1)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])
        self.add_widget(self.layout)

        # 🔵 Circular Logo
        self.logo = Image(
            source="assets/logo_circle.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        self.layout.add_widget(self.logo)

        # 🏷 Tagline
        self.tagline = Label(
            text="Your Journey to Inner Peace and Emotional Well-Being",
            font_size=18,
            font_name="assets/custom_font.ttf",  # Ensure this points to the correct font file
            color=(0.2, 0.2, 0.5, 1),
            halign="center",
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(self.tagline)

        # 🎵 Music Button
        self.music_button = Button(
            text="Music",
            size_hint=(None, None),
            size=(300, 70),
            pos_hint={"center_x": 0.5, "top": 0.7},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.music_button.bind(on_press=self.open_depression_music)
        self.layout.add_widget(self.music_button)

        # 🎙️ Podcast Button
        self.podcast_button = Button(
            text="Podcast",
            size_hint=(None, None),
            size=(300, 70),
            pos_hint={"center_x": 0.5, "top": 0.5},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.podcast_button.bind(on_press=self.open_depression_podcast)
        self.layout.add_widget(self.podcast_button)

        # 📖 Success Stories Button
        self.stories_button = Button(
            text="Success Stories",
            size_hint=(None, None),
            size=(300, 70),
            pos_hint={"center_x": 0.5, "top": 0.3},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.stories_button.bind(on_press=self.open_depression_stories)
        self.layout.add_widget(self.stories_button)

        # 🧘 Breathing Exercises Button
        self.breathing_button = Button(
            text="Breathing Exercises",
            size_hint=(None, None),
            size=(300, 70),
            pos_hint={"center_x": 0.5, "top": 0.1},
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.breathing_button.bind(on_press=self.open_breathing_exercises)
        self.layout.add_widget(self.breathing_button)

        # Back to Home Button
        self.back_button = Button(
            text="Back to Home",
            size_hint=(0.5, None),
            height=60,
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1]  # Blue
        )
        self.back_button.bind(on_press=self.go_home)
        self.layout.add_widget(self.back_button)

    def open_depression_music(self, instance):
        # Redirect to Depression Music Playlist on Spotify
        webbrowser.open("https://open.spotify.com/playlist/4ObM9QfYxMnRyFXMVtOJGH?si=8EEXU0LRTKajPKCl2IAJCA&pi=W0Y4rHLlQ3G2u")

    def open_depression_podcast(self, instance):
        # Redirect to Depression Podcast Playlist on Spotify
        webbrowser.open("https://open.spotify.com/show/7ADkjXwA5v9nSg7aYmnEEt?si=LpsmR2PmQH2pVqxhjm9s1g")

    def open_depression_stories(self, instance):
        # Redirect to Depression Success Stories Playlist on Spotify
        webbrowser.open("https://youtube.com/playlist?list=PLfX83djbCFH_3AL7Y7uahu2Ku9mirTyD5&si=pI4hqCI-b9UBHFQN")

    def open_breathing_exercises(self, instance):
        # Redirect to Breathing Exercises Playlist on YouTube
        webbrowser.open("https://youtube.com/playlist?list=PLaMm5Ot_fDYTQaYOAbCwkMR1mQ-PYDwOC&feature=shared")

    def go_home(self, instance):
        """ Navigate back to HomeScreen """
        self.manager.current = 'home'  # Use self.manager to access the ScreenManager