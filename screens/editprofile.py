from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class EditProfileScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance  # Reference to the main app instance

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])

        # Heading
        self.layout.add_widget(Label(text="Edit Profile", font_size=24, size_hint_y=None, height=50))

        # Name Field
        self.name_input = TextInput(hint_text="Enter your name", size_hint=(1, 0.1))
        self.layout.add_widget(self.name_input)

        # Email Field (Read-only)
        self.email_input = TextInput(hint_text="Email (Cannot be changed)", size_hint=(1, 0.1), readonly=True)
        self.layout.add_widget(self.email_input)

        # Update Button
        self.update_button = Button(text="Update Profile", size_hint=(1, 0.1))
        self.update_button.bind(on_press=self.update_profile)
        self.layout.add_widget(self.update_button)

        # Back Button (✅ Fixed Syntax)
        self.back_button = Button(text="Back to Profile", size_hint=(1, 0.1))
        self.back_button.bind(on_press=lambda x: setattr(self.app.sm, 'current', 'user_profile'))  # ✅ Fixed Syntax
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def update_profile(self, instance):
        """Update user profile in the database"""
        new_name = self.name_input.text.strip()
        if not new_name:
            print("⚠ Name cannot be empty.")
            return

        user_email = self.app.current_user_email
        if not user_email:
            print("⚠ No logged-in user found.")
            return

        # Update database with new name
        self.app.db.update_one({"email": user_email}, {"$set": {"name": new_name}})
        print("✅ Profile updated successfully!")

        # Go back to User Profile
        self.app.sm.current = "user_profile"
