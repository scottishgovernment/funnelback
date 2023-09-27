from httpx import Client
from .roles.role import Role


class Environment:
    def __init__(self, name, client, prefix=None):
        self.name = name
        if prefix is None:
            hostname = f"{client}-admin.clients.uk.funnelback.com"
        else:
            hostname = f"{prefix}-{client}-admin.clients.uk.funnelback.com"
        self.base_url = f"https://{hostname}/admin-api/account/v2"
        self.__client = None

    def has_role(self, id):
        url = f"{self.base_url}/roles/{id}"
        r = self.client.head(url)
        if r.status_code == 200:
            return True
        if r.status_code == 404:
            return False
        raise Exception(
            f"Could not check if {id} exists on {self.name} ({r.status_code})"
        )

    def create_role(self, id):
        url = f"{self.base_url}/roles/{id}"
        r = self.client.put(url, params={'editable-in-role': 'govscot~infrastructure'})
        if r.status_code != 200:
            raise Exception(f"Could not create role {id} on {self.name}", r)

    def get_role(self, id):
        return Role(self.get(f"roles/{id}"))

    def get_roles(self):
        return [ r for r in self.get("editable-roles")["data"] if not r.startswith("default~") ]

    def get(self, url):
        print(f"GET {self.base_url}/{url}")
        r = self.client.get(url)
        if r.status_code != 200:
            raise Exception(f"Could not GET {url}", r)
        return r.json()

    def put(self, url, content=None):
        print(f"PUT {self.base_url}/{url}")
        r = self.client.put(url, content=content)
        if r.status_code != 200:
            raise Exception(f"Could not PUT {url}")

    def delete(self, url):
        print(f"DELETE {self.base_url}/{url}")
        r = self.client.delete(url)
        if r.status_code != 200:
            raise Exception(f"Could not DELETE {url}", r)

    @property
    def client(self):
        if not self.__client:
            self.__client = Client(
                base_url=self.base_url,
                headers={"Content-Type": "application/json"},
            )
        return self.__client
