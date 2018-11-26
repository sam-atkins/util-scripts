import requests


def api_request(method, url, params):
    try:
        response = requests.request(method=method, url=url, params=params)
        return response
    except Exception as ex:
        raise Exception(f"Unsuccessful attempt to hit endpoint {url}: {ex}")
