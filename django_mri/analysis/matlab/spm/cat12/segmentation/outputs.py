SEGMENTATION_OUTPUT = {
    "surface_estimation": [
        "surf/lh.central.{file_name}.gii",
        "surf/lh.sphere.{file_name}.gii",
        "surf/lh.sphere.reg.{file_name}.gii",
        "surf/lh.thickness.{file_name}.gii",
        "surf/rh.central.{file_name}.gii",
        "surf/rh.sphere.{file_name}.gii",
        "surf/rh.sphere.reg.{file_name}.gii",
        "surf/rh.thickness.{file_name}.gii",
    ],
    "neuromorphometrics": [
        "label/catROI_{file_name}.mat",
        "label/catROI_{file_name}.xml",
    ],
    "lpba40": "{file_name}",
    "cobra": "{file_name}",
    "hammers": "{file_name}",
    "native_grey_matter": "mri/p1{file_name}.nii",
    "modulated_grey_matter": "mri/mwp1{file_name}.nii",
    "dartel_grey_matter": {"rigid": "mri/rp1{file_name}.nii}"},
    "native_white_matter": "mri/p2{file_name}.nii",
    "modulated_white_matter": "mri/mwp2{file_name}.nii",
    "dartel_white_matter": {"rigid": "mri/rp2{file_name}.nii}"},
    "native_pve": "mri/p0{file_name}.nii",
    "warped_image": "mri/wm{file_name}.nii",
    "jacobian_determinant": "mri/wj_{file_name}",
    "deformation_fields": {
        "none": None,
        "forward": "mri/y_{file_name}.nii",
        "inverse": "mri/iy_{file_name}.nii",
        "both": ["mri/y_{file_name}.nii", "iy_{file_name}.nii"],
    },
}

AUXILIARY_OUTPUT = {
    "batch_file": "segmentation.m",
    "reports": [
        "report/cat_{file_name}.mat",
        "report/cat_{file_name}.xml",
        "report/catlog_{file_name}.txt",
        "report/catreport_{file_name}.pdf",
        "report/catreportj_{file_name}.jpg",
    ],
}
