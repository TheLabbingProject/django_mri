from django_mri.analysis.atlas.definitions import ATLAS_DEFINITIONS
from django_mri.models.atlas import Atlas


def load_atlases():
    return Atlas.objects.from_list(ATLAS_DEFINITIONS)
