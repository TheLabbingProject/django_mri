from django.db.models.query import QuerySet


class SessionQuerySet(QuerySet):
    def get_scan_set(self) -> QuerySet:
        Scan = self.model.scan_set.rel.related_model
        return Scan.objects.filter(session__in=self.all())
