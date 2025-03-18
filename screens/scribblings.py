from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from backend import backend
from bson.objectid import ObjectId  # Import ObjectId for MongoDB

class ScribblingsScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])

        # Background Color
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light Grey-White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Logo
        self.logo = Image(
            source="assets/logo_circle.png",  # Ensure this path is correct
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(self.logo)

        # 🏷 Tagline (Different Font)
        self.tagline = Label(
            text="Your Journey to Inner Peace and Emotional Well-Being",
            font_size=18,
            font_name="assets/custom_font.ttf",  # Ensure this points to the correct font file
            color=(0.2, 0.2, 0.5, 1),
            halign="center",
            size_hint=(1, None),
            height=40
        )
        self.layout.add_widget(self.tagline)

        # ✅ Add ScrollView for scribblings
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scribblings_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.scribblings_container.bind(minimum_height=self.scribblings_container.setter('height'))
        self.scroll_view.add_widget(self.scribblings_container)
        self.layout.add_widget(self.scroll_view)

        # Back to Writing Button
        self.back_to_writing_button = Button(
            text="Back to Writing",
            size_hint=(0.5, None),
            height=60,
            pos_hint={'center_x': 0.5},
            background_color=[0.5, 0.2, 0.7, 1]  # Purple
        )
        self.back_to_writing_button.bind(on_press=self.go_to_writing)
        self.layout.add_widget(self.back_to_writing_button)

        # Back to Home Button
        self.back_to_home_button = Button(
            text="Back to Home",
            size_hint=(0.5, None),
            height=60,
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

    def on_pre_enter(self, *args):
        """ Fetch and display scribblings when the screen is about to be displayed """
        print("Loading scribblings...")
        self.scribblings_container.clear_widgets()

        # Get the logged-in user
        user = backend.login_user(self.app.username, self.app.password)
        if user:
            print(f"Logged-in user: {user}")
            # Handle both cases: user is an ObjectId or a dictionary
            user_id = user["_id"] if isinstance(user, dict) else user
            print(f"User ID: {user_id}")
            scribblings = backend.get_scribblings(user_id)
            if scribblings:
                print(f"Found {len(scribblings)} scribblings.")
                for scribble in scribblings:
                    # Create a new TextInput for each scribble
                    scribble_box = TextInput(
                        text=scribble["note"],
                        size_hint=(1, None),
                        height=100,
                        background_color=[1, 1, 1, 1],
                        readonly=True  # Make the TextInput read-only
                    )
                    self.scribblings_container.add_widget(scribble_box)
            else:
                print("No scribblings found.")
                # Display a message if no scribblings are found
                no_notes_label = Label(
                    text="No scribblings found.",
                    font_size=16,
                    color=[0.8, 0.2, 0.2, 1],  # Red for error
                    size_hint=(1, None),
                    height=30
                )
                self.scribblings_container.add_widget(no_notes_label)
        else:
            print("User not logged in.")
            # Display a message if the user is not logged in
            login_label = Label(
                text="⚠️ Please log in to view your scribblings.",
                font_size=16,
                color=[0.8, 0.2, 0.2, 1],  # Red for error
                size_hint=(1, None),
                height=30
            )
            self.scribblings_container.add_widget(login_label)
            
    def go_to_writing(self, instance):
        """ Navigate back to the DearMeScreen """
        if "dear_me" in self.app.sm.screen_names:  # ✅ Check correct screen name
            self.app.sm.current = 'dear_me'
        else:
            print("Error: 'dear_me' screen not found!")

    def go_home(self, instance):
        """ Navigate back to HomeScreen """
        self.app.sm.current = 'home'