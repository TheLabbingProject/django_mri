from django.apps import apps
from django.db.models import QuerySet
from django_analyses.models.run import Run
from django_mri.analysis.metric.mriqc import MRIQC_METRICS
from django_mri.models.metric import Metric
from django_mri.models.scan import Scan


def create_mriqc_scores(run: Run) -> QuerySet:
    Score = apps.get_model("django_mri", "Score")
    df = run.parse_output()
    score_ids = []
    for nii_stem, scores in df.iterrows():
        origin = Scan.objects.get(_nifti__path__endswith=f"{nii_stem}.nii.gz")
        for metric_title, value in scores.iteritems():
            try:
                metric = Metric.objects.get(title=metric_title)
            except Metric.DoesNotExist:
                for metric_definition in MRIQC_METRICS:
                    Metric.objects.get_or_create(**metric_definition)
                try:
                    metric = Metric.objects.get(title=metric_title)
                except Metric.DoesNotExist:
                    print(f"Metric {metric_title} not registered, skipping.")
                    continue
            except Metric.MultipleObjectsReturned:
                print(f"{metric_title} return multiple!")
                metric = Metric.objects.filter(title=metric_title).first()
            score, _ = Score.objects.get_or_create(
                run=run, metric=metric, value=value
            )
            if not score.origin.exists():
                score.origin.set([origin])
            score_ids.append(score.id)
    return Score.objects.filter(id__in=score_ids)
