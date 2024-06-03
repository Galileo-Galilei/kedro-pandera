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
    version="0.2.2",  # this will be bumped automatically by bump2version
    description="A kedro plugin to use pandera in your kedro projects",
    license="Apache Software License (Apache 2.0)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Galileo-Galilei/kedro-pandera",
    python_requires=">=3.8, <3.12",
    packages=find_packages(exclude=["docs*", "tests*"]),
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=base_requirements,
    extras_require={
        "doc": [
            "sphinx>=4.5.0,<7.3.0",  # https://github.com/kai687/sphinxawesome-theme/issues/1464
            "sphinxawesome-theme",
            "sphinx-docsearch",
            "sphinx-markdown-tables~=0.0.15",
            "sphinx-click>=3.1,<6.0",
            "sphinx_copybutton~=0.5.0",
            # "sphinx-sitemap",
            "sphinx-design",
            "myst-parser>=0.17.2,<2.1.0",
        ],
        "test": [
            "ruff>=0.4.0, <0.5.0",
            "pytest>=7.0.0, <8.0.0",
            "pytest-cov>=4.0.0, <5.0.0",
            "pytest-mock",
            "pre-commit>=2.0.0,<4.0.0",
            "cookiecutter",
            "kedro-datasets",
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
        "kedro.hooks": [
            "pandera_hook = kedro_pandera.framework.hooks.pandera_hook:pandera_hook",
        ],
    },
    zip_safe=False,
    keywords="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Kedro",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
)
