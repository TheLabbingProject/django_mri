from django.test import TestCase
from django_mri.models.choices import ScanningSequence, SequenceVariant
from django_mri.models.sequence_type import SequenceType


TEST_SEQUENCE = {
    "title": "TEST",
    "scanning_sequence": [ScanningSequence.GR.name, ScanningSequence.RM.name],
    "sequence_variant": [
        SequenceVariant.SK.name,
        SequenceVariant.SP.name,
        SequenceVariant.MP.name,
    ],
}


class SequenceTypeModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        SequenceType.objects.create(**TEST_SEQUENCE)

    def setUp(self):
        self.sequence_type = SequenceType.objects.first()

    ########
    # Meta #
    ########

    def test_unique_together(self):
        result = SequenceType._meta.unique_together
        expected = (("scanning_sequence", "sequence_variant"),)
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

    # scanning_sequence
    def test_scanning_sequence_blank_and_null(self):
        field = SequenceType._meta.get_field("scanning_sequence")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_scanning_sequence_size(self):
        field = SequenceType._meta.get_field("scanning_sequence")
        self.assertEqual(field.size, 5)

    def test_scanning_sequence_base_max_length(self):
        field = SequenceType._meta.get_field("scanning_sequence")
        self.assertEqual(field.base_field.max_length, 2)

    def test_scanning_sequence_choices(self):
        field = SequenceType._meta.get_field("scanning_sequence")
        result = field.base_field.choices
        expected = ScanningSequence.choices()
        self.assertTupleEqual(result, expected)

    # sequence_variant
    def test_sequence_variant_blank_and_null(self):
        field = SequenceType._meta.get_field("sequence_variant")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_sequence_variant_base_max_length(self):
        field = SequenceType._meta.get_field("sequence_variant")
        self.assertEqual(field.base_field.max_length, 4)

    def test_sequence_variant_choices(self):
        field = SequenceType._meta.get_field("sequence_variant")
        result = field.base_field.choices
        expected = SequenceVariant.choices()
        self.assertTupleEqual(result, expected)

    ###########
    # Methods #
    ###########

    def test_get_string(self):
        result = str(self.sequence_type)
        expected = TEST_SEQUENCE["title"]
        self.assertEqual(result, expected)

    ####################
    # Common Sequences #
    ####################

    def test_common_sequences_load(self):
        from django_mri.models.common_sequences import sequences

        objects = [SequenceType(**sequence) for sequence in sequences]
        SequenceType.objects.bulk_create(objects)
