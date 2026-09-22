from app.agent.memory import ConversationMemory


memory = ConversationMemory()


# First customer message
memory.add_message(
    "user",
    "Mujhe Lucknow mein 2 BHK flat chahiye."
)


# Extracted information
memory.update_customer_data({
    "location": "Lucknow",
    "property_type": "Apartment",
    "bhk": "2 BHK"
})


print("Customer Data:")
print(memory.get_customer_data())


print("\nMissing Information:")
print(memory.get_missing_fields())


print("\nConversation:")
print(memory.get_messages())