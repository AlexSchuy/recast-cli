import click
import yaml
import os
from distutils.dir_util import copy_tree
import string

import pkg_resources
import getpass

from ..config import config
from ..workflow.recast_workflow.common import utils
from ..workflow.recast_workflow.scripts import catalogue as ctlg

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
def combinations():
    """
    Returns all valid catalogue combinations for the given analysis.
    """
    valid = ctlg.get_valid_combinations({
        'analysis_id': 1609448
    })
    click.echo(valid)


'''
Below are deprecated commands. Delete if necessary.
'''


@catalogue.command()
@click.argument("name")
def check(name):
    data = config.catalogue[name]
    assert data
    '''
    valid = validate_entry(data)
    if not valid:
        click.secho("Sadly something is wrong :(")
    else:
        click.secho("Nice job! Everything looks good.", fg="green")
    '''


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
