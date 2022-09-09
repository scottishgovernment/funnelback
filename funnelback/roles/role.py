from ..properties.list_property import ListProperty
from ..properties.string_property import StringProperty
from ..properties.unrestrictable_map import UnrestrictableMapProperty
from ..properties.unrestrictable_list import UnrestrictableListProperty


class Role:

    SELF_DESCRIPTION = StringProperty("selfDescription", "self-description")

    PERMISSIONS = UnrestrictableListProperty("permissions", "permissions", "permission")

    IN_ROLES = ListProperty("inRoles", "in-roles/role")

    EDIT_ROLES = UnrestrictableListProperty("canEditRoles", "can-edit-roles", "role")

    GRANT_ROLES = UnrestrictableListProperty("canGrantRoles", "can-grant-roles", "role")

    COLLECTIONS = UnrestrictableListProperty("collections", "collections", "collection")

    PROFILES = UnrestrictableListProperty("profiles", "profiles", "profile")

    LICENSES = UnrestrictableListProperty("licenses", "licenses", "license")

    READ_CONFIG = UnrestrictableListProperty(
        "canReadConfigKeys",
        "can-read-config-keys",
        "key",
    )

    USER_SUFFIXES = UnrestrictableListProperty(
        "canCreateUsersWithSuffix",
        "can-create-users-with-suffix",
        "suffix",
    )

    ACCESSIBILITY_SCOPE = StringProperty(
        "accessibilityAuditorScope",
        "accessibility-auditor-scope",
    )

    ACCESSIBILITY_DOMAINS = UnrestrictableListProperty(
        "accessibilityAuditorDomains",
        "accessibility-auditor-domains",
        "domain",
    )

    COLLECTION_TYPES = UnrestrictableListProperty(
        "permittedCollectionCreationTypes",
        "permitted-collection-creation-types",
        "type",
    )

    EDIT_USERS = UnrestrictableListProperty("canEditUsers", "can-edit-users", "user")

    ENVIRONMENTS = UnrestrictableListProperty(
        "canEditKeysInConfigEnvironments",
        "can-edit-keys-in-config-environments",
        "env",
    )

    EDIT_CONFIG = UnrestrictableMapProperty(
        "canEditConfigKeys",
        "can-edit-config-keys",
        "key",
    )

    ROLE_SUFFIXES = UnrestrictableListProperty(
        "canCreateRolesWithSuffix",
        "can-create-roles-with-suffix",
        "suffix",
    )

    def __init__(self, json):
        self.properties = []
        self.self_description = self.__add(Role.SELF_DESCRIPTION)
        self.permissions = self.__add(Role.PERMISSIONS)
        self.in_roles = self.__add(Role.IN_ROLES)
        self.can_edit_roles = self.__add(Role.EDIT_ROLES)
        self.can_grant_roles = self.__add(Role.GRANT_ROLES)
        self.collections = self.__add(Role.COLLECTIONS)
        self.licenses = self.__add(Role.LICENSES)
        self.can_read_config_keys = self.__add(Role.READ_CONFIG)
        self.user_suffixes = self.__add(Role.USER_SUFFIXES)
        self.accessibility_scope = self.__add(Role.ACCESSIBILITY_SCOPE)
        self.accessibility_domains = self.__add(Role.ACCESSIBILITY_DOMAINS)
        self.collection_types = self.__add(Role.COLLECTION_TYPES)
        self.can_edit_users = self.__add(Role.EDIT_USERS)
        self.environments = self.__add(Role.ENVIRONMENTS)
        self.can_edit_config_keys = self.__add(Role.EDIT_CONFIG)
        self.role_suffixes = self.__add(Role.ROLE_SUFFIXES)
        self.json = json

    @property
    def id(self):
        return self.json["data"]["id"]

    def __add(self, property):
        self.properties.append(property)
        return property

    def exists(self, env):
        return env.has_role(self.id)

    def diff(self, other):
        diffs = [
            p.from_json(self.json).diff(p.from_json(other.json))
            for p in self.properties
        ]
        return [d for d in diffs if d.changed]

    def normalise(self):
        for p in self.properties:
            p.from_json(self.json).normalise()

    def url(self):
        return f"roles/{self.id}"
