import click
import yaml
from ..subcommands import *
from .catalogue import add as catalogue_add

from ..workflow.recast_workflow.scripts import scan as scan_backend

@click.group(help="RECAST Scan Features")
def scan():
    pass

@scan.command()
@click.argument('workflow', nargs=1)
@click.option('-o', '--output_path')
@click.pass_context
def build(ctx, workflow: str, output_path: str):
    """
    Convert existing singlestep-stage workflow into multistage workflow for scans.
    """
    # get Workflow as dictionary from file
    wf_path = get_workflow_file_path(workflow)
    with open(wf_path, 'r+') as wf_file:
        wf_yml = yaml.safe_load(wf_file)

        # use build_multi to get new workflow
        wf_yml = scan_backend.build_multi(wf_yml)

    # Save new wflow to output path if specified
    if output_path:
        with open(output_path, 'w+') as output_file:
            yaml.dump(wf_yml, output_file)
    else:
        # Save to catalogue
        ctx.invoke(catalogue_add, workflow_dict=wf_yml)
