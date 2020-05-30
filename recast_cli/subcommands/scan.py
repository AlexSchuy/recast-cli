import click

@click.group(help="RECAST Scan Features")
def scan():
    pass

@scan.command()
def build(workflow: str):
    """
    Convert existing singlestep-stage workflow into multistage workflow for scans.

    :param workflow: singlestep-stage workflow file
    :return:
    """
    click.echo("building scan...")
