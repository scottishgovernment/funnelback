import json


class StringProperty:
    def __init__(self, property, url):
        self.property = property
        self.url = url

    def from_json(self, role):
        return StringValue(self, role["data"][self.property])


class StringValue:
    def __init__(self, property, json):
        self.property = property
        self.json = json

    @property
    def value(self):
        return self.json

    def diff(self, value):
        if not isinstance(value, StringValue):
            raise f"Incorrect property type: {value}"
        if self.property.property != value.property.property:
            raise f"Mismatched property: {value.property.property}"

        changed = self.value != value.value
        if changed:
            new_value = value.value
        else:
            new_value = None
        return StringDiff(self.property, changed, new_value)

    def normalise(self):
        pass

    def __str__(self):
        return str(self.json)


class StringDiff:
    def __init__(self, property, changed, value):
        self.property = property
        self._changed = changed
        self.value = value

    @property
    def changed(self):
        return self._changed

    def apply(self, env, id):
        if self.changed:
            url = f"roles/{id}/{self.property.url}"
            v = {}
            v[self.property.property] = self.value
            js = json.dumps(v)
            env.put(url, js)

    def __repr__(self):
        v = {}
        if self.changed:
            v["property"] = self.property.property
            v["changed"] = self.value
        return json.dumps(v, indent=2)
