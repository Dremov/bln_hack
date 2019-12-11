import json
import urllib.request

url_address = "http://mockbcknd.tk/"


def get_agents():
    with urllib.request.urlopen(url_address) as url:
        data = json.loads(url.read().decode())
        print(data)
        print(type(data))
        return data

