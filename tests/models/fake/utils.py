import pandas as pd

from django.conf import settings


def snake_case_to_camel_case(string: str) -> str:
    return "".join([part.title() for part in string.split("_")])


def read_subject_table() -> pd.DataFrame:
    return pd.read_excel(
        settings.RAW_SUBJECT_TABLE_PATH,
        sheet_name="Subjects",
        header=[0, 1],
        converters={("Raw", "Patient ID"): str},
    )


class CustomAttributesProcessor:
    STRING_TO_TYPE = {
        "String": str,
        "Integer": int,
        "Float": float,
        "Boolean": bool,
        "List": list,
        "Dictionary": dict,
    }

    def __init__(self, custom_attributes: dict):
        self.custom_attributes = custom_attributes

    def get_type_from_string(self, type_string: str):
        try:
            return self.STRING_TO_TYPE[type_string]
        except KeyError:
            invalid_message = f"Invalid type definition: {type_string}!"
            valid_types = list(self.STRING_TO_TYPE.keys())
            types_message = f"Type must be in: {valid_types}"
            raise ValueError(f"{invalid_message}\n{types_message}")

    def validate_definition_fields(self, definition: dict):
        if not ("value" in definition and "type" in definition):
            raise ValueError(
                'Custom attributes must contain "value" and "type" definitions!'
            )

    def validate_definition(self, definition: dict):
        self.validate_definition_fields(definition)
        value_type = self.get_type_from_string(definition["type"])
        if isinstance(definition["value"], value_type):
            return True
        return False

    def validate(self):
        for key, definition in self.custom_attributes.items():
            if not self.validate_definition(definition):
                type_representation = definition["type"].lower()
                raise ValueError(
                    f"Invalid custom attribute value!\n{key} must be of type {type_representation}."
                )
