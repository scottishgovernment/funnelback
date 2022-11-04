class ListProperty:
    def __init__(self, property, url):
        self.property = property
        self.url = url

    def from_json(self, role):
        return ListValue(self, role["data"][self.property])


class ListValue:
    def __init__(self, property, json):
        self.property = property
        self.json = json

    @property
    def values(self):
        return self.json

    def diff(self, value):
        if not isinstance(value, ListValue):
            raise f"Incorrect property type: {value}"
        if self.property.property != value.property.property:
            raise f"Mismatched property: {value.property.property}"

        added = [v for v in value.values if v not in self.values]
        removed = [v for v in self.values if v not in value.values]
        return ListDiff(self.property, added, removed)

    def normalise(self):
        list.sort(self.json)

    def __str__(self):
        return str(self.json)


class ListDiff:
    def __init__(self, property, added, removed):
        self.property = property
        self.added = added
        self.removed = removed

    @property
    def changed(self):
        return self.added or self.removed

    def apply(self, env, id):
        for item in self.added:
            url = f"roles/{id}/{self.property.url}/{item}"
            env.put(url)
        for item in self.removed:
            url = f"roles/{id}/{self.property.url}/{item}"
            env.delete(url)

    def __repr__(self):
        v = {}
        v["property"] = self.property.property
        if self.added:
            v["added"] = self.added
        if self.removed:
            v["removed"] = self.removed
        return str(v)
