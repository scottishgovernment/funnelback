import click

from ..environments import ENVS
from ..worktree import Worktree


@click.command()
@click.argument("environment")
def fetch(environment):
    env = ENVS[environment]
    role_ids = env.get_roles()
    ignored_roles = ["owner-resources", "primary", "in-owner-resources", "resources"]
    ids = [r for r in role_ids if r not in ignored_roles]
    for id in ids:
        role = env.get_role(id)
        role.normalise()
        worktree = Worktree("roles")
        name = role.id
        worktree.write_state(env, name, role)
