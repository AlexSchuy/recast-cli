import click
from pathlib import Path
import pkg_resources
import os

catalogue_dir = Path(pkg_resources.resource_filename("recast_cli", "data/catalogue"))
if not catalogue_dir.exists():
    os.mkdir(catalogue_dir)


def get_workflow_file_path(workflow_name: str):
    """
    Echos message if workflow is not found in the catalogue

    :return: workflow file path or None
    """
    workflow_file = Path(os.path.abspath(catalogue_dir / (workflow_name + ".yml")))
    if not workflow_file.exists():
        click.secho(f"Workflow named {workflow_name} not found in catalogue.")
        return
    return workflow_file
