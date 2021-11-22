from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from skimage.exposure import match_histograms

from django_mri.analysis.utils import get_mni


class IntensityCorrection:
    STEPS = "saturate_extremes", "stretch_histogram"

    def saturate_extremes(
        self,
        image: np.ndarray,
        lowest_percentile: float = 1,
        highest_percentile: float = 99,
    ) -> np.ndarray:
        """
        Saturates values below *lowest* or above *highest* in the given *image*.

        Parameters
        ----------
        image : np.ndarray
            N-dimensional image to saturate
        lowest_percentile : float, optional
            Bottom saturations percentile, by default 1
        highest_percentile : float, optional
            Top saturation percentile, by default 99

        Returns
        -------
        np.ndarray
            Image with transformed values
        """

        bottom_value = np.percentile(image, lowest_percentile)
        top_value = np.percentile(image, highest_percentile)
        result = np.where(image < bottom_value, bottom_value, image)
        return np.where(result > top_value, top_value, result)

    def stretch_histogram(
        self,
        image: np.ndarray,
        lowest_value: float = -(2 ** 15),
        highest_value: float = 2 ** 15 - 1,
        gamma: float = 1,
    ):
        """
        Spreads the values of the image between the specified *lowest_value* and
        *highest_value*.

        Parameters
        ----------
        image : np.ndarray
            Image to be manipulated
        lowest_value : float, optional
            New lowest value, by default -(2 ** 15)
        highest_value : float, optional
            New highest value, by default 2**15-1
        gamma : float, optional
            Changes the value-mapping curve, by default 1 (linear)

        Returns
        -------
        np.ndarray
            Image with transformed values
        """

        current_min, current_max = image.min(), image.max()
        return (((image - current_min) / (current_max - current_min)) ** gamma) * (
            highest_value - lowest_value
        ) + lowest_value

    def prepare_reference(self) -> np.ndarray:
        mni = get_mni().get_data()
        reference = self.saturate_extremes(mni)
        return self.stretch_histogram(reference)

    def match_histogram(self, image: np.ndarray) -> np.ndarray:
        reference = self.prepare_reference()
        return match_histograms(image, reference)

    def run(self, image: np.ndarray) -> np.ndarray:
        image = self.saturate_extremes(image)
        image = self.stretch_histogram(image)
        image = self.match_histogram(image)
        image = (image - image.min()) / 50
        return image

    def show(
        self, image: np.ndarray, corrected: np.ndarray = None, layer: int = 50,
    ) -> None:
        if corrected is None:
            corrected = self.run(image)
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))
        origin = ax1.imshow(image[:, :, layer], cmap="bone")
        fig.colorbar(origin, ax=ax1)
        ax1.set_title("Raw")
        mni = get_mni().get_data()
        reference = ax2.imshow(mni[:, :, layer], cmap="bone")
        fig.colorbar(reference, ax=ax2)
        ax2.set_title("MNI")
        result = ax3.imshow(corrected[:, :, layer], cmap="bone")
        fig.colorbar(result, ax=ax3)
        ax3.set_title("Corrected")
        plt.tight_layout()
        plt.show()
