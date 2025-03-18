from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# Import all screens
from screens.loading import LoadingScreen
from screens.welcome import WelcomeScreen
from screens.login import LoginScreen
from screens.forgotpassword import ForgotPasswordScreen
from screens.signup import SignupScreen
from screens.home import HomeScreen
from screens.motivational_stories import MotivationalStoriesScreen
from screens.dear_me import DearMeScreen
from screens.scribblings import ScribblingsScreen 
from screens.emotion_trend import EmotionTrendScreen
from screens.user_profile import UserProfileScreen
from screens.editprofile import EditProfileScreen
from screens.feedback import FeedbackScreen
from screens.letsstart import LetsStartedScreen
from screens.startanalysis import StartAnalysisScreen
from screens.facialview import FacialViewScreen
from screens.voiceview import VoiceViewScreen
from screens.textview import TextViewScreen
from screens.result import ResultScreen
from screens.reco_stress import RecoStressScreen
from screens.reco_anxiety import RecoAnxietyScreen
from screens.reco_depression import RecoDepressionScreen  
from backend import backend 

# Set window size for mobile view
Window.size = (360, 640)

class MindBlissApp(App):
    def build(self):
        # Initialize ScreenManager
        self.sm = ScreenManager()
        self.current_user_email = "" 

        # Initialize the MongoDB collections
        self.users_collection = backend.users  # Access the users collection from the backend
        self.scribblings_collection = backend.scribblings  # Access the scribblings collection from the backend

        # Add all screens to the ScreenManager
        self.sm.add_widget(LoadingScreen(name='loading'))
        self.sm.add_widget(WelcomeScreen(app_instance=self, name='welcome'))  # Pass app_instance
        self.sm.add_widget(LoginScreen(app_instance=self, name='login'))
        self.sm.add_widget(ForgotPasswordScreen(name='forgot_password'))
        self.sm.add_widget(SignupScreen(app_instance=self, name='signup'))
        self.sm.add_widget(HomeScreen(app_instance=self, name='home'))
        self.sm.add_widget(MotivationalStoriesScreen(app_instance=self, name='motivational_stories'))
        self.sm.add_widget(DearMeScreen(app_instance=self, name='dear_me'))  
        self.sm.add_widget(ScribblingsScreen(app_instance=self, name='scribblings'))
        self.sm.add_widget(EmotionTrendScreen(app_instance=self, name='emotion_trend'))
        self.sm.add_widget(UserProfileScreen(app_instance=self, name='user_profile'))
        self.sm.add_widget(EditProfileScreen(app_instance=self, name='editprofile'))
        self.sm.add_widget(FeedbackScreen(app_instance=self, name='feedback'))
        self.sm.add_widget(LetsStartedScreen(app_instance=self, name='letsstart'))
        self.sm.add_widget(StartAnalysisScreen(app_instance=self, name='start_analysis'))
        self.sm.add_widget(FacialViewScreen(app_instance=self, name='facialview'))
        self.sm.add_widget(VoiceViewScreen(app_instance=self, name='voiceview'))
        self.sm.add_widget(TextViewScreen(app_instance=self, name='textview'))
        self.sm.add_widget(ResultScreen(app_instance=self, name='result'))
        self.sm.add_widget(RecoStressScreen(app_instance=self, name='reco_stress'))
        self.sm.add_widget(RecoAnxietyScreen(app_instance=self, name="reco_anxiety"))
        self.sm.add_widget(RecoDepressionScreen(app_instance=self, name="reco_depression"))

        # Initialize user login status
        self.user_id = None  # Store the logged-in user's ID

        return self.sm

    def is_user_logged_in(self):
        """Check if a user is logged in."""
        return self.user_id is not None

    def set_user_credentials(self, username, password):
        """ Store the logged-in user's credentials """
        self.username = username
        self.password = password

if __name__ == '__main__':
    MindBlissApp().run()