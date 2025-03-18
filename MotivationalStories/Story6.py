from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
import os

class StoryScreen(Screen):
    def __init__(self, app, **kwargs):
        super(StoryScreen, self).__init__(**kwargs)
        self.app = app

        # **Main Layout**
        main_layout = RelativeLayout()

        # **Background Image (Low opacity for readability)**
        self.bg = Image(source=os.path.abspath("E:/WAZA/PRO/MotivationalStories/story6.png"),
                        allow_stretch=True, keep_ratio=False, opacity=0.1)  # **Light background for contrast**
        main_layout.add_widget(self.bg)

        # **Content Layout**
        content_layout = BoxLayout(orientation='vertical', padding=[50, 80], spacing=20, size_hint=(0.9, 0.9),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.55})  # **Balanced positioning**

        # **Story Headline (Bold & Large)**
        headline_label = Label(
            text="[b]The Starfish Story[/b]",
            font_size="38sp",
            halign="center",
            valign="middle",
            color=[1, 1, 1, 1],  # **White for clarity**
            markup=True,
            size_hint=(1, 0.15)
        )
        content_layout.add_widget(headline_label)

        # **Story Text (3 Clear Paragraphs)**
        paragraph1 = """A man was walking along the beach when he saw thousands of starfish washed ashore. 
        A young boy was picking them up, one by one, and throwing them back into the ocean."""

        paragraph2 = """The man asked, “Why are you doing this? You can’t save them all.”"""

        paragraph3 = """The boy picked up another starfish, tossed it into the waves, and said, 
        “I made a difference for that one.”"""

        # **Adding Paragraphs**
        for para in [paragraph1, paragraph2, paragraph3]:
            story_label = Label(
                text=para,
                font_size="22sp",
                halign="justify",
                valign="middle",
                color=[1, 1, 1, 1],  # **White text for contrast**
                size_hint=(1, 0.3),
                text_size=(None, None),
                markup=True
            )
            content_layout.add_widget(story_label)

        # **Moral Section (Distinct Styling)**
        moral_label = Label(
            text="🌿 [b]Moral:[/b] Even small acts of kindness matter. Never underestimate the impact you can have.",
            font_size="24sp",
            halign="center",
            valign="middle",
            font_name="Roboto-BoldItalic",
            color=[1, 0.8, 0.4, 1],  # **Soft gold-white for a premium look**
            size_hint=(1, 0.1),
            text_size=(None, None),
            markup=True
        )
        content_layout.add_widget(moral_label)

        # **Back Button (Fixed Positioning)**
        back_button = Button(
            text="Back to Stories",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=[0.1, 0.6, 0.9, 1],  # **Professional blue**
            color=[1, 1, 1, 1]
        )
        back_button.bind(on_press=self.go_back)
        content_layout.add_widget(back_button)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def go_back(self, instance):
        """ Navigate back to the Motivational Stories screen """
        self.app.root.current = 'motivational_stories'
