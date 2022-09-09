import click
from .cmd_fetch import fetch
from .cmd_sync import sync
from .cmd_drift import drift


@click.group()
def roles():
    pass


roles.add_command(fetch)
roles.add_command(sync)
roles.add_command(drift)
