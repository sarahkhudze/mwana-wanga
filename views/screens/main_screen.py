from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from datetime import datetime, timedelta
from constants import TRANSLATIONS
from views.components.ai_chatbot import AIChatbot
from models.advice_model import PregnancyAdvice


# Translations
UI_TRANSLATIONS = {
    "en": {
        "title": "Mwana Wanga",
        "date_hint": "Enter Last Menstrual Period (YYYY-MM-DD)",
        "chat_button": "Chat with AI",
        "predict_button": "Predict Due Date",
        "hospitals_button": "Find Nearby Hospitals",
        "symptom_hint": "Enter symptom...",
        "chat_title": "AI Pregnancy Chat",
        "close_button": "Close",
        "get_advice_button": "Get Symptom Advice"
    },
    "ny": {
        "title": "Localized Title",
        "date_hint": "Localized Hint",
        "chat_button": "Localized Chat Button",
        "predict_button": "Localized Predict",
        "hospitals_button": "Localized Hospitals",
        "symptom_hint": "Localized Symptom Hint",
        "chat_title": "Localized Chat Title",
        "close_button": "Localized Close",
        "get_advice_button": "Localized Advice Button"
    }
}

class MainScreen(Screen):
    def __init__(self, auth_service, ai_service, location_service, update_language_callback, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = auth_service
        self.ai_service = ai_service
        self.location_service = location_service
        self.update_language_callback = update_language_callback
        self.current_week = None
        self.chatbot = None
        self.language = "en"  # Default language

        self.build_ui(self.language)

    def build_ui(self, language):
        self.language = language
        t = UI_TRANSLATIONS.get(language, UI_TRANSLATIONS["en"])
        self.clear_widgets()

        # Title
        self.add_widget(MDLabel(
            text=t["title"],
            halign="center",
            pos_hint={"center_y": 0.95},
            font_style="H5"
        ))

        # Date Input
        self.date_input = MDTextField(
            hint_text=t["date_hint"],
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            size_hint_x=0.8
        )
        self.add_widget(self.date_input)

        # Predict Button
        predict_button = MDRaisedButton(
            text=t["predict_button"],
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            on_release=self.predict_date,
            md_bg_color=(0.3, 0.5, 0.8, 1)
        )
        self.add_widget(predict_button)

        # Symptom Input
        self.symptom_input = MDTextField(
            hint_text=t["symptom_hint"],
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint_x=0.8
        )
        self.add_widget(self.symptom_input)

        # Get Advice Button
        get_advice_button = MDRaisedButton(
            text=t["get_advice_button"],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.get_symptom_advice,
            md_bg_color=(0.9, 0.6, 0.2, 1)
        )
        self.add_widget(get_advice_button)

        # Show Hospitals Button
        hospital_button = MDRaisedButton(
            text=t["hospitals_button"],
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.show_hospitals,
            md_bg_color=(0.8, 0.2, 0.3, 1)
        )
        self.add_widget(hospital_button)

        # Chatbot Button
        chat_button = MDRaisedButton(
            text=t["chat_button"],
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_release=self.show_chatbot,
            md_bg_color=(0.2, 0.7, 0.5, 1)
        )
        self.add_widget(chat_button)

        # Result Label
        self.result_label = MDLabel(
            text="",
            halign="center",
            pos_hint={"center_y": 0.15},
            font_style="Body1"
        )
        self.add_widget(self.result_label)

    def update_language(self, language):
        self.language = language
        self.build_ui(language)

    def show_chatbot(self, instance):
        if not self.chatbot:
            self.chatbot = AIChatbot(
                self.ai_service,
                language=self.language
            )
            if hasattr(self, 'current_week'):
                self.chatbot.current_week = self.current_week

        t = UI_TRANSLATIONS.get(self.language, UI_TRANSLATIONS["en"])

        dialog = MDDialog(
            title=t["chat_title"],
            type="custom",
            content_cls=self.chatbot,
            size_hint=(0.9, 0.8),
            buttons=[
                MDFlatButton(
                    text=t["close_button"],
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def predict_date(self, instance):
        t = TRANSLATIONS[self.language]
        try:
            lmp_date = datetime.strptime(self.date_input.text, "%Y-%m-%d")
            due_date = lmp_date + timedelta(days=280)
            self.current_week = (datetime.today() - lmp_date).days // 7

            if self.current_week < 0:
                self.result_label.text = t["future_date"]
            elif self.current_week > 40:
                self.result_label.text = t["congrats"]
            else:
                tip = PregnancyAdvice.get_weekly_advice(self.current_week, self.language)
                self.result_label.text = (
                    f"{t['due_date']} {due_date.strftime('%Y-%m-%d')}\n"
                    f"{t['week_advice'].format(self.current_week)} {tip}"
                )
        except ValueError:
            self.result_label.text = t["invalid_date"]

    def get_symptom_advice(self, instance):
        #symptom = self.symptom_input.text.strip().lower()
        symptom = self.symptom_input.text.strip().title()

        if symptom:
            advice = PregnancyAdvice.get_symptom_advice(symptom, self.language)
            print(f"Advice returned: {advice}")  # Debug print
            if advice:
                self.advice_dialog = MDDialog(
                    title="Symptom Advice",
                    text=advice,
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=lambda x: self.advice_dialog.dismiss()
                        )
                    ]
                )
                self.advice_dialog.open()
            else:
                print("No advice found for the given symptom.")

    def show_hospitals(self, instance):
        from views.components.hospital_dialog import HospitalDialog
        dialog = HospitalDialog(self.location_service, self.language)
        dialog.show_dialog()

