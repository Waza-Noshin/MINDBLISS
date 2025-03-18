from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.clock import Clock  # Import Clock for timed events
from backend import backend  # Import the backend

class DearMeScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])

        # Background Color
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light Grey-White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Motivational Quote
        self.title = Label(
            text="\"Sometimes writing down your thoughts helps clear your mind.\"",
            font_size=20,
            color=[0.3, 0.4, 0.7, 1],  # Blue Shade
            bold=True
        )
        self.layout.add_widget(self.title)

        # Text Input Box
        self.text_input = TextInput(
            hint_text="Write your thoughts here...",
            size_hint=(1, 0.5),
            background_color=[1, 1, 1, 1]
        )
        self.layout.add_widget(self.text_input)

        # Save Button
        self.save_button = Button(
            text="Save",
            size_hint=(0.5, None),
            height=60,
            pos_hint={'center_x': 0.5},
            background_color=[0.5, 0.2, 0.7, 1]  # Purple
        )
        self.save_button.bind(on_press=self.save_note)
        self.layout.add_widget(self.save_button)

        # Success/Error Message
        self.message_label = Label(
            text="",
            font_size=16,
            color=[0.2, 0.6, 0.2, 1],  # Green Text for Success
            size_hint=(1, None),
            height=30
        )
        self.layout.add_widget(self.message_label)

        # Show Scribblings Button
        self.show_notes_button = Button(
            text="Show My Scribblings",
            size_hint=(0.5, None),
            height=60,
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.7, 0.6, 1]  # Teal Shade
        )
        self.show_notes_button.bind(on_press=self.show_notes)
        self.layout.add_widget(self.show_notes_button)

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

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """ Update background when screen resizes """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def save_note(self, instance):
        """ Save the user’s note in MongoDB """
        note_text = self.text_input.text.strip()

        if not note_text:
            self.message_label.text = "Please enter text before saving."
            self.message_label.color = [0.8, 0.2, 0.2, 1]  # Red for error
            return

        # Get the logged-in user
        user = backend.login_user(self.app.username, self.app.password)
        if user:
            # Convert the ObjectId to a string
            user_id = str(user["_id"])
            # Save the note to the database
            backend.save_scribble(user_id, note_text)
            self.message_label.text = "✅ Your note has been saved successfully!"
            self.message_label.color = [0.2, 0.6, 0.2, 1]  # Green for success
            self.text_input.text = ""  # Clear the input field after saving

            # Clear the message after 5 seconds
            Clock.schedule_once(self.clear_message, 5)
        else:
            self.message_label.text = "⚠️ Please log in to save your note."
            self.message_label.color = [0.8, 0.2, 0.2, 1]  # Red for error

    def clear_message(self, dt):
        """ Clear the success/error message """
        self.message_label.text = ""

    def show_notes(self, instance):
        """ Navigate to the ScribblingsScreen """
        self.app.sm.current = 'scribblings'

    def go_home(self, instance):
        """ Navigate back to HomeScreen """
        self.app.sm.current = 'home'