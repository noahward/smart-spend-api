from setuptools import setup, find_packages

setup(
    name="SmartSpend",
    description="setup.py for SmartSpend",
    version="v2022.05.31",
    packages=find_packages(include=["api", "api.*"]),
    author="Noah Ward",
    install_requires=[],
)
