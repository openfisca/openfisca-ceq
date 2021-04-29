#! /usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='OpenFisca-CEQ',
    version='0.4.1',
    author='OpenFisca Team',
    author_email='contact@openfisca.fr',
    description=u'OpenFisca tax and benefit system for CEQ',
    keywords='benefit microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/openfisca/openfisca-ceq',
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Survey-Manager >=0.40.1,<1.0',
        'OpenFisca-Core >=34.4.2,<36.0',
        'matplotlib >=3.2.1,<4.0',
        'pandas >= 0.24.1',
        'python-slugify',
        'scipy',
        'xlrd >= 1.0.0',
        'xlsxwriter',
        'xlwt >= 1.0.0',
        ],
    extras_require = {
        'dev': [
            "autopep8 ==1.5.6",
            "flake8 >=3.8.0,<3.10.0",
            "flake8-print",
            "papermill",
            'pdbpp',
            "pytest >= 5.0.0, < 7.0.0",
            "requests >= 2.8",
            "yamllint >=1.11.1,<1.27",
            ],
        },
    packages=find_packages(),
    )
