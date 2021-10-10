"""
Setup.py file.
Install once-off with:  "pip install ."
For development:        "pip install -e .[dev]"
"""
import setuptools


#with open("requirements.txt") as f:
#    install_requires = f.read().splitlines()

PROJECT_NAME = "flood_model"

setuptools.setup(
    name=PROJECT_NAME,
    version="0.1",
    author="aklilu_dinkneh",
    author_email="ateklesadik@redcross.nl",
    description="flood trigger model",
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="lib"),
    #install_requires=install_requires,
    extras_require={
        "dev": [  # Place NON-production dependencies in this list - so for DEVELOPMENT ONLY!
            "black",
            "flake8"
        ],
    },
    entry_points={
        'console_scripts': [
            f"run-flood-model = {PROJECT_NAME}.runPipeline:main",
        ]
    }
)
