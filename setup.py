from pathlib import Path

from setuptools import setup, find_packages

import undetected_playwright

# python setup.py sdist bdist_wheel && python -m twine upload dist/*
setup(
    name="undetected-playwright",
    version=undetected_playwright.__version__,
    keywords=["playwright", "undetected-playwright", "playwright-stealth"],
    packages=find_packages(
        include=["undetected_playwright", "'undetected_playwright'.*", "LICENSE"]
    ),
    package_data={"undetected_playwright": ["js/*.js"]},
    url="https://github.com/QIN2DIM/undetected-playwright",
    license="Apache-2.0 license",
    author="QIN2DIM",
    author_email="yaoqinse@gmail.com",
    description="You know who I am",
    long_description=Path(__file__).parent.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=["playwright"],
    python_requires=">=3.8",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
)
