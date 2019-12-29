import pytest

from ..config import ET_ROOT
from ..client import _etrequest, get_project


def test_etrequest():
    endpoint = "http://fakeendpoint/"
    with pytest.raises(RuntimeError):
        _etrequest(endpoint, method="get")
    assert _etrequest(ET_ROOT)
    # ensure timeout is working properly
    endpoint = "https://google.com"
    with pytest.raises(RuntimeError):
        _etrequest(endpoint, timeout=0.01)
    assert _etrequest(endpoint)


def test_get_project():
    repo = "invalidrepo"
    with pytest.raises(ValueError):
        get_project(repo)
    repo = "github/hub"
    res = get_project(repo)
    assert "version" in res
