import re
from app.agent.memory import ConversationMemory
from app.services.property_service import PropertyService
from app.database.database import save_leads


def extract_phone_number(text):
    """
    Extract a valid Indian 10-digit phone number.
    """

    digits = "".join(char for char in text if char.isdigit())

    # Direct 10 digit number
    if len(digits) == 10 and digits[0] in "6789":
        return digits

    # +91 / 91 followed by 10 digits
    if len(digits) == 12 and digits.startswith("91"):
        phone = digits[2:]

        if phone[0] in "6789":
            return phone

    return None

class RealEstateAgent:

    def __init__(self):
        self.memory = ConversationMemory()
        self.property_service = PropertyService()
        self.lead_saved = False

    def extract_requirements(self, message):

        text = message.lower().strip()
        data = {}

        # -------------------------
        # LOCATION
        # -------------------------

        locations = [
            "lucknow",
            "kanpur",
            "varanasi",
            "delhi",
            "noida"
        ]

        for location in locations:

            if location in text:
                data["location"] = location.title()
                break

        # -------------------------
        # PROPERTY TYPE
        # -------------------------

        if "flat" in text or "apartment" in text:
            data["property_type"] = "Apartment"

        elif "villa" in text:
            data["property_type"] = "Villa"

        elif "plot" in text:
            data["property_type"] = "Plot"

        # -------------------------
        # BHK
        # -------------------------

        bhk_match = re.search(
            r"(\d+)\s*(?:bhk|b\s*h\s*k)",
            text
        )

        if bhk_match:
            data["bhk"] = int(
                bhk_match.group(1)
            )

        # -------------------------
        # BUDGET
        #
        # IMPORTANT:
        # Only values containing lakh/lac/crore/cr
        # are treated as budget.
        #
        # "7"       -> NOT budget
        # "60 lakh" -> 60,00,000
        # "1 crore" -> 1,00,00,000
        # -------------------------

        budget_match = re.search(
            r"(\d+(?:\.\d+)?)\s*"
            r"(lakh|lakhs|lac|lacs|crore|crores|cr)\b",
            text
        )

        if budget_match:

            amount = float(
                budget_match.group(1)
            )

            unit = budget_match.group(2)

            if unit in [
                "lakh",
                "lakhs",
                "lac",
                "lacs"
            ]:
                data["budget_max"] = int(
                    amount * 100000
                )

            elif unit in [
                "crore",
                "crores",
                "cr"
            ]:
                data["budget_max"] = int(
                    amount * 10000000
                )

        # -------------------------
        # TIMELINE
        # -------------------------

        if (
            "month" in text
            or "months" in text
            or "manth" in text
            or "mahine" in text
            or "mahina" in text
        ):

            data["timeline"] = message.strip()

        elif (
            "year" in text
            or "years" in text
            or "saal" in text
        ):

            data["timeline"] = message.strip()

        elif (
            "immediately" in text
            or "immediate" in text
            or "jaldi" in text
        ):

            data["timeline"] = message.strip()

        # -------------------------
        # PURPOSE
        # -------------------------

        if (
            "self use" in text
            or "self-use" in text
            or "self use ke liye" in text
            or "self-use ke liye" in text
            or "selfie use" in text
            or "selfie uske" in text
            or "selfish" in text
            or "khud ke liye" in text
            or "rehne ke liye" in text
            or "rehna hai" in text
        ):
            data["purpose"] = "Self Use"

        elif (
            "investment" in text
            or "invest" in text
            or "investment ke liye" in text
        ):

            data["purpose"] = "Investment"


        if (
            "mera naam" in text
            or "my name is" in text
            or "i am" in text
        ):

            name = re.sub(
                r"(mera naam|my name is|i am)",
                "",
                message,
                flags=re.IGNORECASE
            ).strip()

            # Remove optional "hai"
            name = re.sub(
                r"\bhai\b",
                "",
                name,
                flags=re.IGNORECASE
            ).strip()

            if name:
                data["name"] = name

        # -------------------------
        # PHONE
        # -------------------------

        phone = extract_phone_number(
            message
        )

        if phone:
            data["phone"] = phone

        return data

    def search_properties(self):

        customer = (
            self.memory.get_customer_data()
        )

        results = (
            self.property_service.search_properties(
                location=customer.get("location"),
                bhk=customer.get("bhk"),
                property_type=customer.get(
                    "property_type"
                ),
                budget_max=customer.get(
                    "budget_max"
                )
            )
        )

        return results

    def calculate_score(self):

        customer = (
            self.memory.get_customer_data()
        )

        # 100-point lead qualification score
        score = 0

        # Property requirement
        if customer.get("location"):
            score += 20

        if customer.get("bhk"):
            score += 15

        if customer.get("budget_max"):
            score += 20

        # Buying intent
        if customer.get("timeline"):
            score += 20

        if customer.get("purpose"):
            score += 10

        # Contact information
        if customer.get("phone"):
            score += 15

        return score

    def save_lead(
        self,
        selected_property=None
    ):

        customer = (
            self.memory.get_customer_data()
        )

        score = self.calculate_score()

        requirements = str({
            "location": customer.get(
                "location"
            ),
            "property_type": customer.get(
                "property_type"
            ),
            "bhk": (
                f"{customer.get('bhk')} BHK"
                if customer.get("bhk")
                else None
            ),
            "budget_min": customer.get(
                "budget_min"
            ),
            "budget_max": customer.get(
                "budget_max"
            ),
            "timeline": customer.get(
                "timeline"
            ),
            "purpose": customer.get(
                "purpose"
            ),
            "selected_property": selected_property
        })

        budget_max = customer.get(
            "budget_max"
        )

        if budget_max:

            budget_text = (
                f"₹{budget_max // 100000} lakh"
            )

        else:

            budget_text = "not specified"

        summary = (
            f"Customer {customer.get('name')} "
            f"is looking for a "
            f"{customer.get('bhk')} BHK "
            f"{customer.get('property_type')} "
            f"in {customer.get('location')}. "
            f"Maximum budget is "
            f"{budget_text}. "
            f"Purchase timeline is "
            f"{customer.get('timeline')}. "
            f"Purpose is "
            f"{customer.get('purpose')}."
        )

        if selected_property:

            summary += (
                f" Selected property: "
                f"{selected_property}."
            )

        lead_data = {

            "name": customer.get(
                "name"
            ),

            "phone": customer.get(
                "phone"
            ),

            "location": customer.get(
                "location"
            ),

            "property_type": customer.get(
                "property_type"
            ),

            "bhk": (
                f"{customer.get('bhk')} BHK"
                if customer.get("bhk")
                else None
            ),

            "budget_min": customer.get(
                "budget_min"
            ),

            "budget_max": customer.get(
                "budget_max"
            ),

            "timeline": customer.get(
                "timeline"
            ),

            "purpose": customer.get(
                "purpose"
            ),

            "requirements": requirements,

            "recommended_properties": (
                selected_property
                if selected_property
                else ""
            ),

            "conversation_summary": summary,

            "qualification_score": score
        }

        lead_id = save_leads(
            lead_data
        )

        self.lead_saved = True

        return lead_id

    def get_lead_info(self):
        customer = self.memory.get_customer_data()

        budget_max = customer.get("budget_max")

        if budget_max:
            budget_text = f"₹{budget_max // 100000} lakh"
        else:
            budget_text = "not specified"

        summary = (
            f"Customer {customer.get('name') or 'Customer'} "
            f"is looking for a "
            f"{customer.get('bhk') or 'unspecified'} BHK "
            f"{customer.get('property_type') or 'property'} "
            f"in {customer.get('location') or 'an unspecified location'}. "
            f"Maximum budget is {budget_text}. "
            f"Purchase timeline is "
            f"{customer.get('timeline') or 'not specified'}. "
            f"Purpose is "
            f"{customer.get('purpose') or 'not specified'}."
        )

        if customer.get("selected_property"):
            summary += (
                f" Selected property: "
                f"{customer.get('selected_property')}."
            )

        return {
            "lead_score": self.calculate_score(),
            "conversation_summary": summary
        }

    def process_message(
        self,
        message
    ):

        message = message.strip()

        if not message:

            return {
                "response": (
                    "Sorry, mujhe aapki "
                    "baat samajh nahi aayi."
                ),
                "customer_data": (
                    self.memory.get_customer_data()
                ),
                "lead_id": None,
                **self.get_lead_info()
            }

        # -------------------------
        # SAVE USER MESSAGE
        # -------------------------

        self.memory.add_message(
            "user",
            message
        )

        # -------------------------
        # EXTRACT DATA
        # -------------------------

        extracted_data = (
            self.extract_requirements(
                message
            )
        )

        self.memory.update_customer_data(
            extracted_data
        )

        customer = (
            self.memory.get_customer_data()
        )

        message_lower = message.lower()

        # -------------------------
        # AFTER LEAD SAVED
        # -------------------------

        if self.lead_saved:

            response = (
                "Thank you! "
                "Our team will contact "
                "you shortly."
            )

            self.memory.add_message(
                "assistant",
                response
            )

            return {
                "response": response,
                "customer_data": customer,
                "lead_id": None,
                **self.get_lead_info()
            }

        # -------------------------
        # CHECK IF PROPERTY
        # ALREADY SELECTED
        # -------------------------

        selected_property = (
            customer.get(
                "selected_property"
            )
        )

        # -------------------------
        # PROPERTY ALREADY SELECTED
        # -------------------------

        if selected_property:

            # -------------------------
            # CAPTURE NAME
            # -------------------------

            if not customer.get("name"):

                clean_message = (
                    message.strip()
                )

                lower_message = (
                    clean_message.lower()
                )

                ignored_words = {
                    "yes",
                    "haan",
                    "han",
                    "ha",
                    "interested",
                    "interest",
                    "okay",
                    "ok",
                    "theek hai",
                    "thik hai"
                }

                invalid_name_words = [
                    "lakh",
                    "lakhs",
                    "lac",
                    "lacs",
                    "crore",
                    "crores",
                    "budget",
                    "bhk",
                    "month",
                    "months",
                    "mahine",
                    "mahina",
                    "year",
                    "years",
                    "saal"
                ]

                looks_like_name = (

                    1
                    <= len(
                        clean_message.split()
                    )
                    <= 4

                    and len(
                        clean_message
                    ) >= 2

                    and lower_message not in (
                        ignored_words
                    )

                    and not any(
                        char.isdigit()
                        for char in clean_message
                    )

                    and not any(
                        word in lower_message
                        for word in (
                            invalid_name_words
                        )
                    )
                )

                if looks_like_name:

                    customer["name"] = (
                        clean_message
                    )

                else:

                    response = (
                        "Great choice. "
                        "Aapka naam bata denge?"
                    )

                    self.memory.add_message(
                        "assistant",
                        response
                    )

                    return {
                        "response": response,
                        "customer_data": customer,
                        "lead_id": None
                    }

            # -------------------------
            # ASK PHONE
            # -------------------------

            if not customer.get("phone"):

                response = (
                    f"Thank you {customer.get('name')}. "
                    "Aapka phone number share kar denge?"
                )

                self.memory.add_message(
                    "assistant",
                    response
                )

                return {
                    "response": response,
                    "customer_data": customer,
                    "lead_id": None
                }

            # -------------------------
            # SAVE LEAD
            # -------------------------

            lead_id = self.save_lead(
                selected_property
            )

            response = (
                f"Thank you "
                f"{customer.get('name')}. "
                "Aapki details successfully "
                "note kar li hain. "
                "Hamari team aapse jaldi "
                "contact karegi."
            )

            self.memory.add_message(
                "assistant",
                response
            )

            return {
                "response": response,
                "customer_data": customer,
                "lead_id": lead_id,
                **self.get_lead_info()
            }

        # -------------------------
        # CHECK REQUIRED FIELDS
        # -------------------------

        missing_fields = (
            self.memory.get_missing_fields()
        )

        if missing_fields:

            field = missing_fields[0]

            if field == "location":

                response = (
                    "Aapko kis location mein "
                    "property chahiye?"
                )

            elif field == "bhk":

                response = (
                    "Aapko kitne BHK ki "
                    "property chahiye?"
                )

            elif field == "budget_max":

                response = (
                    "Aapka maximum budget "
                    "kitna hai?"
                )

            elif field == "timeline":

                response = (
                    "Aap property kab tak "
                    "purchase karna chahte hain?"
                )

            elif field == "purpose":

                response = (
                    "Property aap self-use "
                    "ke liye le rahe hain ya "
                    "investment ke liye?"
                )

            self.memory.add_message(
                "assistant",
                response
            )

            return {
                "response": response,
                "customer_data": customer,
                "lead_id": None,
                **self.get_lead_info()
            }

        # -------------------------
        # PROPERTY SEARCH
        # -------------------------

        properties = (
            self.search_properties()
        )

        # -------------------------
        # CHECK PROPERTY SELECTION
        # -------------------------

        # User exact property name bolta hai
        #
        # Example:
        # "Sunrise Enclave"
        # -------------------------

        for property_data in properties:

            property_name = (
                property_data["name"].lower()
            )

            if property_name in message_lower:

                selected_property = (
                    property_data["name"]
                )

                customer[
                    "selected_property"
                ] = selected_property

                break

        # -------------------------
        # USER SAYS INTERESTED
        # -------------------------

        if (
            not selected_property
            and properties
            and (
                re.search(
                    r"\binterested\b",
                    message_lower
                )
                or re.search(
                    r"\binterest\b",
                    message_lower
                )
                or re.search(
                    r"\bhaan\b",
                    message_lower
                )
                or re.search(
                    r"\bhan\b",
                    message_lower
                )
                or re.search(
                    r"\byes\b",
                    message_lower
                )
                or re.search(
                    r"\bha\b",
                    message_lower
                )
            )
        ):

            selected_property = (
                properties[0]["name"]
            )

            customer[
                "selected_property"
            ] = selected_property

        # -------------------------
        # PROPERTY NOT SELECTED
        # -------------------------

        if not selected_property:

            if properties:

                property_data = (
                    properties[0]
                )

                response = (
                    "Aapki requirement ke "
                    "according mujhe ye "
                    "property mili hai. "

                    f"{property_data['name']}, "

                    f"{property_data['bhk']} BHK, "

                    f"₹{property_data['price'] // 100000} lakh. "

                    "Kya aap is property mein "
                    "interested hain?"
                )

            else:

                response = (
                    "Aapki requirement ke "
                    "according abhi mujhe "
                    "suitable property nahi mili. "

                    "Kya aap apna budget ya "
                    "location thoda flexible "
                    "kar sakte hain?"
                )

            self.memory.add_message(
                "assistant",
                response
            )

            return {
                "response": response,
                "customer_data": customer,
                "lead_id": None,
                **self.get_lead_info()
            }

        # -------------------------
        # PROPERTY SELECTED
        #
        # This handles the moment
        # user says "haan".
        # -------------------------

        if selected_property:

            # -------------------------
            # ASK NAME
            # -------------------------

            if not customer.get("name"):

                response = (
                    "Great choice. "
                    "Aapka naam bata denge?"
                )

                self.memory.add_message(
                    "assistant",
                    response
                )

                return {
                    "response": response,
                    "customer_data": customer,
                    "lead_id": None
                }

            # -------------------------
            # ASK PHONE
            # -------------------------

            if not customer.get("phone"):

                response = (
                    f"Thank you "
                    f"{customer.get('name')}. "
                    "Aapka phone number "
                    "share kar denge?"
                )

                self.memory.add_message(
                    "assistant",
                    response
                )

                return {
                    "response": response,
                    "customer_data": customer,
                    "lead_id": None
                }

            # -------------------------
            # SAVE LEAD
            # -------------------------

            lead_id = self.save_lead(
                selected_property
            )

            response = (
                f"Thank you "
                f"{customer.get('name')}. "
                "Aapki details successfully "
                "note kar li hain. "
                "Hamari team aapse jaldi "
                "contact karegi."
            )

            self.memory.add_message(
                "assistant",
                response
            )

            return {
                "response": response,
                "customer_data": customer,
                "lead_id": lead_id,
                **self.get_lead_info()
            }