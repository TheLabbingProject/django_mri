from django.apps import apps
from django.db.models import QuerySet
from django_analyses.models.run import Run
from django_mri.analysis.metric.freesurfer import RECON_ALL_ANATOMICAL_STATS
from django_mri.models.atlas import Atlas
from django_mri.models.metric import Metric
from django_mri.models.region import Region
from django_mri.models.scan import Scan


def create_recon_all_scores(run: Run) -> QuerySet:
    Score = apps.get_model("django_mri", "Score")
    df = run.parse_output()
    by_metric = df.to_dict()
    origin = Scan.objects.filter(_nifti__path__in=run.get_input("T1_files"))
    score_ids = []
    for metric_title, region_id in by_metric.items():
        try:
            metric = Metric.objects.get(title=metric_title)
        except Metric.DoesNotExist:
            for metric_definition in RECON_ALL_ANATOMICAL_STATS:
                Metric.objects.get_or_create(**metric_definition)
            try:
                metric = Metric.objects.get(title=metric_title)
            except Metric.DoesNotExist:
                continue
        for key, value in region_id.items():
            atlas_title, hemisphere_label, region_title = key
            atlas, _ = Atlas.objects.get_or_create(title=atlas_title)
            region, _ = Region.objects.get_or_create(
                atlas=atlas,
                hemisphere=hemisphere_label[0],
                title=region_title,
            )
            score, _ = Score.objects.get_or_create(
                run=run, region=region, metric=metric, value=value,
            )
            if not score.origin.exists():
                score.origin.set(origin)
            score_ids.append(score.id)
    return Score.objects.filter(id__in=score_ids)
