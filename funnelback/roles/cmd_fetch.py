import click

from ..environments import ENVS
from .worktree import Worktree


@click.command()
@click.argument("environment")
def fetch(environment):
    env = ENVS[environment]
    role_ids = env.get_roles()
    for id in role_ids:
        role = env.get_role(id)
        role.normalise()
        worktree = Worktree()
        worktree.write_state(env, role)
