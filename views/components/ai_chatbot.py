from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineListItem, MDList
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp



class AIChatbot(MDBoxLayout):
    def __init__(self, ai_service, language="en", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(10)
        self.padding = dp(10)
        self.ai_service = ai_service
        self.language = language
        self.chat_history = []

        # Chat history display - Improved scrolling
        self.scroll_view = ScrollView(
            bar_width=dp(4),
            bar_color=(0.5, 0.5, 0.5, 0.5)
        )
        self.chat_list = MDList(
            spacing=dp(5),
            padding=dp(5)
        )
        self.scroll_view.add_widget(self.chat_list)
        self.add_widget(self.scroll_view)

        # Input area - Better layout proportions
        self.input_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )
        self.chat_input = MDTextField(
            hint_text="Type your question..." if language == "en" else "Lembani funso lanu...",
            multiline=False,
            size_hint_x=0.8,
            mode="fill",
            #fill_color=(0.95, 0.95, 0.95, 1)
        )
        self.send_button = MDRaisedButton(
            text="Send" if language == "en" else "Tumiza",
            size_hint_x=0.2,
            md_bg_color=(0.2, 0.5, 0.7, 1)  # Slightly darker blue
        )
        self.send_button.bind(on_release=self.send_message)
        self.input_layout.add_widget(self.chat_input)
        self.input_layout.add_widget(self.send_button)
        self.add_widget(self.input_layout)

        self.offline_mode = False



    def send_message(self, instance):
        message = self.chat_input.text.strip()
        if not message:
            return

        # Add user message
        self.add_message(f"You: {message}", is_user=True)
        self.chat_input.text = ""

        if self.offline_mode:
            response = "AI is offline. Please connect to the internet for AI advice."
        else:
            try:
                response = self.ai_service.get_ai_response(
                    message,
                    language=self.language,
                    week=getattr(self, 'current_week', None)
                )
                print("AI Response:", response)  # Debugging
            except Exception as e:
                print("Error:", str(e))  # Debugging
                response = "AI service unavailable. Using offline advice."
                self.offline_mode = True

        self.add_message(f"AI: {response}", is_user=False)

    def add_message(self, text, is_user=False):
        self.chat_history.append((text, is_user))
        self.chat_list.add_widget(
            OneLineListItem(
                text=text,
                bg_color=(0.9, 0.92, 0.98, 1) if is_user else (0.98, 0.96, 0.89, 1),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1)  # Black text for better readability
            )
        )
        # Auto-scroll to bottom
        self.scroll_view.scroll_to(self.chat_list.children[0])

    def set_language(self, language):
        self.language = language
        self.chat_input.hint_text = "Type your question..." if language == "en" else "Lembani funso lanu..."
        self.send_button.text = "Send" if language == "en" else "Tumiza"