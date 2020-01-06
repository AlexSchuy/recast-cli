from setuptools import setup, find_packages

setup(
    name='recast_cli',
    version='0.0.2',
    install_requires=[
        'Click',
        'PyYAML',
        'requests',
        'yadage'
    ],
    entry_points='''
        [console_scripts]
        recast-cli=recast_cli.cli:recast_cli
    ''',
    packages=find_packages()
)
