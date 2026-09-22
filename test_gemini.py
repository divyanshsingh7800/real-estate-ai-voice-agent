from app.services.llm_service import LLMService

llm = LLMService()

response = llm.generate_response(
    "Say hello in one short sentence."
)

print("Gemini Response:")
print(response)