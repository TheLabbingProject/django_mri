"""
Definition of the :class:`SessionSerializer` class.
"""
from django_mri.models.session import Session
from django_mri.serializers.utils import MiniSubjectSerializer
from rest_framework import serializers
from rest_framework.response import Response


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    subject = MiniSubjectSerializer()

    class Meta:
        model = Session
        fields = "id", "subject", "comments", "time"

    def patch(self, request, pk) -> Response:
        """
        Handles "PATCH" requests.

        Parameters
        ----------
        request : Request
            HTTP request object
        pk : int
            Session primary key

        Returns
        -------
        Response
            HTTP response with updated instance or error message
        """

        instance = Session.objects.get(id=pk)
        serializer = SessionSerializer(
            instance=instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(code=201, data=serializer.data)
        return Response(code=400, data=f"Failed to patch session #{pk}")
