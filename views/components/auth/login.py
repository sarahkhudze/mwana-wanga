from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog


class LoginTab(MDBoxLayout, MDTabsBase):
    def __init__(self, auth_service, on_success, **kwargs):
        self.language = kwargs.pop('language', 'en')
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '20dp'
        self.padding = '40dp'
        self.auth_service = auth_service
        self.on_success = on_success
        self.build_ui()

    def build_ui(self):
        self.username = MDTextField(
            hint_text="Username",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        self.password = MDTextField(
            hint_text="Password",
            password=True,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )

        self.add_widget(self.username)
        self.add_widget(self.password)

        self.add_widget(MDRaisedButton(
            text="Login",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.attempt_login
        ))

    def attempt_login(self, instance):
        success, message = self.auth_service.login_user(
            self.username.text.strip(),
            self.password.text.strip()
        )

        if success:
            self.on_success()
        else:
            MDDialog(
                title="Login Error",
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
            ).open()