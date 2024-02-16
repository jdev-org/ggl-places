from setuptools import setup, find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().split("\n")

setup(
    name="ggl_places",
    version="0.2",
    description="A simple script to read and write geoserver layer",
    author="jdev",
    author_email="",
    url="https://github.com/jdev-org/ggl-places.git",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)