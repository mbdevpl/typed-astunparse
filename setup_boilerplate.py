"""Below code is generic boilerplate and normally should not be changed."""

import importlib
import pathlib
import shutil
import sys
import typing as t

import setuptools

__updated__ = "2017-08-23"

HERE = pathlib.Path(__file__).resolve().parent

SRC_DIR = '.'
"""Directory with source code, relative to the setup.py file location."""


def setup():
    """Implement this when using this boilerplate."""
    raise NotImplementedError()


def clean(build_directory_name: str = 'build') -> None:
    """Recursively delete build directory (by default "build") if it exists."""
    build_directory_path = HERE.joinpath(build_directory_name)
    if build_directory_path.is_dir():
        shutil.rmtree(str(build_directory_path))


def find_version(
        package_name: str, version_module_name: str = '_version',
        version_variable_name: str = 'VERSION') -> str:
    """Simulate behaviour of "from package_name._version import VERSION", and return VERSION."""
    version_module = importlib.import_module(
        '{}.{}'.format(package_name.replace('-', '_'), version_module_name))
    return getattr(version_module, version_variable_name)


def find_packages() -> t.List[str]:
    """Find packages to pack."""
    exclude = ['test', 'test.*'] if ('bdist_wheel' in sys.argv or 'bdist' in sys.argv) else []
    packages_list = setuptools.find_packages(SRC_DIR, exclude=exclude)
    return packages_list


def parse_readme(readme_path: str = 'README.rst', encoding: str = 'utf-8') -> str:
    """Read contents of readme file (by default "README.rst") and return them."""
    with open(str(HERE.joinpath(readme_path)), encoding=encoding) as readme_file:
        desc = readme_file.read()
    return desc


def parse_requirements(
        requirements_path: str = 'requirements.txt') -> t.List[str]:
    """Read contents of requirements.txt file and return data from its relevant lines.

    Only non-empty and non-comment lines are relevant.
    """
    requirements = []
    with open(str(HERE.joinpath(requirements_path))) as reqs_file:
        for requirement in [line.strip() for line in reqs_file.read().splitlines()]:
            if not requirement or requirement.startswith('#'):
                continue
            requirements.append(requirement)
    return requirements


def find_required_python_version(
        classifiers: t.Sequence[str], ver_prefix: str = 'Programming Language :: Python :: ',
        only_suffix: str = ' :: Only') -> str:
    """Determine the minimum required Python version."""
    versions = [ver.replace(ver_prefix, '') for ver in classifiers if ver.startswith(ver_prefix)]
    versions_min = [ver for ver in versions if not ver.endswith(only_suffix)]
    versions_only = [ver.replace(only_suffix, '') for ver in versions if ver.endswith(only_suffix)]
    versions_min = [tuple([int(_) for _ in ver.split('.')]) for ver in versions_min]
    versions_only = [tuple([int(_) for _ in ver.split('.')]) for ver in versions_only]
    if len(versions_only) > 1:
        raise ValueError(
            'more than one "{}" version encountered in {}'.format(only_suffix, versions_only))
    only_version = None
    if len(versions_only) == 1:
        only_version = versions_only[0]
        for version in versions_min:
            if version[:len(only_version)] != only_version:
                raise ValueError(
                    'the "{}" version {} is inconsistent with version {}'
                    .format(only_suffix, only_version, version))
    min_supported_version = None
    for version in versions_min:
        if min_supported_version is None or \
                (len(version) >= len(min_supported_version) and version < min_supported_version):
            min_supported_version = version
    if min_supported_version is None:
        if only_version is not None:
            return '.'.join([str(_) for _ in only_version])
    else:
        return '>=' + '.'.join([str(_) for _ in min_supported_version])
    return None


def main() -> None:
    """Call this when using this boilerplate."""
    clean()
    setup()
