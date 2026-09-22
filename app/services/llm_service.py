import os
import time
import json
from dotenv import load_dotenv
from google import genai
from app.agent.prompts import (EXTRACTION_PROMPT, RESPONSE_PROMPT)

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file"
            )
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"

    def generate_response(self, prompt):
        response = self._generate_content_with_retry(prompt)
        return response.text.strip()

    def extract_requirements(self, conversation):
        prompt = f"""
    {EXTRACTION_PROMPT}
    Conversation:
    {conversation}
    """
        response = self._generate_content_with_retry(prompt)
        text = response.text.strip()
        print("\nRaw Gemini Response:")
        print(text)
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(
                f"Gemini returned invalid JSON:\n{text}"
            )
        return data

    def generate_agent_response(
        self,
        conversation,
        customer_data,
        missing_fields
    ):
        prompt = RESPONSE_PROMPT.format(
            conversation=conversation,
            customer_data=customer_data,
            missing_fields=missing_fields
        )
        response = self._generate_content_with_retry(prompt)

        return response.text.strip()

    def _generate_content_with_retry(self, prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response
            except Exception as e:
                error_text = str(e)
                if "503" in error_text or "UNAVAILABLE" in error_text:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(
                            f"\nGemini temporarily unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )
                        time.sleep(wait_time)
                        continue
                    raise
                elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    raise RuntimeError(
                        "Gemini API quota exhausted. "
                        "Please use another API key/model or wait for quota reset."
                    )
                else:
                    raise