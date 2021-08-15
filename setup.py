from setuptools import setup, find_namespace_packages
from os import path
from io import open

script_directory = path.abspath(path.dirname(__file__))

with open(path.join(script_directory, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

with open(path.join(script_directory, 'requirements.txt'), encoding='utf-8') as f:
    install_requirements = f.readlines()

setup(
    name="pikamon-py",
    version="1.0.0",
    description="A Pokemon Discord bot inspired by the late Pokecord.",
    long_description=readme,
    long_description_content_type="test/markdown",
    url="",
    author="David Rocker",
    author_email="",
    classifiers=[
        "Private :: Do not upload to pypi server"
    ],
    keywords="Pikamon",
    packages=find_namespace_packages(include=["pikamon.*"], exclude=["tests"]),
    python_requires=">=3.9",
    install_requires=install_requirements,
    # entry_points={
    #    "console_scripts": ["pikamon=pikamon:main"]
    # },
    project_url={
        "Bug Reports": "https://github.com/dlrocker/pikamon-py",
        "Support": "https://github.com/dlrocker/pikamon-py"
    }
)
