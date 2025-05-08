import os
from dotenv import load_dotenv
from services.ai_service import AIService

# Load environment variables
load_dotenv()


def test_ai():
    print("🔍 Testing Mistral AI Connection...")

    try:
        ai = AIService()
        test_prompt = "What are 3 important nutrients during pregnancy?"

        print(f"\n📩 Sending test prompt: '{test_prompt}'")
        response = ai.get_ai_response(test_prompt, week=12)


        print("\n✅ Received response:")
        print(response[:500] + "..." if len(response) > 500 else response)

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        print("Troubleshooting steps:")
        print("1. Verify .env file exists in project root")
        print("2. Check MISTRAL_API_KEY is set")
        print("3. Run 'pip show mistralai' to confirm version")


if __name__ == "__main__":
    test_ai()