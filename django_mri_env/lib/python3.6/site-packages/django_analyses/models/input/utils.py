from django_analyses.utils import ChoiceEnum


class ListElementTypes(ChoiceEnum):
    STR = "String"
    INT = "Integer"
    FLT = "Float"
    BLN = "Boolean"


TYPES_DICT = {
    ListElementTypes.STR: str,
    ListElementTypes.INT: int,
    ListElementTypes.FLT: float,
    ListElementTypes.BLN: bool,
}
