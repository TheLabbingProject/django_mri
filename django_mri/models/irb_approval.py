from django.db import models


class IrbApproval(models.Model):
    """
    A model representing an institutional review board approval information.
    """

    #: The institution that gave the approval.
    institution = models.CharField(max_length=128, blank=True, null=True)

    #: IRB Approval ID.
    number = models.CharField(max_length=32, blank=False, null=False)

    #: Approval document.
    document = models.FileField(
        max_length=1000, upload_to="mri/irb/", blank=True, null=True
    )

    class Meta:
        verbose_name = "IRB Approval"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """

        return f"{self.institution} | {self.number}"
