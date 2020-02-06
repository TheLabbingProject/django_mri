from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_analyses.models.input.types.file_input import FileInput
from django_analyses.models.output.types.file_output import FileOutput
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan


@receiver(post_save, sender=FileOutput)
def file_output_post_save_receiver(sender, instance, created, **kwargs):
    is_nifti = instance.value.endswith(".nii") or instance.value.endswith(".nii.gz")

    # Try to associate with the parent Scan instance
    if is_nifti and created:

        # First find input NIfTI instances
        run_inputs = FileInput.objects.filter(run=instance.run)
        nifti_inputs = run_inputs.filter(
            Q(value__endswith=".nii") | Q(value__endswith=".nii.gz")
        )

        # If NIfTI input instances were found, look for a distinct parent.
        if nifti_inputs:
            niftis = NIfTI.objects.filter(path__in=list(nifti_inputs))
            parents = set(niftis.values_list("parent", flat=True))
            if len(parents) == 1:
                scan = Scan.objects.get(id=parents.pop())
                NIfTI.objects.get_or_create(
                    path=instance.value, is_raw=False, parent=scan
                )
                return

        # If there are no NIfTI instances in the input, or no distinct
        # Scan instance could be determined as the parent, create an
        # orphan NIfTI instance.
        NIfTI.objects.get_or_create(path=instance.value, is_raw=False)
