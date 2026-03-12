import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/pathways>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = "pathways/VERSION"
print(os.path.join(os.path.dirname(__file__), version_path))
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/pathways"
setup(
    name="pathways",
    version=VERSION,
    packages=["pathways"],
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        "django~=4.2",
        "UW-Django-SAML2~=1.8",
        'lxml==4.9.4',
        "whoosh~=2.7",
        'xmlsec==1.3.13',
        'azure-storage-blob~=12.25',
    ],
    license="Apache License, Version 2.0",
    description="A tool for visually displaying UW course prerequisites",
    long_description=README,
    url=url,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
