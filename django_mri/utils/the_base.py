from enum import Enum


NAME_TO_LOC = {
    "dMRI_MB4_6dirs_d15D45_PA": {
        "data_type": "dwi",
        "pe_dir": "PA",
        "modality": "dwi",
    },
    "dMRI_MB4_6dirs_d15D45_PA_SBRef": {
        "data_type": "fmap",
        "pe_dir": "PA",
        "acq": "dwi",
        "modality": "epi",
    },
    "dMRI_MB4_185dirs_d15D45_AP": {
        "data_type": "dwi",
        "pe_dir": "AP",
        "modality": "dwi",
    },
    "dMRI_MB4_185dirs_d15D45_AP_SBRef": {
        "data_type": "fmap",
        "pe_dir": "AP",
        "acq": "dwi",
        "modality": "epi",
    },
    "T2w_SPC_RL": {"data_type": "anat", "modality": "T2w",},
    "T1w_MPRAGE_RL": {"data_type": "anat", "modality": "T1w",},
    "t2_tirm_tra_dark_fluid_FLAIR": {
        "data_type": "anat",
        "modality": "FLAIR",
    },
    "rsfMRI_AP": {"data_type": "func", "task": "rest", "modality": "bold",},
    "rsfMRI_AP_SBRef": {
        "data_type": "func",
        "task": "rest",
        "modality": "sbref",
    },
    "SpinEchoFieldMap_PA": {
        "data_type": "fmap",
        "pe_dir": "PA",
        "acq": "func",
        "modality": "epi",
    },
    "SpinEchoFieldMap_AP": {
        "data_type": "fmap",
        "pe_dir": "AP",
        "acq": "func",
        "modality": "epi",
    },
    "localizer_3D_2": {"data_type": "anat", "modality": "localizer"},
}


def get_modality_and_data_type(scan, header, acq) -> dict:
    """
    Extracts relevant parameters for BIDS-compatible naming, specifically for TheBase4Ever scans.

    Parameters
    ----------
    scan : [django_mri.models.Scan instance]
        [A Scan instance containing information regarding the acquisition of the image]

    Returns
    -------
    [dict]
        [A dictionary containing relevant for proper naming of the scan]
    """
    data = NAME_TO_LOC.get(scan.description.split(" ")[0].replace("-", "_"))
    if data:
        if ("anat" in data.get("data_type")) and (
            "T1w" in data.get("modality") or "T2w" in data.get("modality")
        ):
            image_type = header["ImageType"]
            if "NORM" in image_type:
                data["acq"] = f"{acq}corrected"
            else:
                data["acq"] = f"{acq}uncorrected"
        else:
            if "acq" in data.keys():
                data["acq"] = f"{acq}{data.get('acq')}"
            else:
                data["acq"] = acq
    else:
        return None
    return data
