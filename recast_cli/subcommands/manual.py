import click
import yaml
import os
from distutils.dir_util import copy_tree
from pathlib import Path

import pkg_resources

from ..workflow.recast_workflow.scripts import catalogue as ctlg
from ..workflow.recast_workflow.scripts import workflow

@click.group(help="Creating Workflows without full RECAST Interface ")
def manual():
    pass

@manual.command()
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
    save_dir = Path(os.getcwd())
    save_file = save_dir / ('-'.join(names) + ".yml")
    with open(save_file, 'w+') as f:
        f.write(workflow_text)

    click.secho(f"Workflow saved to {save_file}")

    # create runnable directory
    click.confirm("Get runnable yadage directory?", abort=True)
    ctx.invoke(save, workflow_file=save_file)

    # click.secho(workflow_text)


@manual.command()
@click.argument('workflow_file', nargs=1)
def save(workflow_file: Path):
    """
    Create runnable yadage directory given path to workflow yaml
    """
    workflow_file = Path(os.path.abspath(workflow_file))
    save_dir = Path(os.path.abspath(os.path.join(workflow_file, '..')))
    save_dir /= Path(os.path.basename(workflow_file).rstrip(".yml"))
    template = Path(pkg_resources.resource_filename("recast_cli", "data/templates/yadage_dir"))

    if save_dir.exists():
        click.secho("Workflow folder already saved with that name. Rename file and try again.")
        return

    # Create directory
    try:
        os.mkdir(save_dir)
        copy_tree(str(template), str(save_dir))
        os.rename(workflow_file, save_dir / "workflows" / "workflow.yml")
    except FileNotFoundError:
        raise FileNotFoundError("Workflow file does not exist.")

    click.secho(f"Made yadage directory at {save_dir} using {workflow_file}")


@manual.command()
@click.argument('workflow_file', nargs=1)
def get_inputs(workflow_file: Path):
    """
    Generates input.yml file that contains all input required to run the given workflow.
    """
    workflow_file = Path(os.path.abspath(workflow_file))
    with workflow_file.open() as f:
        workflow_yaml = yaml.safe_load(f)
        input_list = workflow.get_inputs(workflow_yaml)
        input_text = yaml.dump({k: '' for k in input_list})
        with open(Path(os.getcwd()) / 'inputs.yml', "w+") as input_file:
            input_file.write(input_text)
