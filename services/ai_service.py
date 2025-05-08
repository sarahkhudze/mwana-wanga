import os
import redis
import requests
from dotenv import load_dotenv
from textblob import TextBlob
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
print(api_key)

if not api_key:
    raise ValueError("Error: Missing Mistral API key. Please set MISTRAL_API_KEY in your .env file.")


class AIService:
    def __init__(self, model="mistral-small-latest"):
        self.api_key = api_key
        self.model = model
        self.online = bool(self.api_key)

        try:
            self.cache = redis.StrictRedis(host='localhost', port=6379, db=0)
            self.cache.ping()
        except redis.ConnectionError:
            self.cache = None

        self.client = MistralClient(api_key=self.api_key)

    def get_ai_response(self, prompt, language="en", week=None):
        if not self.online:
            return "Error: No API key or internet connection."

        try:
            if self.cache:
                cached_response = self.cache.get(prompt)
                if cached_response:
                    return cached_response.decode('utf-8')

            context = f"\n\nContext: Week {week} of pregnancy" if week else ""
            system_prompt = self._create_system_prompt(language)

            sentiment = self._analyze_sentiment(prompt)
            if sentiment < -0.3:
                system_prompt += "\n\nBe extra empathetic, as the user might be feeling distressed."

            health_advice = self._fetch_pregnancy_advice()

            response = self.client.chat(
                model=self.model,
                messages=[
                    ChatMessage(role="system", content=system_prompt),
                    ChatMessage(role="user", content=prompt + context + "\n\nAdditional Advice:\n" + health_advice)
                ]
            )

            reply = response.choices[0].message.content

            if self.cache:
                self.cache.set(prompt, reply, ex=86400)

            return reply

        except Exception as e:
            print(f"AI Service Error: {str(e)}")
            return "Error: Failed to generate response. (API issue)"

    def _create_system_prompt(self, language):
        base_prompt = """You are a helpful pregnancy advisor for women in Malawi. 
        Provide accurate, medically-sound information in a caring, empathetic tone. 
        Always recommend consulting with a healthcare professional for serious concerns."""

        language_prompts = {
            "ny": "Perekani mayankho m'Chichewa.",
            "fr": "Donnez des réponses en français.",
            "zh": "请提供中文回答。",
            "en": "Provide responses in English."
        }
        return base_prompt + "\n\n" + language_prompts.get(language, "Provide responses in English.")

    def _analyze_sentiment(self, text):
        return TextBlob(text).sentiment.polarity

    def _fetch_pregnancy_advice(self):
        url = "https://health.gov/myhealthfinder/api/v3/topicsearch.json?categoryId=18"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if "Result" in data and "Resources" in data["Result"]:
                return "\n".join(
                    f"{item['Title']}: {item['AccessibleVersion'][:200]}..."
                    for item in data["Result"]["Resources"]["Resource"]
                )
            return "No additional advice found."
        except Exception as e:
            print(f"Health API Error: {str(e)}")
            return ""
