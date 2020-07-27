from django.test import TestCase
from django_mri.models.choices import ScanningSequence, SequenceVariant
from django_mri.models.sequence_type import SequenceType
from django_mri.models.sequence_type_definition import SequenceTypeDefinition
from django_mri.serializers.sequence_type_definition import (
    SequenceTypeDefinitionSerializer,
)
from tests.utils import load_common_sequences


class SequenceTypeModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        load_common_sequences()

    def setUp(self):
        self.sequence_type = SequenceType.objects.get(title="DWI")
        self.definitions = self.sequence_type.sequence_definition_set.all()

    ########
    # Meta #
    ########

    def test_unique_together(self):
        result = SequenceTypeDefinition._meta.unique_together
        expected = (("scanning_sequence", "sequence_variant"),)
        self.assertTupleEqual(result, expected)

    ##########
    # Fields #
    ##########

    # scanning_sequence
    def test_scanning_sequence_blank_and_null(self):
        field = SequenceTypeDefinition._meta.get_field("scanning_sequence")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_scanning_sequence_size(self):
        field = SequenceTypeDefinition._meta.get_field("scanning_sequence")
        self.assertEqual(field.size, 5)

    def test_scanning_sequence_base_max_length(self):
        field = SequenceTypeDefinition._meta.get_field("scanning_sequence")
        self.assertEqual(field.base_field.max_length, 2)

    def test_scanning_sequence_choices(self):
        field = SequenceTypeDefinition._meta.get_field("scanning_sequence")
        result = field.base_field.choices
        expected = ScanningSequence.choices()
        self.assertTupleEqual(result, expected)

    # sequence_variant
    def test_sequence_variant_blank_and_null(self):
        field = SequenceTypeDefinition._meta.get_field("sequence_variant")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_sequence_variant_base_max_length(self):
        field = SequenceTypeDefinition._meta.get_field("sequence_variant")
        self.assertEqual(field.base_field.max_length, 4)

    def test_sequence_variant_choices(self):
        field = SequenceTypeDefinition._meta.get_field("sequence_variant")
        result = field.base_field.choices
        expected = SequenceVariant.choices()
        self.assertTupleEqual(result, expected)

    ###########
    # Methods #
    ###########

    def test_get_string(self):
        result = str(self.definitions[0])
        expected = "Scanning Sequence: ['EP']\nSequence Variant: ['SK', 'SP']"
        self.assertEqual(result, expected)

    def test_create_serializer(self):
        serializer = SequenceTypeDefinitionSerializer()
        definition = {
            "scanning_sequence": ["RM"],
            "sequence_variant": ["None"],
            "sequence_id": self.sequence_type,
        }
        result = serializer.create(definition)
        self.assertIsInstance(result, SequenceTypeDefinition)
