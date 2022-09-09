import json


class UnrestrictableListProperty:
    def __init__(self, json_property, collection, item):
        self.property = json_property
        self.unrestricted_url = f"{collection}/unrestricted-access"
        self.url = f"{collection}/{item}"

    def from_json(self, role):
        return UnrestrictableListValue(self, role["data"][self.property])


class UnrestrictableListValue:
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
        if not isinstance(value, UnrestrictableListValue):
            raise f"Incorrect property type: {value}"
        if self.property.property != value.property.property:
            raise f"Mismatched property: {value.property.property}"

        unrestricted = None
        if self.unrestricted != value.unrestricted:
            unrestricted = value.unrestricted
        added = [v for v in value.values if v not in self.values]
        removed = [v for v in self.values if v not in value.values]
        return UnrestrictableListDiff(self.property, unrestricted, added, removed)

    def normalise(self):
        list.sort(self.values)

    def __str__(self):
        return str(self.json)


class UnrestrictableListDiff:
    def __init__(self, property, unrestricted, added, removed):
        self.property = property
        self.unrestricted = unrestricted
        self.added = added
        self.removed = removed

    @property
    def changed(self):
        return (self.unrestricted is not None) or self.added or self.removed

    def apply(self, env, id):
        if self.unrestricted is not None:
            url = f"roles/{id}/{self.property.unrestricted_url}"
            if self.unrestricted:
                env.put(url)
            else:
                env.delete(url)
        for item in self.added:
            url = f"roles/{id}/{self.property.url}/{item}"
            env.put(url)
        for item in self.removed:
            url = f"roles/{id}/{self.property.url}/{item}"
            env.delete(url)

    def __repr__(self):
        v = {}
        if self.unrestricted is not None:
            v["unrestricted"] = self.unrestricted
        if self.added:
            v["added"] = self.added
        if self.removed:
            v["removed"] = self.removed
        return json.dumps(v, indent=2)
