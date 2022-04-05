#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import pathlib

base_path = pathlib.Path(__file__).parent.absolute()

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=8.0', 
    'requests', 
    'click_log', 
    'Jinja2',
]

test_requirements = [ 'coverage', 'nose2' ]

setup(
    author="Heinz Axelsson-Ekker",
    author_email='heinz.ekker@vbcf.ac.at',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Generate dataclasses from Swagger/OpenAPI2 defs",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='swagspotta',
    name='swagspotta',
    packages=find_packages(include=['swagspotta', 'swagspotta.*']),
    package_data={'swagspotta': ['templates/*/*']},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://ngs.vbcf.ac.at/repo/software/swagspotta.git',
    version='0.0.4',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'spotta = swagspotta.cli:cli',
        ],
    },
)
