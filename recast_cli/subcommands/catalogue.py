from typing import Dict

import click
import yaml
import os
from distutils.dir_util import copy_tree
import string

import pkg_resources
import getpass

from ..workflow.recast_workflow.common import utils
from ..workflow.recast_workflow.scripts import catalogue as ctlg
from ..workflow.recast_workflow.scripts import workflow

default_meta = {"author": "unknown", "short_description": "no description"}


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
def combinations(params):
    """
    Returns all valid catalogue combinations for the given analysis.
    """
    # TODO: common_inputs hasn't been implemented yet.
    input_parameters = {}
    for i in params:
        lst = i.split('=')
        if not len(lst) == 2:
            click.secho('Invalid parameters.')
            return
        else:
            input_parameters[lst[0]] = lst[1]

    valid = ctlg.get_valid_combinations(input_parameters)
    fmt = '{0:20}{1:30}'

    for index, combination in enumerate(valid):
        click.secho('-' * 50)
        click.secho(f'Combination {index + 1}:')
        click.secho(fmt.format('STEP', 'NAME'))
        for k, v in combination.items():
            click.secho(fmt.format(k, v))
        click.secho()

    # TODO: error occured when typing in the analysis_id
    click.confirm('Do you want to start the "make" process?', abort=True)

    workflow_index = click.prompt('Please select the combination, or enter 0 to cancel', type=int) - 1
    while not -1 <= workflow_index < len(valid):
        workflow_index = click.prompt('Invalid index. Try again', type=int) - 1

    env = valid[workflow_index]
    steps = []
    names = []
    env_settings = []
    for k, v in env.items():
        steps.append(k)
        names.append(v)
        env_settings.append({})

    workflow_text = yaml.dump(workflow.make_workflow(steps, names, env_settings))
    # TODO: Save this yaml to a file.
    click.secho(workflow_text)


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
