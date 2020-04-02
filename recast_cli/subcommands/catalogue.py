from typing import Dict

import click
import yaml
import os
from distutils.dir_util import copy_tree
import string
from pathlib import Path
import shutil

import pkg_resources
import getpass

from ..workflow.recast_workflow.common import utils
from ..workflow.recast_workflow.scripts import catalogue as ctlg
from ..workflow.recast_workflow.scripts import workflow

default_meta = {"author": "unknown", "short_description": "no description"}

catalogue_dir = Path(pkg_resources.resource_filename("recast_cli", "data/made_workflows"))
if not catalogue_dir.exists():
    os.mkdir(catalogue_dir)

@click.group(help="The RECAST Analysis Catalogue")
def catalogue():
    pass


# TODO: Add description/no description option
@catalogue.command()
def inputs():
    """Parameters available for generating valid combinations.
    """
    params = utils.get_common_inputs(include_descriptions=True)
    fmt = '{0:20}{1:60}{2:40}'
    click.secho(fmt.format(
        'INPUT',
        'DESCRIPTION',
        'STEPS'
    ))
    for key, value in params.items():
        click.secho(
            fmt.format(
                key,
                value.get('description', 'no description'),
                str(value.get('steps', 'no steps'))
            )
        )


@catalogue.command()
@click.argument('params', nargs=-1)
@click.pass_context
def combinations(ctx, params):
    """
    Returns all valid catalogue combinations for the given common inputs.
    Filters combinations using common inputs.
    Makes one combination into yadage file.
    """
    input_parameters = {}
    for i in params:
        lst = i.split('=')
        if not len(lst) == 2:
            click.secho('Invalid parameters.')
            return
        else:
            input_parameters[lst[0]] = lst[1]

    # Add common inputs
    done_adding_params = False
    while not done_adding_params:
        valid = ctlg.get_valid_combinations(input_parameters)
        fmt = '{0:20}{1:30}'

        if len(valid) < 1:
            click.secho('No valid combinations for given common inputs')

        for index, combination in enumerate(valid):
            click.secho('-' * 50)
            click.secho(f'Combination {index + 1}:')
            click.secho(fmt.format('STEP', 'NAME'))
            for k, v in combination.items():
                click.secho(fmt.format(k, v))
        click.secho()

        click.secho("Current common inputs used:")
        for k, v in input_parameters.items():
            click.secho(f"{k}: {v}")
        click.secho()

        param_to_add = click.prompt('Add an additional common input or enter \'done\' to continue', type=str)
        if param_to_add == '' or param_to_add.lower() == 'done':
            done_adding_params = True
            continue
        else:
            param_to_add = param_to_add.split('=')

        if len(param_to_add) == 2:
            input_parameters[param_to_add[0]] = param_to_add[1]
        else:
            click.secho("Common input not recognized.")

    click.confirm('Do you want to start the "make" process?', abort=True)

    # Pick a combination number
    workflow_index = click.prompt('Please select the combination, or enter 0 to cancel', type=int) - 1
    while not -1 <= workflow_index < len(valid):
        workflow_index = click.prompt('Invalid index. Try again', type=int) - 1
    if workflow_index < 0:
        return

    env = valid[workflow_index]
    steps = []
    names = []
    env_settings = []
    for k, v in env.items():
        steps.append(k)
        names.append(v)
        env_settings.append({})

    workflow_text = yaml.dump(workflow.make_workflow(steps, names, env_settings))

    # save workflow yaml as file
    workflow_name = '-'.join(names)
    save_file = catalogue_dir / (workflow_name + ".yml")
    if save_file.exists():
        click.confirm(f'Workflow {workflow_name} already exists. Overwrite this workflow?', abort=True)
    with open(save_file, 'w+') as f:
        f.write(workflow_text)

    click.secho(f"Workflow {workflow_name} saved to catalogue.")

@catalogue.command()
@click.argument('workflow_name', nargs=1)
@click.argument('destination', nargs=1, required=False)
def getyml(workflow_name: str, destination: str):
    """
    Get yaml workflow file in catalogue for workflow name
    """
    # check workflow_name.yml is in catalogue
    workflow_file = catalogue_dir / (workflow_name + ".yml")
    if not workflow_file.exists():
        print(f"Workflow named {workflow_name} not found in catalogue.")
        return

    # copy file
    if not destination:
        destination = os.getcwd()

    shutil.copyfile(workflow_file, destination + (f"/{workflow_name}.yml"))
    print(f"Workflow {workflow_name} copied to {destination}.")



