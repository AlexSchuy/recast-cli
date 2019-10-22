from setuptools import setup, find_packages

setup(
    name='recast_cli',
    version='0.0.1',
    install_requires=[
        'Click', 'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        recast-cli=recast_cli.cli:recast_cli
    ''',
)
