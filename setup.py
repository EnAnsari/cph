from setuptools import setup, find_packages
import os

DATA_FOLDER = 'data'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# create data address file
with open(os.path.join('rcph', 'config', 'data.py'), 'w') as file:
    data_path = os.path.join(os.getcwd(), DATA_FOLDER).replace('\\', '/')
    file.write(f"DATA_ADDRESS = \'{data_path}\'")

setup(
    name="rcph",
    version="2.0.0",
    author="Rahmat Ansari",
    author_email="rahmat2022a@gmail.com",
    license="MIT License",
    description="A competitive programming helper tool.",
    long_description=long_description,  # Detailed description
    long_description_content_type="text/markdown",  # Content type of the long description
    url="https://github.com/EnAnsari/cph",  # Project's URL (GitHub, etc.)
    classifiers=[  # Metadata classifiers for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
    ],
    packages= find_packages(),
    install_requires=[
        'prompt_toolkit',
        'tqdm',
        'selenium',
        'beautifulsoup4',
        # Add other dependencies if needed
    ],
    python_requires='>=3.7',  # Specify the minimum Python version
    project_urls={  # Additional project links
        "mini judgement": "https://github.com/ctrl-alt-Defeat-icpc/mini-judge",
        "test case adder": "https://github.com/ctrl-alt-Defeat-icpc/mini-tca",
    },
    entry_points={
        "console_scripts": [
            "rcph = rcph.main:main",  # The entry point for the CLI tool
        ],
    }
)