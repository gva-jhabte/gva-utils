from setuptools import setup, find_packages  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='gva.utils',
   version='0.1.52',
   description='GVA Data Libraries',
   long_description=long_description,
   long_description_content_type="text/markdown",
   maintainer='The GVA Engineering Team',
   packages=find_packages(include=['gva', 'gva.*']),
   url="https://github.com/gva-jhabte/gva-utils",
   install_requires=[
        'ujson',
        'networkx'
   ]
)
