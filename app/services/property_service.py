import json
from pathlib import Path

class PropertyService:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        file_path = base_dir / "data" / "properties.json"

        with open(file_path, "r", encoding="utf-8") as file:
            self.properties = json.load(file)

    def search_properties(
            self,
            location = None,
            bhk = None,
            property_type = None,
            budget_max = None
    ):
        results = []
        for property_data in self.properties:
            if location:
                if property_data['location'].lower() != location.lower():
                    continue

            if property_type:
                if property_data['property_type'].lower() != property_type.lower():
                    continue

                if bhk:
                    bhk_values = []
                    if isinstance(bhk, int):
                        bhk_values = [bhk]

                    elif isinstance(bhk, str):
                        for value in bhk.replace("or", ",").split(","):
                            value = value.strip()
                            if value.isdigit():
                                bhk_values.append(int(value))

                    if bhk_values:
                        if property_data['bhk'] not in bhk_values:
                            continue

                if budget_max:
                    if property_data['price'] > budget_max:
                        continue
                results.append(property_data)

        return results
