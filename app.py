import sys
from os.path import dirname, join
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.fitimage import FitImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from datetime import datetime

# Add the views directory to Python path
sys.path.append(join(dirname(__file__), 'views'))

# Import services and main screen
from views.screens.main_screen import MainScreen as AppMainScreen
from services.auth_service import AuthService
from services.ai_service import AIService
from services.location_service import LocationService


class LoginScreen(Screen):
    def __init__(self, auth_service, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"
        self.language = "en"
        self.auth_service = auth_service
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.back_button = MDFlatButton(
            text="Back",
            on_release=self.go_back,
            pos_hint={"x": 0}
        )

        self.username = MDTextField(
            hint_text="Username",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )

        self.password = MDTextField(
            hint_text="Password",
            mode="rectangle",
            password=True,
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )

        login_text = "Login" if self.language == "en" else "Lowetsa"
        self.login_btn = MDRaisedButton(
            text=login_text,
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            on_release=self.attempt_login
        )

        layout.add_widget(self.back_button)
        title_text = "Login" if self.language == "en" else "Lowetsa"
        #layout.add_widget(MDLabel(text=title_text, halign="center", font_style="H4"))
        self.title_label = MDLabel(text="Login", halign="center", font_style="H4")
        layout.add_widget(self.title_label)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "welcome"

    def attempt_login(self, instance):
        success, message = self.auth_service.login_user(
            self.username.text.strip(),
            self.password.text.strip()
        )

        if success:
            self.manager.current = "main"
        else:
            error_title = "Login Error" if self.language == "en" else "Vuto la kulowa"
            ok_text = "OK" if self.language == "en" else "Zikomo"

            self.dialog = MDDialog(
                title=error_title,
                text=message,
                buttons=[
                    MDFlatButton(
                        text=ok_text,
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()

    def update_language(self, language):
        self.language = language
        login_text = "Login" if language == "en" else "Lowetsa"
        self.login_btn.text = login_text

        title_text = "Login" if language == "en" else "Lowetsa"
        if hasattr(self, 'title_label'):
            self.title_label.text = title_text


class RegisterScreen(Screen):
    def __init__(self, auth_service, **kwargs):
        super().__init__(**kwargs)
        self.name = "register"
        self.language = "en"
        self.auth_service = auth_service
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.back_button = MDFlatButton(
            text="Back",
            on_release=self.go_back,
            pos_hint={"x": 0}
        )

        self.username = MDTextField(
            hint_text="Username",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )

        self.email = MDTextField(
            hint_text="Email",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )

        self.password = MDTextField(
            hint_text="Password",
            mode="rectangle",
            password=True,
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )

        self.confirm_password = MDTextField(
            hint_text="Confirm Password",
            mode="rectangle",
            password=True,
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )

        register_text = "Register" if self.language == "en" else "Lembetsa"
        self.register_btn = MDRaisedButton(
            text=register_text,
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            on_release=self.attempt_register
        )

        layout.add_widget(self.back_button)
        title_text = "Register" if self.language == "en" else "Lembetsa"
        #layout.add_widget(MDLabel(text=title_text, halign="center", font_style="H4"))
        self.title_label = MDLabel(text="Register", halign="center", font_style="H4")
        layout.add_widget(self.title_label)
        layout.add_widget(self.username)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(self.confirm_password)
        layout.add_widget(self.register_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "welcome"

    def attempt_register(self, instance):
        if self.password.text != self.confirm_password.text:
            error_message = "Passwords don't match" if self.language == "en" else "Mawu achinsinsi sakugwirizana"
            self.show_error_dialog(error_message)
            return

        if len(self.password.text) < 6:
            error_message = "Password must be at least 6 characters" if self.language == "en" else "Mawu achinsinsi ayenera kukhala osachepera 6"
            self.show_error_dialog(error_message)
            return

        if "@" not in self.email.text or "." not in self.email.text:
            error_message = "Please enter a valid email" if self.language == "en" else "Chonde lowetsa imelo yoyenera"
            self.show_error_dialog(error_message)
            return

        success, message = self.auth_service.register_user(
            self.username.text.strip(),
            self.password.text.strip(),
            self.email.text.strip()
        )

        if success:
            success_message = "Registration successful! Please login" if self.language == "en" else "Kulembetsa kwabwino! Chonde lowani"
            self.show_success_dialog(success_message)
            self.manager.current = "login"
        else:
            self.show_error_dialog(message)

    def show_error_dialog(self, message):
        error_title = "Registration Error" if self.language == "en" else "Vuto la kulembetsa"
        ok_text = "OK" if self.language == "en" else "Zikomo"

        self.dialog = MDDialog(
            title=error_title,
            text=message,
            buttons=[
                MDFlatButton(
                    text=ok_text,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def show_success_dialog(self, message):
        success_title = "Success" if self.language == "en" else "Zabwino"
        ok_text = "OK" if self.language == "en" else "Zikomo"

        self.dialog = MDDialog(
            title=success_title,
            text=message,
            buttons=[
                MDFlatButton(
                    text=ok_text,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()



    def update_language(self, language):
        self.language = language
        register_text = "Register" if language == "en" else "Lembetsani"
        self.register_btn.text = register_text

        title_text = "Register" if language == "en" else "Lembetsani"
        if hasattr(self, 'title_label'):
            self.title_label.text = title_text


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "welcome"
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 50, 10, 10])

        self.logo_image = FitImage(
            source="assets/images/logo.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5}
        )

        self.title_label = MDLabel(
            text="Welcome to Pregnancy Assistant",
            halign="center",
            font_style="H4"
        )

        self.language_button = MDRaisedButton(
            text="Select Language",
            pos_hint={"center_x": 0.5},
            on_release=self.open_language_menu
        )

        self.login_button = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5},
            on_release=self.login_action
        )

        self.register_button = MDRaisedButton(
            text="Register",
            pos_hint={"center_x": 0.5},
            on_release=self.register_action
        )

        layout.add_widget(self.logo_image)
        layout.add_widget(self.title_label)
        layout.add_widget(self.language_button)
        layout.add_widget(self.login_button)
        layout.add_widget(self.register_button)
        self.add_widget(layout)

        self.menu = None

    def open_language_menu(self, instance):
        menu_items = [
            {"text": "English", "viewclass": "OneLineListItem", "on_release": lambda x="en": self.switch_language(x)},
            {"text": "Chichewa", "viewclass": "OneLineListItem", "on_release": lambda x="ny": self.switch_language(x)},
        ]

        self.menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def switch_language(self, language):
        self.language_button.text = "English" if language == "en" else "Chinyanja"
        self.title_label.text = "Welcome to Pregnancy Assistant" if language == "en" else "Takulandirani ku Nthandizi wa Pakati"
        self.login_button.text = "Login" if language == "en" else "Lowetsa"
        self.register_button.text = "Register" if language == "en" else "Lembetsa"

        if self.manager.has_screen("login"):
            login_screen = self.manager.get_screen("login")
            login_screen.language = language
            login_screen.update_language(language)

        if self.manager.has_screen("register"):
            register_screen = self.manager.get_screen("register")
            register_screen.language = language
            register_screen.update_language(language)

    def login_action(self, instance):
        self.manager.current = "login"

    def register_action(self, instance):
        self.manager.current = "register"


class PregnancyTrackerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()
        self.ai_service = AIService()
        self.location_service = LocationService()
        self.update_language_callback = self.update_all_screens_language

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(auth_service=self.auth_service, name="login"))
        sm.add_widget(RegisterScreen(auth_service=self.auth_service, name="register"))
        sm.add_widget(AppMainScreen(
            auth_service=self.auth_service,
            ai_service=self.ai_service,
            location_service=self.location_service,
            update_language_callback=self.update_language_callback,
            name="main"
        ))
        return sm

    def update_all_screens_language(self, language):
        if self.root.has_screen("welcome"):
            welcome_screen = self.root.get_screen("welcome")
            welcome_screen.switch_language(language)

        if self.root.has_screen("login"):
            login_screen = self.root.get_screen("login")
            login_screen.language = language
            login_screen.update_language(language)

        if self.root.has_screen("register"):
            register_screen = self.root.get_screen("register")
            register_screen.language = language
            register_screen.update_language(language)


if __name__ == "__main__":
    PregnancyTrackerApp().run()