from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from constants import TRANSLATIONS

Builder.load_string('''
<SystemDialogContent>
    orientation: "vertical"
    padding: "20dp"
    spacing: "12dp"

    MDLabel:
        id: dialog_text
        text: ""
        halign: "center"
        font_style: "Body1"
        theme_text_color: "Secondary"

    MDSeparator:
        height: "1dp"
''')


class SystemDialogContent(MDBoxLayout):
    """Custom dialog content with Chichewa/English support"""
    pass


class SystemDialog:
    def __init__(self, language="en"):
        self.language = language
        self.dialog = None

    def show_dialog(self, title, text, buttons=None):
        """Show a system dialog with localized text"""
        t = TRANSLATIONS.get(self.language, {})

        if not buttons:
            buttons = [
                MDFlatButton(
                    text=t.get("ok_button", "OK"),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]

        self.dialog = MDDialog(
            title=t.get(title, title),
            text=t.get(text, text),
            buttons=buttons,
            type="custom",
            content_cls=SystemDialogContent()
        )
        self.dialog.content_cls.ids.dialog_text.text = t.get(text, text)
        self.dialog.open()
        return self.dialog

    def show_error(self, error_code):
        """Show standardized error messages"""
        errors = {
            "gps_error": {
                "en": "Please enable GPS to find nearby hospitals",
                "ny": "Chonde yatsani GPS kuti mupeze zipatala"
            },
            "network_error": {
                "en": "Internet connection required for this feature",
                "ny": "Mukufunika intaneti kuti mugwiritse ntchito izi"
            }
        }

        message = errors.get(error_code, {}).get(self.language, str(error_code))
        self.show_dialog(
            title="error_title",
            text=message
        )