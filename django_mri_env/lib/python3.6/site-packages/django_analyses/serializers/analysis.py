from django_analyses.models.analysis import Analysis
from django_analyses.models.category import Category
from rest_framework import serializers


class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:analysis-detail")
    category = serializers.HyperlinkedRelatedField(
        view_name="analysis:category-detail", queryset=Category.objects.all()
    )

    class Meta:
        model = Analysis
        fields = (
            "id",
            "title",
            "description",
            "category",
            "created",
            "modified",
            "url",
        )

