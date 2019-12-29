from requests import request, ConnectionError, ReadTimeout

from .config import ET_PROJECTS


def _etrequest(endpoint, method="get", **kwargs):
    if kwargs.get('timeout') is None:
        kwargs['timeout'] = 5
    try:
        res = request(method, endpoint, **kwargs)
    except ConnectionError:
        raise RuntimeError("Connection to server could not be made")
    except ReadTimeout:
        raise RuntimeError(
            "No response from server in {timeout} seconds".format(
                timeout=kwargs.get('timeout')
            )
        )
    res.raise_for_status()
    return res


def get_project(repo, **rargs):
    """
    Fetch latest version from server.

    Parameters
    ==========
    repo : str
        GitHub repository as <owner>/<project>
    **rargs
        Request keyword arguments

    Returns
    =======
    response
        Dictionary with `version` field
    """
    if "/" not in repo:
        raise ValueError("Invalid repository")
    res = _etrequest(ET_PROJECTS.format(repo=repo), **rargs)
    return res.json(encoding="utf-8")
