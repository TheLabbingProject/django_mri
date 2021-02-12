import numpy as np
from scipy import stats

#: CAT12 segmentation analysis title used to query the execution node.
CAT12_SEGMENTATION_TITLE = "CAT12 Segmentation"

#: CAT12 segmentation configuration used to query the execution node.
CAT12_SEGMENTATION_CONFIGURATION = {
    "cobra": True,
    "lpba40": True,
    "hammers": True,
    "native_pve": True,
    "warped_image": True,
    "dartel_grey_matter": True,
    "native_grey_matter": True,
    "neuromorphometrics": True,
    "surface_estimation": True,
    "dartel_white_matter": True,
    "native_white_matter": True,
    "jacobian_determinant": True,
    "modulated_grey_matter": True,
    "modulated_white_matter": True,
}


def get_cat12_segmentation_node():
    """
    Returns the default CAT12 segmentation node.

    Returns
    -------
    Node
        Default CAT12 segmentation
    """
    from django_analyses.models.pipeline.node import Node

    return Node.objects.get_or_create(
        analysis_version__analysis__title=CAT12_SEGMENTATION_TITLE,
        configuration=CAT12_SEGMENTATION_CONFIGURATION,
    )[0]


def freedman_diaconis(data) -> int:
    """
    Use Freedman Diaconis rule to compute optimal number of histogram bins.


    Parameters
    ----------
    data: np.ndarray
        One-dimensional array.
    """

    data = np.asarray(data, dtype=np.float_)
    IQR = stats.iqr(data, rng=(25, 75), scale=1.0, nan_policy="omit")
    N = data.size
    bw = (2 * IQR) / np.power(N, 1 / 3)
    datmin, datmax = data.min(), data.max()
    datrng = datmax - datmin
    return int((datrng / bw) + 1)
