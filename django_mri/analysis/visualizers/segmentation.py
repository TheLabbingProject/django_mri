from pathlib import Path

import matplotlib.pyplot as plt
from nilearn.plotting import plot_stat_map

DIMENSIONS = "x", "y", "z"
N_SLICES = 10


class SegmentationVisualizer:
    def visualize(
        self,
        grey_matter: Path,
        white_matter: Path,
        display: tuple = DIMENSIONS,
        n_slices: int = N_SLICES,
    ) -> None:
        fig, ax = plt.subplots(nrows=len(display))
        for i, dimension in enumerate(display):
            plot_stat_map(
                grey_matter,
                cmap="Reds",
                display_mode=dimension,
                cut_coords=n_slices,
                colorbar=False,
                figure=fig,
                axes=ax[i],
            )
            plot_stat_map(
                white_matter,
                cmap="Blues",
                display_mode=dimension,
                cut_coords=n_slices,
                colorbar=False,
                bg_img=None,
                figure=fig,
                axes=ax[i],
            )
        figure_manager = plt.get_current_fig_manager()
        figure_manager.resize(*figure_manager.window.maxsize())
        plt.show()
