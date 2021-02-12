from django_mri.analysis.visualizers.segmentation import SegmentationVisualizer


class ReconAllVisualizer(SegmentationVisualizer):
    def visualize(self, run) -> None:
        pass
        # grey_matter = run.get_output("modulated_grey_matter")
        # white_matter = run.get_output("modulated_white_matter")
        # super().visualize(grey_matter=grey_matter, white_matter=white_matter)
