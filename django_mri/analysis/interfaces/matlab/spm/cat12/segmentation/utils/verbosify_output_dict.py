"""
A utility module created for the definition of the
:meth:`verbosify_output_dict` method.
"""

from pathlib import Path

ROI_ATLAS_MAPS = "neuromorphometrics", "lpba40", "cobra", "hammers"


def _verbose_surface_estimation(output_dict: dict) -> dict:
    if output_dict.get("surface_estimation"):
        surface_estimation = output_dict["surface_estimation"]
        return {
            "left_hemisphere_central_surface": surface_estimation[0],
            "left_hemisphere_spherical_surface": surface_estimation[1],
            "left_hemisphere_spherical_registered_surface": surface_estimation[
                2
            ],
            "left_hemisphere_cortical_thickness": surface_estimation[3],
            "right_hemisphere_central_surface": surface_estimation[4],
            "right_hemisphere_spherical_surface": surface_estimation[5],
            "right_hemisphere_spherical_registered_surface": surface_estimation[  # noqa: E501
                6
            ],
            "right_hemisphere_cortical_thickness": surface_estimation[7],
        }
    return {}


def _verbosify_label_files(output_dict: dict) -> dict:
    label_files = [
        output_dict.get(atlas_map)
        for atlas_map in ROI_ATLAS_MAPS
        if output_dict.get(atlas_map)
    ]
    if any(label_files):
        return {
            "labels_mat": label_files[0][0],
            "labels_xml": label_files[0][1],
        }
    return {}


def _verbosify_deformation_fields(output_dict: dict) -> dict:
    value = output_dict.get("deformation_fields")
    if isinstance(value, Path):
        if value.name.startswith("y"):
            return {"forward_deformation_field": value}
        elif value.name.startswith("iy"):
            return {"inverse_deformation_field": value}
    elif isinstance(value, list):
        return {
            "forward_deformation_field": value[0],
            "inverse_deformation_field": value[1],
        }
    return {}


def _verbosify_reports(reports: list) -> dict:
    return {
        "report_mat": reports[0],
        "report_xml": reports[1],
        "report_txt": reports[2],
        "report_pdf": reports[3],
        "report_jpg": reports[4],
    }


def verbosify_output_dict(output_dict: dict) -> dict:
    """
    Flattens and verbosifies the output files dictionary to facilitate
    integration with django_analyses.

    Parameters
    ----------
    output_dict : dict
        Output files by key

    Returns
    -------
    dict
        Flat and verbose output files by key
    """

    result = _verbose_surface_estimation(output_dict)
    result.update(_verbosify_label_files(output_dict))
    result.update(_verbosify_deformation_fields(output_dict))
    result.update(_verbosify_reports(output_dict["reports"]))
    result.update(
        {
            key: value
            for key, value in output_dict.items()
            if isinstance(value, Path)
        }
    )
    return result
