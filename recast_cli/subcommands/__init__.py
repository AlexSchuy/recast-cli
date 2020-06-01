import click
from pathlib import Path
import pkg_resources
import os
import yaml

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


def save_workflow(wf_dict: dict, save_path: Path):
    """
    Save workflow dictionary to given save_path
    """
    with open(save_path, 'w+') as save_file:
        yaml.dump(wf_dict, save_file)


def get_wf_dict(wf_path):
    """
    Get workflow dictionary from file path
    """
    with open(wf_path, 'r+') as wf_file:
        return yaml.safe_load(wf_file)
