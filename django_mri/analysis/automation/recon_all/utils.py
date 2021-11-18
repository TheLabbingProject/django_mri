"""
Utility functions for the execution and evaluation of FreeSurfer's ReconAll.
"""
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import \
    InputDefinition
from django_analyses.models.pipeline.node import Node
from django_analyses.models.run import Run

from django_mri.analysis.automation.recon_all import messages
from django_mri.models.scan import Scan

#: ReconAll analysis title.
ANALYSIS_TITLE = "ReconAll"

#: Default ReconAll analysis version.
VERSION_TITLE = "6.0.0"

#: Default ReconAll analysis configuration.
RECON_ALL_CONFIGURATION = {}

T1_FILES_KEY = "T1_files"
"""
ReconAll's input file
:attr:`~django_analyses.models.input.definitions.input_definition.InputDefinition.key`.
"""

#: Index labels used for anatomical statistics results table.
FIXED_STATS_INDEX = [
    "Subject ID",
    "Run ID",
    "Session IDs",
    "T1 Scan IDs",
    "Atlas",
    "Hemisphere",
    "Region Name",
]


def get_recon_all_version(title: str = VERSION_TITLE) -> AnalysisVersion:
    """
    Returns the provided ReconAll version instance.

    Parameters
    ----------
    title : str, optional
        Analysis version title, by default :attr:`VERSION_TITLE`

    Returns
    -------
    AnalysisVersion
        ReconAll analysis version

    Raises
    ------
    AnalysisVersion.DoesNotExist
        No matching ReconAll version found
    """
    if isinstance(title, str):
        return AnalysisVersion.objects.get(
            analysis__title=ANALYSIS_TITLE, title=title
        )
    else:
        version_set = AnalysisVersion.objects.filter(
            analysis__title=ANALYSIS_TITLE
        )
        if version_set:
            return version_set.first()
        else:
            raise AnalysisVersion.DoesNotExist(messages.NO_RECON_ALL_VERSIONS)


def get_node(
    version_title: str = VERSION_TITLE, configuration: dict = None
) -> Node:
    """
    Returns the default ReconAll execution node. If configuration is `None`,
    defaults to :attr:`RECON_ALL_CONFIGURATION`.

    Parameters
    ----------
    version_title : str, optional
        ReconAll version, by default :attr:`VERSION_TITLE`
    configuration : dict, optional
        ReconAll configuration, by default None

    Returns
    -------
    Node
        Default ReconAll execution node
    """
    recon_all_v = get_recon_all_version(version_title)
    configuration = (
        configuration
        if isinstance(configuration, dict)
        else RECON_ALL_CONFIGURATION
    )
    return Node.objects.get_or_create(
        analysis_version=recon_all_v, configuration=configuration
    )[0]


def get_input_definition() -> InputDefinition:
    """
    Query ReconAll's input file definition (*t1_files*) to check for existing
    runs.

    Returns
    -------
    InputDefinition
        ReconAll's *t1_files* input definition
    """
    node = get_node()
    return node.analysis_version.input_definitions.get(key=T1_FILES_KEY)


def plot_region_boxplot(
    all_stats: pd.DataFrame,
    atlas: str = "Destrieux",
    measurement: str = "Surface Area",
) -> None:
    """
    Plots a boxplot of estimated anatomical statistics by hemisphere and
    region.

    Parameters
    ----------
    all_stats : pd.DataFrame
        Anatomical statistics
    atlas : str, optional
        Atlas used to query region names, by default "Destrieux"
    measurement : str, optional
        Anatomical statistic to display, by default "Surface Area"
    """
    atlas_stats = all_stats.xs(atlas, level="Atlas")
    fig, ax = plt.subplots(figsize=(24, 30))
    sns.boxplot(
        data=atlas_stats.reset_index(),
        x=measurement,
        y="Region Name",
        hue="Hemisphere",
        orient="h",
        ax=ax,
    )
    title = f"Estimated {measurement} by {atlas} Region"
    ax.set_title(title)


def get_t1_scans(run_id: int) -> List[Scan]:
    """
    Associate a given run's *t1_files* input instance with the matching
    :class:`~django_mri.models.scan.Scan` instances.

    Parameters
    ----------
    run_id : int
        Run ID

    Returns
    -------
    List[Scan]
        Input scans
    """
    run = Run.objects.get(id=run_id)
    t1_files = run.get_input("T1_files")
    return [
        Scan.objects.get(_nifti__path=nifti_path) for nifti_path in t1_files
    ]


def query_run_info(all_stats: pd.DataFrame) -> pd.DataFrame:
    """
    Fixes the results returned by the :class:`ReconAllResults` class to replace
    the "Subject ID" column with "Run ID" and add information.

    Parameters
    ----------
    all_stats : pd.DataFrame
        ReconAll stats results summary table

    Returns
    -------
    pd.DataFrame
        Fixed ReconAll results summary table
    """

    run_ids = all_stats.index.levels[0].astype(int)
    fixed_df = all_stats.reset_index()
    fixed_df["Run ID"] = fixed_df["Subject ID"].astype(int)
    fixed_df["Session IDs"] = np.nan
    fixed_df["T1 Scan IDs"] = np.nan
    for run_id in run_ids:
        try:
            t1_scans = get_t1_scans(run_id)
        except Exception:
            continue
        else:
            subject = t1_scans[0].session.subject
            run_mask = fixed_df["Subject ID"] == str(run_id)
            scan_ids = ",".join([str(scan.id) for scan in t1_scans])
            session_ids = ",".join(
                set([str(scan.session.id) for scan in t1_scans])
            )
            fixed_df.loc[run_mask, "Session IDs"] = session_ids
            fixed_df.loc[run_mask, "T1 Scan IDs"] = scan_ids
            fixed_df.loc[run_mask, "Subject ID"] = subject.id
    return fixed_df.set_index(FIXED_STATS_INDEX)
