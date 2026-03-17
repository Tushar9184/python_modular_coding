from setuptools import setup, find_packages
from typing import List
HYPEN_E_DOT = "-e ."
get_requirements = lambda: [req.replace("\n", "") for req in open("requirements.txt").readlines() if req.strip() and req != HYPEN_E_DOT]
setup(
    name="python_modular_coding",
    version="0.0.1",
    author="Your Name",
    author_email="<EMAIL_ADDRESS>",
    description="A modular coding project structure in Python",
    packages=find_packages(),
    install_requires=get_requirements(),
)