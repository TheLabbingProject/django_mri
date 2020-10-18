from celery import shared_task

# from django_analyses.tasks import execute_node


@shared_task(name="django_mri.cat12.7-execution")
def execute_cat12():
    pass
