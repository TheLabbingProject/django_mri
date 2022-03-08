from typing import Dict, List

from django_mri.analysis.atlas.deskian_killiany import DESIKAN_KILLIANY
from django_mri.analysis.atlas.destrieux import DESTRIEUX
from django_mri.analysis.atlas.dkt import DKT

ATLAS_DEFINITIONS: List[Dict] = [DESIKAN_KILLIANY, DESTRIEUX, DKT]
