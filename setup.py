# Copyright 2016-2017  Mateusz Bysiek  http://mbdev.pl/
# This file is part of typed-astunparse.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is setup.py file for typed-astunparse."""

import importlib
import os
import shutil
import sys
import typing as t

import setuptools

_SRC_DIR = '.'
"""Set directory with source code, relative to the setup.py file location."""

def setup() -> None:
    """Run setuptools.setup() with correct arguments.

    List of valid project classifiers: https://pypi.python.org/pypi?:action=list_classifiers

    The extras_require is a dictionary which might have the following key-value pairs:
    'some_feature': ['requirement1', 'requirement2'],

    The entry_points is a dictionary which might have the following key-value pair:
    'console_scripts': ['script_name = package.subpackage:function']
    """
    name = 'typed-astunparse'
    version = find_version(name.replace('-', '_'))
    description = 'typed-astunparse is to typed-ast as astunparse is to ast'
    url = 'http://mbdev.pl/'
    download_url = 'https://github.com/mbdevpl/typed-astunparse'
    author = 'Mateusz Bysiek'
    author_email = 'mb@mbdev.pl'
    license_str = 'Apache License 2.0'
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Utilities'
        ]
    keywords = ['ast', 'unparsing', 'pretty printing']
    extras_require = {}
    entry_points = {}
    test_suite = 'test'

    setuptools.setup(
        name=name, version=version, description=description,
        long_description=parse_readme(), url=url, download_url=download_url,
        author=author, author_email=author_email,
        maintainer=author, maintainer_email=author_email,
        license=license_str, classifiers=classifiers, keywords=keywords,
        packages=find_packages(), package_dir={'': _SRC_DIR},
        install_requires=parse_requirements(), extras_require=extras_require,
        entry_points=entry_points, test_suite=test_suite
        )

# below code is generic boilerplate and normally should not be changed

_HERE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def clean(build_directory_name: str='build') -> None:
    """Recursively delete build directory (by default "build") if it exists."""
    build_directory_path = os.path.join(_HERE, build_directory_name)
    if os.path.isdir(build_directory_path):
        shutil.rmtree(build_directory_path)

def find_version(
        package_name: str, version_module_name: str='_version',
        version_variable_name: str='VERSION') -> str:
    """Simulate behaviour of "from package_name._version import VERSION", and return VERSION."""
    version_module = importlib.import_module('{}.{}'.format(package_name, version_module_name))
    return getattr(version_module, version_variable_name)

def find_packages() -> t.List[str]:
    """Find packages to pack."""
    exclude = ['test', 'test.*'] if 'bdist_wheel' in sys.argv else []
    packages_list = setuptools.find_packages(_SRC_DIR, exclude=exclude)
    return packages_list

def parse_readme(readme_path: str='README.rst', encoding: str='utf-8') -> str:
    """Read contents of readme file (by default "README.rst") and return them."""
    with open(os.path.join(_HERE, readme_path), encoding=encoding) as readme_file:
        desc = readme_file.read()
    return desc

def parse_requirements(
        requirements_path: str='requirements.txt') -> t.List[str]:
    """Read contents of requirements.txt file and return data from its relevant lines.

    Only non-empty and non-comment lines are relevant.
    """
    requirements = []
    with open(os.path.join(_HERE, requirements_path)) as reqs_file:
        for requirement in [line.strip() for line in reqs_file.read().splitlines()]:
            if not requirement or requirement.startswith('#'):
                continue
            requirements.append(requirement)

    return requirements

def main() -> None:
    clean()
    setup()

if __name__ == '__main__':
    main()
