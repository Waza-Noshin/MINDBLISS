from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
import importlib
import os
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class MotivationalStoriesScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.initial_stories = ["Story 1", "Story 2", "Story 3", "Story 4"]
        self.more_stories = ["Story 5", "Story 6", "Story 7", "Story 8", "Story 9", "Story 10"]
        self.showing_initial_stories = True  

        # Main Layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])


        # Set background color
        with self.layout.canvas.before:
            Color(0.9, 0.9, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)


        # Motivational Quote
        self.quote = Label(
            text="Reading motivational stories energizes the mind and fuels success!",
            font_size=18, color=[0.2, 0.2, 0.2, 1], halign='center'
        )
        self.layout.add_widget(self.quote)


        # Story Buttons Layout
        self.story_layout = BoxLayout(orientation='vertical', spacing=10)
        self.layout.add_widget(self.story_layout)


        # Load Initial Stories
        self.load_stories(self.initial_stories)


        # More Stories Button
        self.more_stories_button = Button(
            text="More Stories", size_hint=(0.5, None), height=70,
            pos_hint={'center_x': 0.5}, background_color=[0.5, 0.5, 0.7, 1]
        )
        self.more_stories_button.bind(on_press=self.show_more_stories)
        self.layout.add_widget(self.more_stories_button)


        # Back to Initial Stories Button (Initially hidden)
        self.back_to_initial_button = Button(
            text="Back to Initial Stories", size_hint=(0.5, None), height=70,
            pos_hint={'center_x': 0.5}, background_color=[0.5, 0.5, 0.7, 1]
        )
        self.back_to_initial_button.bind(on_press=self.show_initial_stories)
        self.back_to_initial_button.opacity = 0  
        self.back_to_initial_button.disabled = True
        self.layout.add_widget(self.back_to_initial_button)


        # Back to Home Button
        self.back_button = Button(
            text="Back to Home", size_hint=(0.5, None), height=70,
            pos_hint={'center_x': 0.5}, background_color=[0.2, 0.6, 0.8, 1],
            color=[1, 1, 1, 1]
        )
        self.back_button.bind(on_press=self.go_home)
        self.layout.add_widget(self.back_button)


        self.add_widget(self.layout)


    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


    def load_stories(self, stories):
        self.story_layout.clear_widgets()
        for title in stories:
            btn = Button(
                text=title, size_hint=(0.8, None), height=60,
                pos_hint={'center_x': 0.5}, background_color=[0.5, 0.5, 0.7, 1]
            )
            btn.bind(on_press=self.open_story)
            self.story_layout.add_widget(btn)


    def show_more_stories(self, instance):
        self.load_stories(self.more_stories)
        self.more_stories_button.opacity = 0  
        self.more_stories_button.disabled = True
        self.back_to_initial_button.opacity = 1  
        self.back_to_initial_button.disabled = False
        self.showing_initial_stories = False


    def show_initial_stories(self, instance):
        self.load_stories(self.initial_stories)
        self.back_to_initial_button.opacity = 0  
        self.back_to_initial_button.disabled = True
        self.more_stories_button.opacity = 1  
        self.more_stories_button.disabled = False
        self.showing_initial_stories = True


    def open_story(self, instance):
        
        """ Dynamically load the correct story screen """
        story_name = instance.text.replace(" ", "")  # Convert "Story 1" → "Story1"
        story_screen_name = f"{story_name}_screen"

        # ✅ Use `self.app_instance.sm` instead of `self.app.root`
        if not self.app_instance.sm.has_screen(story_screen_name):
            story_module_path = f"MotivationalStories.{story_name}"
            if os.path.exists(f"MotivationalStories/{story_name}.py"):
                try:
                    # Dynamically import the story module
                    story_module = importlib.import_module(story_module_path)
                    # ✅ Pass `app_instance` as `app`
                    story_screen = story_module.StoryScreen(name=story_screen_name, app=self.app_instance)
                    self.app_instance.sm.add_widget(story_screen)
                except ModuleNotFoundError:
                    print(f"Error: {story_name}.py file not found!")
                except AttributeError:
                    print(f"Error: {story_name}.py does not define a 'StoryScreen' class!")
            else:
                print(f"Error: {story_name}.py does not exist in MotivationalStories folder!")

        # ✅ Switch screen properly
        self.app_instance.sm.current = story_screen_name

    def go_home(self, instance):
        """ Navigate back to the Home Screen """
        self.app_instance.sm.current = 'home'  # ✅ Use `app_instance.sm` instead of `app.root`
