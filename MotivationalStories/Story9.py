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

        # **Background Image (Faded for readability)**
        self.bg = Image(source=os.path.abspath("E:/WAZA/PRO/MotivationalStories/story9.png"),
                        allow_stretch=True, keep_ratio=False, opacity=0.1)  # **Subtle background**
        main_layout.add_widget(self.bg)

        # **Content Layout**
        content_layout = BoxLayout(orientation='vertical', padding=[50, 80], spacing=20, size_hint=(0.9, 0.9),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.55})  # **Centered and well-spaced**

        # **Story Headline (Bold & Large)**
        headline_label = Label(
            text="[b]The Echo in the Valley[/b]",
            font_size="38sp",
            halign="center",
            valign="middle",
            color=[1, 1, 1, 1],  # **White text for contrast**
            markup=True,
            size_hint=(1, 0.15)
        )
        content_layout.add_widget(headline_label)

        # **Story Text (3 Clear Paragraphs)**
        paragraph1 = """A boy was walking in the mountains when he shouted, “I am sad!” 
        To his surprise, the voice echoed back, “I am sad!”"""

        paragraph2 = """He got angry and yelled, “I hate you!” 
        The voice echoed, “I hate you!” Then his father said, “Try saying something nice.”"""

        paragraph3 = """The boy shouted, “I love you!” and the echo replied, “I love you!” 
        The father smiled and said, “Life is like this. Whatever you send out comes back to you.”"""

        # **Adding Paragraphs**
        for para in [paragraph1, paragraph2, paragraph3]:
            story_label = Label(
                text=para,
                font_size="22sp",
                halign="justify",
                valign="middle",
                color=[1, 1, 1, 1],  # **White text for readability**
                size_hint=(1, 0.3),
                text_size=(None, None),
                markup=True
            )
            content_layout.add_widget(story_label)

        # **Moral Section (Distinct Styling)**
        moral_label = Label(
            text="🌿 [b]Moral:[/b] The energy you put out into the world comes back to you. Stay positive.",
            font_size="24sp",
            halign="center",
            valign="middle",
            font_name="Roboto-BoldItalic",
            color=[1, 0.8, 0.4, 1],  # **Elegant gold-white color**
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
