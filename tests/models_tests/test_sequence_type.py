from django.test import TestCase
from django_mri.models.choices import ScanningSequence, SequenceVariant
from django_mri.models.sequence_type import SequenceType
from tests.utils import load_common_sequences


class SequenceTypeModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        load_common_sequences()

    def setUp(self):
        self.sequence_type = SequenceType.objects.get(title="DWI")

    ########
    # Meta #
    ########

    def test_ordering(self):
        result = SequenceType._meta.ordering
        expected = ("title",)
        self.assertTupleEqual(result, expected)

    ##########
    # Fields #
    ##########

    # title
    def test_title_blank_and_null(self):
        field = SequenceType._meta.get_field("title")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_title_uniqueness(self):
        field = SequenceType._meta.get_field("title")
        self.assertFalse(field.unique)

    # description
    def test_description_blank_and_null(self):
        field = SequenceType._meta.get_field("description")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_description_uniqueness(self):
        field = SequenceType._meta.get_field("description")
        self.assertFalse(field.unique)

    ##############
    # Properties #
    ##############

    def test_sequence_definitions(self):
        expected = [
            {"id": 41, "scanning_sequence": ["EP"], "sequence_variant": ["SK", "SP"],}
        ]
        result = self.sequence_type.sequence_definitions
        self.assertIsInstance(result, list)
        self.assertEqual(result, expected)

    ###########
    # Methods #
    ###########

    def test_get_string(self):
        result = str(self.sequence_type)
        expected = "DWI"
        self.assertEqual(result, expected)
