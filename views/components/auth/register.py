from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

class RegisterTab(MDBoxLayout, MDTabsBase):
    def __init__(self, auth_service, on_success, **kwargs):
        self.language = kwargs.pop('language', 'en')  # default to English
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '20dp'
        self.padding = '40dp'
        self.auth_service = auth_service
        self.on_success = on_success
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        labels = {
            'en': {
                'title': "Create Account",
                'username': "Username",
                'email': "Email",
                'password': "Password",
                'confirm_password': "Confirm Password",
                'register': "Register",
                'have_account': "Already have an account?",
                'password_mismatch': "Passwords do not match",
                'account_created': "Account created!",
                'error_title': "Error",
                'success_title': "Success"
            },
            'ny': {  # Chichewa language
                'title': "Sangani Akaunti",
                'username': "Dzina logwiritsa ntchito",
                'email': "Imelo",
                'password': "Chinsinsi",
                'confirm_password': "Tsimikizani chinsinsi",
                'register': "Sungitsani",
                'have_account': "Ndili ndi akaunti kale",
                'password_mismatch': "Zinsinsi sizikugwirizana",
                'account_created': "Akaunti yapangidwa!",
                'error_title': "Vuto linali",
                'success_title': "Zikomo!"
            }
        }

        lang = labels.get(self.language, labels['en'])

        # Save for use in other methods
        self.lang = lang

        # Header
        self.add_widget(MDLabel(
            text=lang['title'],
            halign="center",
            font_style="H4",
            pos_hint={"center_x": 0.5, "top": 0.9}
        ))

        # Registration Form
        self.username = MDTextField(
            hint_text=lang['username'],
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            size_hint_x=0.8
        )
        self.email = MDTextField(
            hint_text=lang['email'],
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            size_hint_x=0.8
        )
        self.password = MDTextField(
            hint_text=lang['password'],
            password=True,
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            size_hint_x=0.8
        )
        self.confirm_password = MDTextField(
            hint_text=lang['confirm_password'],
            password=True,
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            size_hint_x=0.8
        )

        self.add_widget(self.username)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(self.confirm_password)

        # Register Button
        self.add_widget(MDRaisedButton(
            text=lang['register'],
            pos_hint={"center_x": 0.5, "center_y": 0.25},
            on_release=self.attempt_register,
            md_bg_color=(0.3, 0.7, 0.3, 1)  # Green accent
        ))

        # Login Link
        self.add_widget(MDFlatButton(
            text=lang['have_account'],
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            on_release=self.switch_to_login
        ))

    def attempt_register(self, instance):
        # Validate inputs
        if self.password.text != self.confirm_password.text:
            self.show_error(self.lang['password_mismatch'])
            return

        success, message = self.auth_service.register_user(
            self.username.text.strip(),
            self.password.text.strip(),
            self.email.text.strip()
        )

        if success:
            self.show_success(self.lang['account_created'])
            Clock.schedule_once(lambda dt: self.on_success(), 1.5)
        else:
            self.show_error(message)

    def show_error(self, message):
        dialog = MDDialog(
            title=self.lang['error_title'],
            text=message,
            buttons=[MDFlatButton(text="Okay", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def show_success(self, message):
        dialog = MDDialog(
            title=self.lang['success_title'],
            text=message,
            buttons=[]
        )
        dialog.open()
        Clock.schedule_once(lambda dt: dialog.dismiss(), 1.5)

    def switch_to_login(self, instance):
        # Safely switch screens if manager exists
        if self.parent and hasattr(self.parent, 'manager'):
            self.parent.manager.current = 'login'
