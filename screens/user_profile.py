from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import pymongo


class UserProfileScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.db = pymongo.MongoClient("mongodb://localhost:27017/")["mindbliss"]["users"]  # MongoDB connection
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])

        # Background Color
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # Light Grey-White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🔵 Profile Picture
        self.profile_image = Image(
            source="assets/default_profile.png",
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.profile_image)

        # 📌 Title Label
        self.title_label = Label(
            text='User Profile',
            font_size=24,
            color=(0.2, 0.2, 0.5, 1),
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(self.title_label)

        # 📌 Username Display
        self.username_label = Label(
            text="Username: Loading...",
            font_size=18,
            color=(0.1, 0.1, 0.4, 1),
            size_hint=(1, None),
            height=30
        )
        self.layout.add_widget(self.username_label)

        # 📌 Email Display
        self.email_label = Label(
            text="Email: Loading...",
            font_size=18,
            color=(0.1, 0.1, 0.4, 1),
            size_hint=(1, None),
            height=30
        )
        self.layout.add_widget(self.email_label)

        # Fetch User Details
        self.load_user_details()

        # ✏ Edit Profile Button
        self.edit_profile_button = Button(
            text="Edit Profile",
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1]  # Blue
        )
        self.edit_profile_button.bind(on_press=self.go_to_edit_profile)
        self.layout.add_widget(self.edit_profile_button)

        # 📝 Feedback Button
        self.feedback_button = Button(
            text="Feedback",
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5},
            background_color=[0.5, 0.3, 0.7, 1]  # Purple
        )
        self.feedback_button.bind(on_press=self.go_to_feedback)
        self.layout.add_widget(self.feedback_button)

        # 🏠 Back to Home Button
        self.back_to_home_button = Button(
            text="Back to Home",
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5},
            background_color=[0.2, 0.6, 0.8, 1]  # Blue
        )
        self.back_to_home_button.bind(on_press=self.go_home)
        self.layout.add_widget(self.back_to_home_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """ Update background when screen resizes """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def load_user_details(self):
        """ Load user details from MongoDB and update the UI """
        if not self.app.current_user_email:
            print("⚠ No user email found. Defaulting to Guest mode.")
            self.username_label.text = "Username: Guest"
            self.email_label.text = "Email: Not Logged In"
            return

        user = self.db.find_one({"email": self.app.current_user_email})
        if user:
            self.username_label.text = f"Username: {user.get('username', 'Unknown')}"
            self.email_label.text = f"Email: {user.get('email', 'Unknown')}"
        else:
            print("⚠ User not found in database.")

    def go_to_edit_profile(self, instance):
        """ Navigate to Edit Profile Screen """
        if "edit_profile" in self.app.sm.screen_names:
            self.app.sm.current = "edit_profile"
        else:
            print("⚠ Error: Edit Profile screen is not found in ScreenManager.")

    def go_to_feedback(self, instance):
        """ Navigate to Feedback Screen """
        if "feedback" in self.app.sm.screen_names:
            self.app.sm.current = "feedback"
        else:
            print("⚠ Error: Feedback screen is not found in ScreenManager.")

    def go_home(self, instance):
        """ Navigate to HomeScreen """
        self.app.sm.current = 'home'
