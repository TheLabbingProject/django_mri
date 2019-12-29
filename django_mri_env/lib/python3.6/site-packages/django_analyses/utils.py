from enum import Enum


class ChoiceEnum(Enum):
    """
    A Python `enum <https://docs.python.org/3/library/enum.html>`_ with
    a method to provide choices in the format that Django expects them.

    """

    @classmethod
    def choices(cls):
        """
        Returns a tuple of tuples containing the definition of choices for
        a given Django field. For more information see Django's
        `model field reference <https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices>`_.

        Returns
        -------
        tuple
            Tuples representing actual values next to human-readable values.
        """
        return tuple((choice.name, choice.value) for choice in cls)
