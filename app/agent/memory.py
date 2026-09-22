class ConversationMemory:

    def __init__(self):
        self.messages = []
        self.customer_data = {
            "name": None,
            "phone": None,
            "location": None,
            "property_type": None,
            "bhk": None,
            "budget_min": None,
            "budget_max": None,
            "timeline": None,
            "purpose": None,
            "selected_property": None
        }

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def update_customer_data(self, data):
        for key, value in data.items():
            if value is not None:
                self.customer_data[key] = value

    def get_customer_data(self):
        return self.customer_data

    def get_messages(self):
        return self.messages

    def get_missing_fields(self):
        required_fields = [
            "location",
            "bhk",
            "budget_max",
            "timeline",
            "purpose"
        ]

        missing_fields = []
        for field in required_fields:
            if self.customer_data[field] is None:
                missing_fields.append(field)

        return missing_fields