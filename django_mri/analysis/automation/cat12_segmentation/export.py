"""
Export CAT12 segmentation results as an xarray dataset.
"""
from typing import Dict, List

import dask.array as da
import nibabel as nib
import pandas as pd
import xarray as xr
from django.db.models import QuerySet

from django_mri.analysis.automation.cat12_segmentation.utils import (
    get_node, get_run_set, read_nifti)

OUTPUT_KEYS = "modulated_grey_matter", "modulated_white_matter", "warped_image"
OUTPUT_DIMS = "Run ID", "x", "y", "z"


def get_coords(runs: QuerySet) -> Dict[str, List[int]]:
    run_ids = list(runs.values_list("id", flat=True))
    return {"Run ID": run_ids}


def create_output_array(runs: QuerySet, key: str) -> da:
    paths = (run.get_output(key) for run in runs)
    arrays = (da.from_array(read_nifti(path)) for path in paths)
    all_data = da.stack(arrays)
    coords = get_coords(runs)
    return xr.DataArray(all_data, coords=coords, dims=OUTPUT_DIMS, name=key)


INFO_COLUMNS = (
    "Subject ID",
    "Session ID",
    "Scan ID",
    "Scan Description",
    "Acquisition Time",
)


def extract_run_info(runs: QuerySet) -> pd.DataFrame:
    from django_mri.models.scan import Scan

    info = {}
    for run in runs:
        input_path = run.get_input("path")
        scan = Scan.objects.get(_nifti__path=input_path)
        run_info = {
            "Subject ID": scan.session.subject.id,
            "Session ID": scan.session.id,
            "Scan ID": scan.id,
            "Scan Description": scan.description,
            "Acquisition Time": scan.time.strftime("%Y-%m-%d"),
        }
        info[run.id] = run_info
    return pd.DataFrame.from_dict(info, orient="index")


def export_cat_results(runs: QuerySet = None) -> xr.Dataset:
    runs = runs or get_run_set()
    info_df = extract_run_info(runs)
    ds = xr.Dataset.from_dataframe(info_df)
    ds = ds.rename({"index": "Run ID"})

    affine = nib.load(runs[0].get_output(OUTPUT_KEYS[0])).affine
    node = get_node()
    str_configuration = {
        key: str(value) for key, value in node.configuration.items()
    }
    configuration = list(str_configuration.items())
    attrs = {
        "configuration": configuration,
        "affine": affine,
    }
    ds = ds.assign_attrs(attrs)

    data_vars = {key: create_output_array(runs, key) for key in OUTPUT_KEYS}
    return ds.assign(data_vars)
