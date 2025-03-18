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

        # **Background Image (Faint for Readability)**
        self.bg = Image(source=os.path.abspath("E:/WAZA/PRO/MotivationalStories/story4.png"),
                        allow_stretch=True, keep_ratio=False, opacity=0.1)  # **Low opacity for text visibility**
        main_layout.add_widget(self.bg)

        # **Content Layout**
        content_layout = BoxLayout(orientation='vertical', padding=[50, 80], spacing=20, size_hint=(0.9, 0.9),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.55})  # **Better text positioning**

        # **Story Headline (Bold)**
        headline_label = Label(
            text="[b]The Whispering Trees[/b]",
            font_size="38sp",  # **Prominent size**
            halign="center",
            valign="middle",
            color=[1, 1, 1, 1],  # **White for better visibility**
            markup=True,
            size_hint=(1, 0.15)
        )
        content_layout.add_widget(headline_label)

        # **Story Text (3 Clear Paragraphs)**
        paragraph1 = """A man was always anxious and stressed. 
        He sought advice from an old monk who took him to a quiet forest."""

        paragraph2 = """“Listen to the trees,” the monk said.  
        The man listened and heard the rustling leaves. "What are they saying?" he asked."""

        paragraph3 = """ "They are whispering, ‘This too shall pass.’ The seasons change, storms come and go, but the trees stand strong. 
        Life is the same. No matter what you face, it will pass." """

        # **Adding Paragraphs**
        for para in [paragraph1, paragraph2, paragraph3]:
            story_label = Label(
                text=para,
                font_size="22sp",  # **Readable font**
                halign="justify",
                valign="middle",
                color=[1, 1, 1, 1],  # **White text for contrast**
                size_hint=(1, 0.3),
                text_size=(None, None),
                markup=True
            )
            content_layout.add_widget(story_label)

        # **Moral Section (Styled Separately)**
        moral_label = Label(
            text="🌿 [b]Moral:[/b] No pain lasts forever. You will get through this.",
            font_size="24sp",
            halign="center",
            valign="middle",
            font_name="Roboto-BoldItalic",
            color=[1, 0.8, 0.4, 1],  # **Soft gold-white**
            size_hint=(1, 0.1),  # **Spacing adjusted**
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
