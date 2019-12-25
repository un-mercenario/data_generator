import os
from setuptools import setup, find_packages

install_requires = []

setup(
    name="data_generator",
    version="0.0.1",
    author="",
    author_email="",
    description=(""),
    license="MIT",
    keywords=[],
    url="",
    packages=find_packages(),
    package_data={"": ["LICENCE", "requirements.txt", "README.md", "CHANGELOG.md"]},
    include_package_data=True,
    install_requires=install_requires,
)
