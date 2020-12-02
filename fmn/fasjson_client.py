import requests
import requests.exceptions
from requests.compat import urlencode, urljoin
from requests_gssapi import HTTPSPNEGOAuth


class Client(object):
    """
    A fasjson client to make very specific requests to fasjson.
    Necessary because the official fasjson-client library does not support
    python3.
    """
    def __init__(self, url, principal=None):
        self.url = url
        self.principal = principal

        gssapi_auth = HTTPSPNEGOAuth(
            opportunistic_auth=True, mutual_authentication="OPTIONAL"
        )
        self.session = requests.Session()
        self.session.auth = gssapi_auth

    def search(self, email):
        """
        A very limited search built to only serve fmn's requirement of
        finding a user based on an email.
        """
        # email must be an exact match in fasjson, so we will either have
        # 1 result or empty result
        search_string = "search/users" + "?" + urlencode({"email": email})
        endpoint = urljoin(self.url, search_string)

        return self.session.get(endpoint)

    def get_user(self, username):
        """
        Get a specific user based on their username
        """
        url_string = "users/" + username + "/"
        endpoint = urljoin(self.url, url_string)

        return self.session.get(endpoint)

    def list_all_entities(self, ent_name):
        """
        Return all entities of a certain type. In fmn's case it is users.
        """
        endpoint = urljoin(self.url, ent_name + "/")

        next_page_url = endpoint + "?" + urlencode({"page_number": 1})
        while next_page_url:
            res = self.session.get(next_page_url)
            for item in res["result"]:
                yield item
            next_page_url = res.get("page", {}).get("next_page")
