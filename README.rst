Recast CLI
===============

|build-status| |docs| |coverage|

Purpose
-------
Command-line interface for the recast project.

.. |build-status| image:: https://travis-ci.org/recast-hep/recast-cli.svg?branch=master
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/recast-hep/recast-cli
    
.. |docs| image:: https://readthedocs.org/projects/recast-cli/badge/?version=latest
    :alt: documentation status
    :scale: 100%
    :target: https://recast-cli.readthedocs.io/en/latest/?badge=latest


.. |coverage| image:: https://codecov.io/gh/recast-hep/recast-cli/branch/master/graph/badge.svg
    :alt: code coverage
    :scale: 100%
    :target: https://codecov.io/gh/recast-hep/recast-cli
    
Before Development
------------------
1. Go through `this <https://smeehan12.github.io/2019-08-12-dmatlhc-tutorial/index.html>`_ tutorial. You will need to have Docker installed on you computer before you begin. In the tutorial, you run madgraph+pythia, rivet, and contur on one docker image.

2. Git clone `recast-workflow <https://github.com/recast-hep/recast-workflow/tree/dev>`_ (specifically the dev branch) using ``git clone https://github.com/recast-hep/recast-workflow.git --branch dev --single-branch``. You will need to install `pipenv <https://pypi.org/project/pipenv/>`_ and run ``source /recast_workflow/scripts/setup.sh``. This will add recast-workflow/recast_workflow to your PYTHONPATH enviromental variable. Enter pipenv using ``pipenv shell`` and run ``pytest``. Most of the tests should pass.

   One of the pacakges `jq <https://pypi.org/project/jq/>`_ requires a few programs to be installed. On mac, you can install each program seperately using homebrew.

3. Now, clone recast-cli (the subrepository workflow will not be included and that is ok). You will need to move recast-workflow into it and rename it to workflow by running ``mv -r recast-workflow recast-cli/recast_cli/workflow``.
