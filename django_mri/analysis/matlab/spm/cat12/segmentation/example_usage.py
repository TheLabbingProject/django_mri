# Create analyses in the DB
from django_mri.analysis.analysis_definitions import analysis_definitions

Analysis.objects.from_list(analysis_definitions)

# Create node
cat = Analysis.objects.get(title__contains="CAT")
cat_v = cat.version_set.first()
cat_node = Node.objects.create(analysis_version=cat_v, configuration={"cobra": True})

# Run node
mprage = Scan.objects.filter(description__icontains="MPRAGE").first()
results = cat_node.run({"path": mprage.nifti.path})

