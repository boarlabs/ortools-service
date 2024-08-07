
from setuptools import setup, find_packages


with open("requirements.txt", mode="r") as file_handler:
    REQUIREMENTS = file_handler.readlines()


setup(
    name="optclient",
    version="0.0.1",
    description="Energy Optimization Utils",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    license="Proprietary",
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.9"
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=REQUIREMENTS
)