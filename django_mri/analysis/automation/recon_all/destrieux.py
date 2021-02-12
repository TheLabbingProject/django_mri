import matplotlib.pyplot as plt
import pandas as pd
from nilearn import datasets, plotting
from sklearn.preprocessing import StandardScaler

# Nilearn Destrieux region name with no represenation in FreeSurfer
MEDIAL_WALL = "Medial_wall"


def parse_destrieux_label(label: bytes) -> str:
    return label.decode().replace("_and_", "&")


def calculate_destrieux_mean(stats_df: pd.DataFrame) -> pd.DataFrame:
    try:
        return stats_df.xs("Destrieux", level="Atlas").mean(
            level=["Hemisphere", "Region Name"]
        )
    except KeyError:
        return stats_df.mean(level=["Hemisphere", "Region Name"])


def plot_destrieux_surface(
    stats_df: pd.DataFrame,
    hemisphere: str = "Left",
    measurement: str = "Surface Area",
    scale: bool = True,
    title: str = None,
) -> plt.Figure:
    title = title or f"{measurement} ({hemisphere})"
    destrieux_atlas = datasets.fetch_atlas_surf_destrieux()
    destrieux_labels = [
        parse_destrieux_label(label) for label in destrieux_atlas["labels"][1:]
    ]
    fsaverage = datasets.fetch_surf_fsaverage()
    if scale:
        mean_stats = calculate_destrieux_mean(stats_df)
        data = mean_stats.copy()
        if isinstance(data, pd.Series):
            data = data.to_frame()
        standardized_values = StandardScaler().fit_transform(mean_stats)
        data.loc[:, :] = standardized_values * 100
    else:
        data = stats_df
    hemi_stats = data.xs(hemisphere, level="Hemisphere")
    destrieux_projection = destrieux_atlas[f"map_{hemisphere.lower()}"].copy()
    region_ids = sorted(set(destrieux_projection))
    for i, region_id in enumerate(region_ids):
        label = destrieux_labels[i]
        if label == MEDIAL_WALL:
            value = 0
        elif scale:
            value = hemi_stats.loc[label, measurement]
        else:
            value = hemi_stats.loc[(measurement, label)]
        destrieux_projection[destrieux_projection == region_id] = value
    surface = plotting.view_surf(
        fsaverage[f"infl_{hemisphere.lower()}"],
        destrieux_projection,
        bg_map=fsaverage[f"sulc_{hemisphere.lower()}"],
        cmap="coolwarm",
        title=title,
    )
    surface.resize(600, 400)
    return surface
