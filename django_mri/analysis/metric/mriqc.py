MRIQC_METRICS = [
    {
        "title": "cjv",
        "description": "Coefficient of joint variation (CJV): The cjv of GM and WM was proposed as objective function by [Ganzetti2016] for the optimization of INU correction algorithms. Higher values are related to the presence of heavy head motion and large INU artifacts. Lower values are better.",
    },
    {
        "title": "cnr",
        "description": "Contrast-to-noise ratio (CNR): The cnr [Magnota2006], is an extension of the SNR calculation to evaluate how separated the tissue distributions of GM and WM are. Higher values indicate better quality.",
    },
    {"title": "snr", "description": "Signal-to-noise ratio."},
    {"title": "snr_csf", "description": "CSF-masked signal-to-noise ratio."},
    {
        "title": "snr_gm",
        "description": "Grey matter-masked signal-to-noise ratio.",
    },
    {
        "title": "snr_wm",
        "description": "White matter-masked signal-to-noise ratio.",
    },
    {"title": "snr_total", "description": "Total signal-to-noise ratio."},
    {
        "title": "snrd_csf",
        "description": "CSF-masked Dietrich's signal-to-noise ratio.",
    },
    {
        "title": "snrd_gm",
        "description": "Grey matter-masked Dietrich's signal-to-noise ratio.",
    },
    {
        "title": "snrd_wm",
        "description": "White matter-masked Dietrich's signal-to-noise ratio.",
    },
    {
        "title": "snrd_total",
        "description": "Total Dietrich's signal-to-noise ratio.",
    },
    {
        "title": "qi_1",
        "description": "Detect artifacts in the image using the method described in [Mortamet2009]. The QI1 is the proportion of voxels with intensity corrupted by artifacts normalized by the number of voxels in the background. Lower values are better.",
    },
    {
        "title": "qi_2",
        "description": "Mortamet’s quality index 2 (QI2) is a calculation of the goodness-of-fit of a χ2 distribution on the air mask, once the artifactual intensities detected for computing the QI1 index have been removed [Mortamet2009]. Lower values are better.",
    },
    {
        "title": "efc",
        "description": "The EFC [Atkinson1997] uses the Shannon entropy of voxel intensities as an indication of ghosting and blurring induced by head motion. Lower values are better. The original equation is normalized by the maximum entropy, so that the EFC can be compared across images with different dimensions.",
    },
    {
        "title": "fber",
        "description": "The FBER [Shehzad2015], defined as the mean energy of image values within the head relative to outside the head [QAP-measures]. Higher values are better.",
    },
    {
        "title": "inu_med",
        "description": "Median INU field (bias field) as extracted by the N4ITK algorithm [Tustison2010]. Values closer to 1.0 are better, values further from zero indicate greater RF field inhomogeneity.",
    },
    {
        "title": "inu_range",
        "description": "INU field (bias field) range as extracted by the N4ITK algorithm [Tustison2010]. Values closer to 1.0 are better, values further from zero indicate greater RF field inhomogeneity.",
    },
    {
        "title": "wm2max",
        "description": "The white-matter to maximum intensity ratio is the median intensity within the WM mask over the 95% percentile of the full intensity distribution, that captures the existence of long tails due to hyper-intensity of the carotid vessels and fat. Values should be around the interval [0.6, 0.8].",
    },
    {
        "title": "fwhm_avg",
        "description": "The FWHM of the spatial distribution of the image intensity values in units of voxels [Forman1995]. Lower values are better, higher values indicate a blurrier image. Uses the gaussian width estimator filter implemented in AFNI’s 3dFWHMx.",
    },
    {
        "title": "fwhm_x",
        "description": "The FWHM of the spatial distribution of the image intensity values in units of voxels [Forman1995]. Lower values are better, higher values indicate a blurrier image. Uses the gaussian width estimator filter implemented in AFNI’s 3dFWHMx.",
    },
    {
        "title": "fwhm_y",
        "description": "The FWHM of the spatial distribution of the image intensity values in units of voxels [Forman1995]. Lower values are better, higher values indicate a blurrier image. Uses the gaussian width estimator filter implemented in AFNI’s 3dFWHMx.",
    },
    {
        "title": "fwhm_z",
        "description": "The FWHM of the spatial distribution of the image intensity values in units of voxels [Forman1995]. Lower values are better, higher values indicate a blurrier image. Uses the gaussian width estimator filter implemented in AFNI’s 3dFWHMx.",
    },
    {
        "title": "icvs_csf",
        "description": "The ICV fractions of CSF (should move within a normative range).",
    },
    {
        "title": "icvs_gm",
        "description": "The ICV fractions of grey matter (should move within a normative range).",
    },
    {
        "title": "icvs_wm",
        "description": "The ICV fractions of white matter (should move within a normative range).",
    },
    {
        "title": "rpve_wm",
        "description": "The rPVe of white matter. Lower values are better.",
    },
    {
        "title": "rpve_gm",
        "description": "The rPVe of grey matter. Lower values are better.",
    },
    {
        "title": "rpve_csf",
        "description": "The rPVe of CSF. Lower values are better.",
    },
    {"title": "summary_bg_k", "description": "Background summary values."},
    {"title": "summary_bg_mad", "description": "Background summary values."},
    {"title": "summary_bg_mean", "description": "Background summary values."},
    {
        "title": "summary_bg_median",
        "description": "Background summary values.",
    },
    {"title": "summary_bg_n", "description": "Background summary values."},
    {"title": "summary_bg_p05", "description": "Background summary values."},
    {"title": "summary_bg_p95", "description": "Background summary values."},
    {"title": "summary_bg_stdv", "description": "Background summary values."},
    {"title": "summary_fg_k", "description": "Foreground summary values."},
    {"title": "summary_fg_mad", "description": "Foreground summary values."},
    {"title": "summary_fg_mean", "description": "Foreground summary values."},
    {
        "title": "summary_fg_median",
        "description": "Foreground summary values.",
    },
    {"title": "summary_fg_n", "description": "Foreground summary values."},
    {"title": "summary_fg_p05", "description": "Foreground summary values."},
    {"title": "summary_fg_p95", "description": "Foreground summary values."},
    {"title": "summary_fg_stdv", "description": "Foreground summary values."},
    {"title": "summary_csf_k", "description": "CSF summary values."},
    {"title": "summary_csf_mad", "description": "CSF summary values."},
    {"title": "summary_csf_mean", "description": "CSF summary values."},
    {"title": "summary_csf_median", "description": "CSF summary values.",},
    {"title": "summary_csf_n", "description": "CSF summary values."},
    {"title": "summary_csf_p05", "description": "CSF summary values."},
    {"title": "summary_csf_p95", "description": "CSF summary values."},
    {"title": "summary_csf_stdv", "description": "CSF summary values."},
    {"title": "summary_gm_k", "description": "Grey matter summary values."},
    {"title": "summary_gm_mad", "description": "Grey matter summary values."},
    {"title": "summary_gm_mean", "description": "Grey matter summary values."},
    {
        "title": "summary_gm_median",
        "description": "Grey matter summary values.",
    },
    {"title": "summary_gm_n", "description": "Grey matter summary values."},
    {"title": "summary_gm_p05", "description": "Grey matter summary values."},
    {"title": "summary_gm_p95", "description": "Grey matter summary values."},
    {"title": "summary_gm_stdv", "description": "Grey matter summary values."},
    {"title": "summary_wm_k", "description": "White matter summary values."},
    {"title": "summary_wm_mad", "description": "White matter summary values."},
    {
        "title": "summary_wm_mean",
        "description": "White matter summary values.",
    },
    {
        "title": "summary_wm_median",
        "description": "Grey matter summary values.",
    },
    {"title": "summary_wm_n", "description": "White matter summary values."},
    {"title": "summary_wm_p05", "description": "White matter summary values."},
    {"title": "summary_wm_p95", "description": "White matter summary values."},
    {
        "title": "summary_wm_stdv",
        "description": "White matter summary values.",
    },
    {
        "title": "tpm_overlap_csf",
        "description": "The overlap of the TPMs estimated from the image and the corresponding maps from the ICBM nonlinear-asymmetric 2009c template. Higher values are better.",
    },
    {
        "title": "tpm_overlap_gm",
        "description": "The overlap of the TPMs estimated from the image and the corresponding maps from the ICBM nonlinear-asymmetric 2009c template. Higher values are better.",
    },
    {
        "title": "tpm_overlap_wm",
        "description": "The overlap of the TPMs estimated from the image and the corresponding maps from the ICBM nonlinear-asymmetric 2009c template. Higher values are better.",
    },
    {
        "title": "aor",
        "description": "Mean fraction of outliers per fMRI volume as given by AFNI’s 3dToutcount.",
    },
    {
        "title": "aqi",
        "description": "Mean quality index as computed by AFNI’s 3dTqual; for each volume, it is one minus the Spearman’s (rank) correlation of that volume with the median volume. Lower values are better.",
    },
    {
        "title": "dvars_nstd",
        "description": "D referring to temporal derivative of timecourses, VARS referring to RMS variance over voxels ([Power2012] dvars_nstd) indexes the rate of change of BOLD signal across the entire brain at each frame of data. DVARS is calculated with nipype after motion correction.",
    },
    {
        "title": "dvars_std",
        "description": "D referring to temporal derivative of timecourses, VARS referring to RMS variance over voxels ([Power2012] dvars_nstd) indexes the rate of change of BOLD signal across the entire brain at each frame of data. DVARS is calculated with nipype after motion correction.",
    },
    {
        "title": "dvars_vstd",
        "description": "D referring to temporal derivative of timecourses, VARS referring to RMS variance over voxels ([Power2012] dvars_nstd) indexes the rate of change of BOLD signal across the entire brain at each frame of data. DVARS is calculated with nipype after motion correction.",
    },
    {"title": "fd_mean", "description": "Average framewise displacement.",},
    {
        "title": "fd_num",
        "description": "Number of timepoints above FD threshold.",
    },
    {
        "title": "fd_perc",
        "description": "Percent of FDs above the FD threshold.",
    },
    {
        "title": "gcor",
        "description": "Global Correlation: calculates an optimized summary of time-series correlation as in [Saad2013] using AFNI’s @compute_gcor.",
    },
    {"title": "gsr_x", "description": "Ghost to Signal Ratio.",},
    {"title": "gsr_y", "description": "Ghost to Signal Ratio.",},
    {
        "title": "tsnr",
        "description": "Temporal SNR: a simplified interpretation of the tSNR definition [Kruger2001].",
    },
    {
        "title": "dummy_trs",
        "description": "A number of volumes in the begining of the fMRI timeseries identified as non-steady state.",
    },
    {"title": "spacing_x", "description": "X-axis spatial resolution."},
    {"title": "spacing_y", "description": "Y-axis spatial resolution."},
    {"title": "spacing_z", "description": "Z-axis spatial resolution."},
    {"title": "spacing_tr", "description": "Time resolution."},
    {"title": "size_x", "description": "X dimension size."},
    {"title": "size_y", "description": "Y dimension size."},
    {"title": "size_z", "description": "Z dimension size."},
    {"title": "size_t", "description": "Time dimension size."},
]

# flake8: noqa: E501
