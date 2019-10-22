import click

from .subcommands.backends import backends
from .subcommands.catalogue import catalogue
from .subcommands.run import run


@click.group()
def recast_cli():
    """RECAST Project command line interface"""
    pass


recast_cli.add_command(backends)
recast_cli.add_command(catalogue)
recast_cli.add_command(run)
