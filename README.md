MwanaWanga – AI-Powered Pregnancy Assistant
Overview
MwanaWanga is an open-source AI-powered pregnancy assistant designed to improve maternal healthcare in Malawi. Using AI and Data Science, it provides personalized, multilingual pregnancy guidance via SMS and mobile apps, ensuring accessibility for expectant mothers in both urban and rural areas.

Key Features
✅ Multilingual Support – Provides pregnancy advice in Chichewa and English. ✅ AI-Powered Chatbot – Uses Natural Language Processing (NLP) for interactive pregnancy guidance. ✅ Data-Driven Insights – Applies machine learning to identify high-risk pregnancies. ✅ Mobile Accessibility – Delivers health information via SMS and mobile apps. ✅ Safe Motherhood Alignment – Supports early clinic registration, nutrition guidance, and danger sign recognition.

Technology Stack
Python (Backend)

OpenAI / Mistral AI (AI Chatbot)

Redis (Caching)

TextBlob (Sentiment Analysis)

Flask / FastAPI (API)

GitHub Actions (CI/CD)

Installation & Setup
1️⃣ Clone the Repository
bash
git clone https://github.com/sarahkhudze/mwana-wanga.git
cd mwana-wanga
2️⃣ Set Up Virtual Environment
bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
3️⃣ Install Dependencies
bash
pip install -r requirements.txt
4️⃣ Set Up Environment Variables
Create a .env file and add:

MISTRAL_API_KEY=your_api_key_here
REDIS_URL=your_redis_url_here
5️⃣ Run the Application
bash
python app.py
Usage
Ask pregnancy-related questions via the AI chatbot.

Receive medically accurate guidance in local languages.

Access maternal health insights via SMS or mobile apps.

Contributing
We welcome contributions! 

Fork the repository

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m "Added new feature")

Push to GitHub (git push origin feature-name)

Submit a pull request

License
This project is licensed under the MIT License – see the LICENSE file for details.

Contact & Support
📧 Email: [info@solutionsincmw.com] 🌍 Website: www.solutionsincmw.com] 📌 GitHub Issues: Report a bug

🚀 Join us in transforming maternal healthcare in Malawi
