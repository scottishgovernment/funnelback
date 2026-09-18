import click
from ..environments import ENVS


@click.command()
@click.argument("environment")
def audit(environment):
    env = ENVS[environment]
    collections = env.get_collections()
    datasources = [c for c in collections if "~ds-" in c]
    counts = []
    for ds in datasources:
        count = env.get_raw(f"/admin-api/license/usage/collections/{ds}/document-count")["data"]
        counts.append((ds, count))
    for (ds, count) in counts:
        print(ds, count)
