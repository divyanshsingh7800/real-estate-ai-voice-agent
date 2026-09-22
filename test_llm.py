from app.services.llm_service import LLMService


llm = LLMService()


response = llm.generate_response(
    "Explain in one sentence what a real estate AI agent does."
)


print("\nGemini Response:")
print(response)