from setuptools import setup, find_packages

setup(
    name="rcph",
    version="2.0.0",
    packages= find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "rcph = rcph.main:main",  # The entry point for the CLI tool
        ],
    },
)
