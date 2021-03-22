from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="Watt-Lighting-API",
    version="3.0.0",
    author="Molly Pabst",
    author_email="mepabst@g.clemson.edu",
    description="An efficient package for "
                "retrieving lighting data from the Watt center.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.clemson.edu/watt/watt-lighting-api/Test",
    packages=find_packages(),
    package_data={"envision": ["*.json"]},
    install_requires=[
        "pandas",
        "zeep",
        "httpx"
    ]
)
