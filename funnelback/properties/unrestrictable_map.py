import json


class UnrestrictableMapProperty:
    def __init__(self, property, collection, item):
        self.property = property
        self.unrestricted_url = f"{collection}/unrestricted-access"
        self.url = f"{collection}/{item}"

    def from_json(self, role):
        return UnrestrictableMapValue(self, role["data"][self.property])


class UnrestrictableMapValue:
    def __init__(self, property, json):
        self.property = property
        self.json = json

    @property
    def unrestricted(self):
        return self.json["unrestricted"]

    @property
    def values(self):
        return self.json["specificallyAllowedValues"]

    def diff(self, value):
        if not isinstance(value, UnrestrictableMapValue):
            raise f"Incorrect property type: {value}"
        if self.property.property != value.property.property:
            raise f"Mismatched property: {value.property.property}"

        unrestricted = None
        if self.unrestricted != value.unrestricted:
            unrestricted = value.unrestricted
        v1 = self.values
        v2 = value.values
        added = {k: v for k, v in v2.items() if k not in v1 or v1[k] != v}
        removed = [k for k, v in v1.items() if k not in v2 or v2[k] != v]
        return UnrestrictableMapDiff(self.property, unrestricted, added, removed)

    def normalise(self):
        values = {k: v for k, v in sorted(self.values.items())}
        self.json["specificallyAllowedValues"] = values

    def __str__(self):
        return str(self.json)


class UnrestrictableMapDiff:
    def __init__(self, property, unrestricted, added, removed):
        self.property = property
        self.unrestricted = unrestricted
        self.added = added
        self.removed = removed

    @property
    def changed(self):
        return (self.unrestricted is not None) or self.added or self.removed

    def apply(self, env, path):
        if self.unrestricted is not None:
            url = f"{path}/{self.property.unrestricted_url}"
            if self.unrestricted:
                env.put(url)
            else:
                env.delete(url)
        for key, val in self.added.items():
            url = f"{path}/{self.property.url}/{key}"
            env.put(url, json.dumps(val))
        for item in self.removed:
            url = f"{path}/{self.property.url}/{item}"
            env.delete(url)

    def __repr__(self):
        v = {}
        v["property"] = self.property.property
        if self.unrestricted is not None:
            v["unrestricted"] = self.unrestricted
        if self.added:
            v["added"] = self.added
        if self.removed:
            v["removed"] = self.removed
        return json.dumps(v, indent=2)
