from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

# Sample Questions for the Let's Start Screen
QUESTIONS = [
    ("How are you feeling today?", ["Happy", "Sad", "Anxious", "Stressed"]),
    ("Do you often feel overwhelmed?", ["Never", "Sometimes", "Often", "Always"]),
    ("How well did you sleep last night?", ["Very well", "Okay", "Not great", "Terrible"]),
    ("Do you feel motivated to do daily activities?", ["Yes", "A little", "Not really", "Not at all"]),
    ("Have you been avoiding social interactions?", ["Not at all", "Sometimes", "Often", "Always"]),
    ("How is your energy level today?", ["High", "Moderate", "Low", "Very Low"]),
    ("Do you often feel hopeless?", ["Never", "Rarely", "Sometimes", "Often"])
]

class LetsStartedScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.current_question = 0
        self.responses = []
        
        # Main Layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])
        
        # Set background color
        with self.layout.canvas.before:
            Color(0.9, 0.9, 1, 1)  # Light pastel blue
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Question Label
        self.question_label = Label(text="", font_size=24, bold=True, halign='center', color=[0.2, 0.2, 0.4, 1], size_hint=(1, 0.3))
        self.layout.add_widget(self.question_label)
        
        # Answer Buttons Layout inside a separate BoxLayout for aesthetics
        self.answer_container = BoxLayout(orientation='vertical', spacing=15, padding=[20, 20], size_hint=(1, 0.7))
        self.answer_layout = BoxLayout(orientation='vertical', spacing=10)
        self.answer_container.add_widget(self.answer_layout)
        self.layout.add_widget(self.answer_container)
        
        # Load First Question
        self.load_question()
        
        # Add Layout to Screen
        self.add_widget(self.layout)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def load_question(self):
        """ Load the next question in sequence """
        if self.current_question < len(QUESTIONS):
            question, options = QUESTIONS[self.current_question]
            self.question_label.text = question
            
            # Clear previous options
            self.answer_layout.clear_widgets()
            
            for option in options:
                btn = Button(text=option, size_hint=(0.8, None), height=60,
                             pos_hint={'center_x': 0.5}, background_color=[0.3, 0.5, 0.7, 1],
                             color=[1, 1, 1, 1], bold=True)
                btn.bind(on_press=self.save_response)
                self.answer_layout.add_widget(btn)
        else:
            self.go_to_start_analysis()
    
    def save_response(self, instance):
        """ Save the selected answer and move to the next question """
        self.responses.append(instance.text)
        self.current_question += 1
        self.load_question()
    
    def go_to_start_analysis(self):
        """ After the last question, navigate to Start Analysis Screen """
        print("User responses:", self.responses)  # Debugging, store responses in DB later
        self.app.root.current = "start_analysis"