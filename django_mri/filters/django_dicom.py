from django_dicom.models import Series
from django_dicom.serializers import SeriesSerializer
from rest_framework import generics


class UnreviewedDicoms(generics.ListAPIView):
    serializer_class = SeriesSerializer

    def get_queryset(self):
        return Series.objects.filter(scan__isnull=True)
