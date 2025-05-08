from kivymd.uix.screen import Screen
from kivymd.uix.floatlayout import MDFloatLayout
from views.components.auth.login import LoginTab
from views.components.auth.register import RegisterTab
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.tab import MDTabs


class AuthScreen(Screen):
    def __init__(self, auth_service, on_success, language="en", **kwargs):
        super().__init__(**kwargs)
        self.auth_service = auth_service
        self.on_success = on_success
        self.language = language
        self.build_ui()

    def build_ui(self):
        self.tabs = MDTabs()

        self.login_tab = LoginTab(
            auth_service=self.auth_service,
            on_success=self.on_success,
            language=self.language,
            title="Login"  # Title for the tab
        )
        self.tabs.add_widget(self.login_tab)

        self.register_tab = RegisterTab(
            auth_service=self.auth_service,
            on_success=self.on_success,
            language=self.language,
            title="Register"  # Title for the tab
        )
        self.tabs.add_widget(self.register_tab)

        self.add_widget(self.tabs)
