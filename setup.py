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

import setuptools

import setup_boilerplate


def setup() -> None:
    """Run setuptools.setup() with correct arguments.

    List of valid project classifiers: https://pypi.python.org/pypi?:action=list_classifiers

    The extras_require is a dictionary which might have the following key-value pairs:
    'some_feature': ['requirement1', 'requirement2'],

    The entry_points is a dictionary which might have the following key-value pair:
    'console_scripts': ['script_name = package.subpackage:function']
    """
    name = 'typed-astunparse'
    description = 'typed-astunparse is to typed-ast as astunparse is to ast'
    url = 'https://mbdevpl.github.io/'
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
    package_data = {}
    exclude_package_data = {}
    extras_require = {}
    entry_points = {}
    test_suite = 'test'

    setuptools.setup(
        name=name, version=setup_boilerplate.find_version(name), description=description,
        long_description=setup_boilerplate.parse_readme(), url=url, download_url=download_url,
        author=author, author_email=author_email,
        maintainer=author, maintainer_email=author_email,
        license=license_str, classifiers=classifiers, keywords=keywords,
        packages=setup_boilerplate.find_packages(), package_dir={'': setup_boilerplate.SRC_DIR},
        include_package_data=True,
        package_data=package_data, exclude_package_data=exclude_package_data,
        install_requires=setup_boilerplate.parse_requirements(), extras_require=extras_require,
        entry_points=entry_points, test_suite=test_suite
        )


if __name__ == '__main__':
    setup_boilerplate.SRC_DIR = '.'
    setup_boilerplate.setup = setup
    setup_boilerplate.main()
