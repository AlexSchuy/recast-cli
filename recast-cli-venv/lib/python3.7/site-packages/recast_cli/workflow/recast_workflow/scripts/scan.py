from ..scripts import workflow

def build_multi(single_wf: dict, multi_params=[]):
    """
    Convert single-step stage workflow to multistep stages

    :param single_wf: workflow represented as dictionary
    :param multi_params: names of parameters that will take multiple inputs
    :return: new multistep workflow dictionary
    """
    params = workflow.get_inputs(single_wf)

    for i in params:
        if i in multi_params:
            params['flatten'] = True

    multi_wf = {'stages': [{
        'dependencies': ['init'],
        'name': 'multi_' + workflow.make_name(single_wf),
        'scheduler': {
            'parameters': params
        },
        'scheduler_type': 'multistep-stage',
        'scatter': {'method': 'zip', 'parameters': ['param_card']},
        'workflow' : single_wf
    }]}
    return multi_wf
