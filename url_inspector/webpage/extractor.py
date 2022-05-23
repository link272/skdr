from bs4 import BeautifulSoup
import requests

DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


class LinkExtractor(object):

    def __init__(self, headers=DEFAULT_HEADERS):
        self.headers = headers

    def extract(self, url):
        result = {
            "http": [],
            "email": [],
            "tel": []
        }
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise ValueError("Error")
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup.find_all("a"):
            name = tag.string
            if name == "":
                pass
            if "tel:" in tag["href"]:
                result["tel"].append(name)
            elif "mailto:" in tag["href"]:
                result["mail"].append(name)
            elif "http" in tag["href"]:
                result["http"].append(name)
            else:
                pass
        result["nb_http"] = len(result["http"])
        result["nb_tel"] = len(result["tel"])
        result["nb_email"] = len(result["email"])
        result["total"] = result["nb_http"] + result["nb_tel"] + result["nb_email"]
        return result
