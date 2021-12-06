from typing import Dict

from bs4 import BeautifulSoup

DEFAULT_DESTINATION_ID: str = "bk-app"
CSV_CONTENT_TYPE: str = "text/csv"
SESSIONS_CSV_HEADERS: Dict[str, str] = {
    "Content-Disposition": 'attachment; filename="sessions.csv"'
}


def fix_bokeh_script(
    html: str, destination_id: str = DEFAULT_DESTINATION_ID
) -> str:
    soup = BeautifulSoup(html, features="lxml")
    element = soup(["script"])[0]
    random_id = element.attrs["id"]
    script = element.contents[0]
    return script.replace(random_id, destination_id)


class ReadWriteSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set read_serializer_class and write_serializer_class attributes on a
    viewset.

    References
    ----------
    * https://www.revsys.com/tidbits/using-different-read-and-write-serializers-django-rest-framework/
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
            "'%s' should either include a `read_serializer_class` attribute,"
            "or override the `get_read_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
            "'%s' should either include a `write_serializer_class` attribute,"
            "or override the `get_write_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.write_serializer_class
