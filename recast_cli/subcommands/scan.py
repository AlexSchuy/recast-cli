import click
import yaml
from ..subcommands import *

from ..workflow.recast_workflow.scripts import scan

@click.group(help="RECAST Scan Features")
def scan():
    pass

@scan.command()
def build(workflow: str, output_path: str):
    """
    Convert existing singlestep-stage workflow into multistage workflow for scans.

    :param workflow: singlestep-stage workflow file
    :return:
    """
    wf_path = get_workflow_file_path(workflow)
    with open(wf_path, 'r+') as wf_file:
        wf_yml = yaml.safe_load(wf_file)
        wf_yml = scan.build_multi(wf_yml)

    with open(output_path, 'w+') as output_file:
        yaml.dump(wf_yml, output_file)
