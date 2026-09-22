from app.agent.agent import RealEstateAgent


agent = RealEstateAgent()


print("Real Estate AI Agent")
print("--------------------")
print("Type 'exit' to stop.\n")


while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":
        break

    result = agent.process_message(
        user_message
    )

    print("AI:", result["response"])

    print(
        "\nCurrent Customer Data:",
        result["customer_data"]
    )

    print(
        "Missing Fields:",
        result["missing_fields"]
    )

    print()
