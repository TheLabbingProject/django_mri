REGIONS = [
    {
        "title": "caudalanteriorcingulate",
        "description": "Caudal anterior-cingulate cortex.",
    },
    {
        "title": "caudalmiddlefrontal",
        "description": "Caudal middle frontal gyrus.",
    },
    {"title": "cuneus", "description": "Cuneus cortex."},
    {"title": "entorhinal", "description": "Entorhinal cortex."},
    {"title": "fusiform", "description": "Fusiform gyrus."},
    {"title": "inferiorparietal", "description": "Inferior parietal cortex."},
    {"title": "inferiortemporal", "description": "Inferior temporal gyrus."},
    {
        "title": "isthmuscingulate",
        "description": "Isthmus – cingulate cortex.",
    },
    {"title": "lateraloccipital", "description": "Lateral occipital cortex."},
    {
        "title": "lateralorbitofrontal",
        "description": "Lateral orbital frontal cortex.",
    },
    {"title": "lingual", "description": "Lingual gyrus."},
    {
        "title": "medialorbitofrontal",
        "description": "Medial orbital frontal cortex.",
    },
    {"title": "middletemporal", "description": "Middle temporal gyrus."},
    {"title": "parahippocampal", "description": "Parahippocampal gyrus."},
    {"title": "paracentral", "description": "Paracentral lobule."},
    {"title": "parsopercularis", "description": "Pars opercularis."},
    {"title": "parsorbitalis", "description": "Pars orbitalis."},
    {"title": "parstriangularis", "description": "Pars triangularis."},
    {"title": "pericalcarine", "description": "Pericalcarine cortex."},
    {"title": "postcentral", "description": "Postcentral gyrus"},
    {
        "title": "posteriorcingulate",
        "description": "Posterior-cingulate cortex.",
    },
    {"title": "precentral", "description": "Precentral gyrus."},
    {"title": "precuneus", "description": "Precuneus cortex."},
    {
        "title": "rostralanteriorcingulate",
        "description": "Rostral anterior cingulate cortex.",
    },
    {
        "title": "rostralmiddlefrontal",
        "description": "Rostral middle frontal gyrus.",
    },
    {"title": "superiorfrontal", "description": "Superior frontal gyrus."},
    {"title": "superiorparietal", "description": "Superior parietal cortex."},
    {"title": "superiortemporal", "description": "Superior temporal gyrus."},
    {"title": "supramarginal", "description": "Supramarginal gyrus."},
    {
        "title": "transversetemporal",
        "description": "Transverse temporal cortex.",
    },
    {"title": "insula", "description": "Insular cortex."},
]
DESCRIPTION: str = """Desikan-Killiany-Tourville cortical labeling protocol.
101 labeled brain images and a consistent human cortical labeling protocol. Arno Klein, Jason Tourville. Frontiers in Brain Imaging Methods. 6:171. DOI: 10.3389/fnins.2012.00171
See also https://mindboggle.readthedocs.io/en/latest/labels.html."""
DKT = {
    "title": "DKT",
    "description": DESCRIPTION,
    "symmetric": True,
    "regions": REGIONS,
}

# flake8: noqa: E501
