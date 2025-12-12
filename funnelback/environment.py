from os import environ

from httpx import Client, NetRCAuth

from .roles.role import Role


class Environment:
    def __init__(self, name, client_id):
        self.name = name
        self.base_url = "https://dxp02-uk-admin.funnelback.squiz.cloud"
        self.client_id = client_id
        self.__client = None

    def has_role(self, id):
        url = Role.path_for_id(self.client_id, id)
        r = self.client.head(url)
        if r.status_code == 200:
            return True
        if r.status_code == 404:
            return False
        raise Exception(
            f"Could not check if {id} exists on {self.name} ({r.status_code})"
        )

    def create_role(self, id):
        url = Role.path_for_id(self.client_id, id)
        print(f"PUT {self.base_url}/{url}?client-id={self.client_id}")
        r = self.client.put(
            url,
            params={"editable-in-role": f"{self.client_id}~owner-resources"},
        )
        if r.status_code != 200:
            raise Exception(
                f"Could not create role {id} on {self.name}",
                r,
                r.json()["errorMessage"],
            )

    def get_role(self, id):
        path = Role.path_for_id(self.client_id, id)
        return Role(self.get(path))

    def get_roles(self):
        def built_in(role):
            return role.startswith("_default_roles_~") or role.startswith("dxp~")

        path = "/admin-api/account/v2/editable-roles"
        roles = [r for r in self.get(path)["data"] if not built_in(r)]
        roles = [r.split("~")[1] for r in roles]
        return roles

    def get(self, url):
        print(f"GET {self.base_url}{url}?client-id={self.client_id}")
        r = self.client.get(url, params={"client-id": self.client_id})
        if r.status_code != 200:
            raise Exception(f"Could not GET {url}", r)
        return r.json()

    def put(self, url, content=None):
        print(f"PUT {self.base_url}/{url}?client-id={self.client_id}")
        r = self.client.put(url, content=content, params={"client-id": self.client_id})
        if r.status_code != 200:
            # raise Exception(f"Could not PUT {url}", r.json()["errorMessage"])
            print(f"Could not PUT {url}", r.json()["errorMessage"])

    def delete(self, url):
        print(f"DELETE {self.base_url}/{url}?client-id={self.client_id}")
        r = self.client.delete(url, params={"client-id": self.client_id})
        if r.status_code != 200:
            raise Exception(f"Could not DELETE {url}", r)

    @property
    def client(self):
        if not self.__client:
            auth = NetRCAuth(file=environ.get("NETRC"))
            self.__client = Client(
                auth=auth,
                base_url=self.base_url,
                headers={"Content-Type": "application/json"},
            )
        return self.__client
