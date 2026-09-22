from app.services.llm_service import LLMService


llm = LLMService()


conversation = """
Customer: Mujhe Lucknow mein 2 BHK flat chahiye.
Customer: Mera budget 60 lakh tak hai.
"""


requirements = llm.extract_requirements(conversation)


print("Extracted Requirements:")
print(requirements)