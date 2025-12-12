import json
import os

import click

from ..environments import ENVS
from ..worktree import Worktree
from .role import Role


@click.command()
@click.argument("environment")
@click.option("--dryrun", flag_value=True, type=click.BOOL)
def sync(environment, dryrun):
    env = ENVS[environment]
    worktree = Worktree("roles")
    role_ids = env.get_roles()
    design_files = worktree.design_files(env)

    roles = {}
    for path in design_files.values():
        role = load_role(path, env.client_id)
        roles[path] = role
        id = role.id
        if id not in role_ids and not dryrun:
            env.create_role(id)

    for path in design_files.values():
        role = roles[path]
        state = env.get_role(role.id)
        diff = state.diff(role)
        for d in diff:
            if not dryrun:
                d.apply(env, role.path(env.client_id))
            else:
                print(d)


def load_role(file, client_id):
    def rewrite_resource(resource, client_id):
        splits = resource.split("~")
        if splits[0] == "dxp":
            return resource
        return client_id + "~" + splits[1]

    def rewrite_property(role, property, client_id):
        values = role["data"][property]
        new_values = [rewrite_resource(v, client_id) for v in values]
        role["data"][property] = new_values

    def rewrite_unrestrictable(role, property, client_id):
        property = role["data"][property]
        values = property["specificallyAllowedValues"]
        new_values = [rewrite_resource(v, client_id) for v in values]
        property["specificallyAllowedValues"] = new_values

    with open(file, "r") as f:
        try:
            role = json.load(f)
            rewrite_property(role, "inRoles", client_id)
            rewrite_unrestrictable(role, "collections", client_id)
            rewrite_unrestrictable(role, "canEditRoles", client_id)
            rewrite_unrestrictable(role, "canGrantRoles", client_id)
            # rewrite_unrestrictable(role, "profiles", client_id)
            return Role(role)
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"Could not parse file as JSON: {file}") from e
