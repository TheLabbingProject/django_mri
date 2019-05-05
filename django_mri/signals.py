# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from django_dicom.models import Image
# from django_mri.models import Scan


# @receiver(post_save, sender=Image)
# def post_save_series_model_receiver(sender, instance, created, *args, **kwargs):
#     """
#     After a new DICOM series is created with django_dicom_, create a
#     :class:`django_mri.Scan` instance to represent it. This only occurs if the Series has
#     its "*is_updated*" field set to True, so that the relevant meta-data may be
#     updated for the series upon creation as well.

#     .. _django_dicom: https://github.com/ZviBaratz/django_dicom

#     Parameters
#     ----------
#     sender : type
#             The model sending the signal, in this case :class:`django_dicom.Series`.
#     instance : :class:`django_dicom.Series`
#             The instance being saved.
#     created : bool
#             Whether the instance was created in this save call.

#     """

#     scan, _ = Scan.objects.get_or_create(dicom=instance.series)
#     if not scan.is_updated_from_dicom:
#         scan.update_fields_from_dicom()
#         scan.save()
#     return scan

