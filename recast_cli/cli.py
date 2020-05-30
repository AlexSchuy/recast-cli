import click

from .subcommands.backends import backends
from .subcommands.catalogue import catalogue
from .subcommands.run import run
from .subcommands.manual import manual
from .subcommands.scan import scan


@click.group()
def recast_cli():
    """THe RECAST Project Command Line Interface"""
    pass


recast_cli.add_command(backends)
recast_cli.add_command(catalogue)
recast_cli.add_command(run)
recast_cli.add_command(manual)
recast_cli.add_command(scan)
