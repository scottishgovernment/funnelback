import click
import json
import os

from .worktree import Worktree
from ..environments import ENVS
from .role import Role


@click.command()
@click.argument("environment")
@click.option("--dryrun", flag_value=True, type=click.BOOL)
def sync(environment, dryrun):
    env = ENVS[environment]
    worktree = Worktree()
    role_ids = env.get_roles()
    design_files = worktree.design_files(env)
    for path in design_files.values():
        role = load_role(path)
        id = role.id
        if id not in role_ids:
            env.create_role(id)
        state = env.get_role(id)
        diff = state.diff(role)
        for d in diff:
            if not dryrun:
                d.apply(env, role.path)


def load_role(file):
    with open(file, "r") as f:
        return Role(json.load(f))
