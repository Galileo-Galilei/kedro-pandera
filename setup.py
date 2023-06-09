import pathlib

from setuptools import find_packages, setup

NAME = "kedro_pandera"
HERE = pathlib.Path(__file__).parent


def _parse_requirements(path, encoding="utf-8"):
    with open(path, encoding=encoding) as file_handler:
        requirements = [
            x.strip() for x in file_handler if x.strip() and not x.startswith("-r")
        ]
    return requirements


# get the dependencies and installs
base_requirements = _parse_requirements((HERE / "requirements.txt").as_posix())


# Get the long description from the README file
with open((HERE / "README.md").as_posix(), encoding="utf-8") as file_handler:
    README = file_handler.read()


setup(
    name=NAME,
    version="0.0.1",  # this will be bumped automatically by bump2version
    description="A kedro plugin to use pandera in your kedro projects",
    license="Apache Software License (Apache 2.0)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Galileo-Galilei/kedro-pandera",
    python_requires=">=3.8, <3.11",
    packages=find_packages(exclude=["docs*", "tests*"]),
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=base_requirements,
    extras_require={
        "doc": [
            "sphinx>=4.5.0,<8.0.0",
            "sphinx_rtd_theme>=1.0,<1.3",
            "sphinx-markdown-tables~=0.0.15",
            "sphinx-click>=3.1,<4.5",
            "sphinx_copybutton~=0.5.0",
            "myst-parser>=0.17.2,<1.1.0",
        ],
        "test": [
            "pytest>=7.0.0, <8.0.0",
            "pytest-cov>=4.0.0, <5.0.0",
            "flake8==6.0.0",  # ensure consistency with pre-commit
            "black==23.3.0",  # pin black version because it is not compatible with a pip range (because of non semver version number)
            "isort==5.12.0",  # ensure consistency with pre-commit
        ],
        "dev": [
            "pre-commit>=2.0.0,<4.0.0",
            "jupyter>=1.0.0,<2.0.0",
        ],
    },
    author="Yolan Honoré-Rougé",
    entry_points={
        "kedro.project_commands": [
            "kedro_pandera =  kedro_pandera.framework.cli.cli:commands"
        ],
        # "kedro.hooks": [
        #     "pandera_hook = kedro_pandera.framework.hooks.pandera_hook:pandera_hook",
        # ],
    },
    zip_safe=False,
    keywords="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Kedro",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
)
