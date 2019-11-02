import click
from ..config import config
from ..backends import check_backend


@click.command(short_help='lists all backends')
@click.option("--check/--no-check", default=False, help='Checks if the backends are available.')
def backends(check):
    """
    Lists all possible computational backends on this machine.

    """
    ls(check)


def ls(check):
    """Prints all backends.

    :param check: returns backends availability if true
    """
    fmt = "{0:20}{1:60}{2:10}"
    click.secho(fmt.format("NAME", "DESCRIPTION", "STATUS"))
    for k, v in config.backends.items():
        if check:
            status = "OK" if check_backend(k) else "NOT OK"
        else:
            status = "N/A"
        default = {"short_description": "no description given"}
        click.secho(
            fmt.format(k, v.get("metadata", default)["short_description"], status)
        )
