import click

from ..environments import ENVS
from ..worktree import Worktree


@click.command()
@click.argument("environment")
def fetch(environment):
    env = ENVS[environment]
    role_ids = env.get_roles()
    for id in role_ids:
        role = env.get_role(id)
        role.normalise()
        worktree = Worktree("roles")
        name = role.id.split("~")[1]
        worktree.write_state(env, name, role)
