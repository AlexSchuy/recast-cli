import click

from .subcommands.backends import backends

'''
from .subcommands.run import run, submit, retrieve, status
from .subcommands.catalogue import catalogue
from .subcommands.auth import auth
from .subcommands.backends import backends
from .subcommands.testing import testing
from .subcommands.ci import ci
'''


@click.group()
def recast_cli():
    pass


recast_cli.add_command(backends)

'''
recastatlas.add_command(run, "run")
recastatlas.add_command(submit, "submit")
recastatlas.add_command(retrieve, "retrieve")
recastatlas.add_command(status, "status")
recastatlas.add_command(catalogue, "catalogue")
recastatlas.add_command(auth, "auth")
recastatlas.add_command(backends, "backends")
recastatlas.add_command(ci, "ci")
recastatlas.add_command(testing, "tests")
'''
