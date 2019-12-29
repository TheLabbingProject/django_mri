from django_analyses.models.category import Category
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:category-detail")
    parent = serializers.HyperlinkedRelatedField(
        view_name="analysis:category-detail", queryset=Category.objects.all()
    )
    subcategories = serializers.HyperlinkedRelatedField(
        view_name="analysis:category-detail", queryset=Category.objects.all(), many=True
    )

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "description",
            "created",
            "modified",
            "parent",
            "subcategories",
            "url",
        )
