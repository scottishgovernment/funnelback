import click
from .cmd_audit import audit


@click.group()
def licence():
    pass


licence.add_command(audit)
