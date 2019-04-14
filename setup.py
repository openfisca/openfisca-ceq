#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='OpenFisca-CEQ',
    version='0.2.4',
    author='OpenFisca Team',
    author_email='contact@openfisca.fr',
    description=u'OpenFisca tax and benefit system for CEQ',
    keywords='benefit microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/openfisca/openfisca-ceq',
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >=25.2.2,<31.0',
        ],
    extras_require = {
        'dev': [
            "autopep8 ==1.4.4",
            "flake8 >= 3.5.0, < 3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            "pytest < 5.0",
            "requests >= 2.8",
            "yamllint >=1.11.1,<1.16",
            ],
        },
    packages=find_packages(),
    )