@catalogue.command()
@click.argument('workflow_name', nargs=1)
def get(workflow_name: string):
    """
    Create runnable yadage directory given workflow name
    """
    workflow_file = Path(os.path.abspath(workflow_name))
    save_dir = Path(os.path.abspath(os.path.join(workflow_file, '..')))
    save_dir /= Path(os.path.basename(workflow_file).rstrip(".yml"))
    template = Path(pkg_resources.resource_filename("recast_cli", "data/templates/yadage_dir"))

    if save_dir.exists():
        click.secho("Workflow folder already saved with that name. Rename or move folder and try again.")
        return

    # Create directory
    try:
        os.mkdir(save_dir)
        copy_tree(str(template), str(save_dir))
        os.rename(workflow_file, save_dir / "workflows" / "workflow.yml")
    except FileNotFoundError:
        raise FileNotFoundError("Workflow file does not exist.")

    click.secho(f"Made yadage directory at {save_dir} using {workflow_file}")


@catalogue.command()
@click.argument('workflow_name', nargs=1)
def get_inputs(workflow_name: str):
    """
    Generates input.yml file that contains all input required to run the given workflow.
    """
    workflow_file = catalogue_dir / workflow_name
    if not workflow_file.exists():
        print(f"Workflow named f{workflow_name} not found in catalogue.")
        return

    with workflow_file.open() as f:
        workflow_yaml = yaml.safe_load(f)
        input_list = workflow.get_inputs(workflow_yaml)
        input_text = yaml.dump({k: '' for k in input_list})
        with open(Path(os.getcwd()) / 'inputs.yml', "w+") as input_file:
            input_file.write(input_text)

def make(environment: Dict[str, str]):
    # TODO: Problem

    click.echo(workflow.make_workflow(environment.keys, environment.values, environment))


'''
Below are deprecated commands. Delete if necessary.



@catalogue.command()
@click.argument("name")
def check(name):
    data = config.catalogue[name]
    assert data
    
    valid = validate_entry(data)
    if not valid:
        click.secho("Sadly something is wrong :(")
    else:
        click.secho("Nice job! Everything looks good.", fg="green")
    


@catalogue.command()
@click.argument("name")
@click.argument("path")
def create(name, path):
    template_path = pkg_resources.resource_filename(
        "recastatlas", "data/templates/helloworld"
    )
    copy_tree(template_path, path)
    recast_file = os.path.join(path, "recast.yml")
    data = string.Template(open(recast_file).read()).safe_substitute(
        name=name, author=getpass.getuser()
    )
    with open(recast_file, "w") as f:
        f.write(data)
    click.secho(
        "New skeleton created at {path}\nRun $(recast catalogue add {path}) to add to the catlogue".format(
            path=path
        )
    )


@catalogue.command()
@click.argument("path")
def add(path):
    if os.path.exists(path) and os.path.isdir(path):
        paths = []
        existing = os.environ.get("RECAST_ATLAS_CATALOGUE")
        if existing:
            paths.append(existing)
        paths.append(path)
        click.secho("export RECAST_ATLAS_CATALOGUE=" + ":".join(paths))
    else:
        raise click.Abort("path {} does not exist or is not a directory".format(path))


@catalogue.command()
def ls():
    fmt = "{0:35}{1:60}{2:20}"
    click.secho(fmt.format("NAME", "DESCRIPTION", "EXAMPLES"))

    for k, v in sorted(config.catalogue.items(), key=lambda x: x[0]):
        click.secho(
            fmt.format(
                k,
                v.get("metadata", default_meta)["short_description"],
                ",".join(list(v.get("example_inputs", {}).keys())),
            )
        )


@catalogue.command()
@click.argument("name")
def describe(name):
    data = config.catalogue[name]

    metadata = data.get("metadata", default_meta)
    toprint = """\

{name:20}
--------------------
description  : {short:20}
author       : {author}
""".format(
        author=metadata["author"], name=name, short=metadata["short_description"]
    )
    click.secho(toprint)


@catalogue.command()
@click.argument("name")
@click.argument("example")
def example(name, example):
    data = config.catalogue[name]
    if not example in data.get("example_inputs", {}):
        click.secho("example not found.")
        return
    click.secho(yaml.dump(data["example_inputs"][example], default_flow_style=False))

'''
