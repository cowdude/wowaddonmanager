from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wowaddonmanager",
    version="0.1.0",
    description="A minimalistic World of Warcraft addon manager",  # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cowdude/wowaddonmanager",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.6",
    install_requires=[
        "docopt>=0.6.2",
        "requests_html==0.10.0",
        "requests>=2.21.0",
        "PyYAML>=5.1.1",
    ],
)
