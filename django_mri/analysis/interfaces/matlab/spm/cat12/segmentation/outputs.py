"""
Dictionaries containing CAT12 segmentation output file names by key.
"""

#: Output file names by key.
SEGMENTATION_OUTPUT = {
    "surface_estimation": [
        "surf/lh.central.{file_name}.gii",
        "surf/lh.sphere.{file_name}.gii",
        "surf/lh.sphere.reg.{file_name}.gii",
        "surf/lh.thickness.{file_name}",
        "surf/rh.central.{file_name}.gii",
        "surf/rh.sphere.{file_name}.gii",
        "surf/rh.sphere.reg.{file_name}.gii",
        "surf/rh.thickness.{file_name}",
    ],
    "neuromorphometrics": [
        "label/catROI_{file_name}.mat",
        "label/catROI_{file_name}.xml",
    ],
    "lpba40": ["label/catROI_{file_name}.mat", "label/catROI_{file_name}.xml"],
    "cobra": ["label/catROI_{file_name}.mat", "label/catROI_{file_name}.xml"],
    "hammers": [
        "label/catROI_{file_name}.mat",
        "label/catROI_{file_name}.xml",
    ],
    "native_grey_matter": "mri/p1{file_name}.nii",
    "modulated_grey_matter": "mri/mwp1{file_name}.nii",
    "dartel_grey_matter": {
        "rigid": "mri/rp1{file_name}_rigid.nii",
        "affine": "mri/rp1{file_name}_affine.nii",
    },
    "native_white_matter": "mri/p2{file_name}.nii",
    "modulated_white_matter": "mri/mwp2{file_name}.nii",
    "dartel_white_matter": {
        "rigid": "mri/rp2{file_name}_rigid.nii",
        "affine": "mri/rp2{file_name}_affine.nii",
    },
    "native_pve": "mri/p0{file_name}.nii",
    "warped_image": "mri/wm{file_name}.nii",
    "jacobian_determinant": "mri/wj_{file_name}.nii",
    "deformation_fields": {
        "none": None,
        "forward": "mri/y_{file_name}.nii",
        "inverse": "mri/iy_{file_name}.nii",
        "both": ["mri/y_{file_name}.nii", "mri/iy_{file_name}.nii"],
    },
}

#: Artifacts created during execution.
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
