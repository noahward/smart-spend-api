from setuptools import setup, find_packages

setup(
    name="app-name",
    description="setup.py for app",
    version="v2022.01.15",
    packages=find_packages(include=["api", "api.*"]),
    author="Noah Ward",
    install_requires=[],
)
