from importlib import resources
from json import load
from os.path import join

# Read from the file.
with resources.path("envision", "credentials.json") as path:
    with open(path, "r") as file:
        credentials = load(file)

# Build the URLs.
REST_URL = join(
    "https://" + credentials["Server"], credentials["REST"]
)
WEB_URL = join(
    "https://" + credentials["Server"], credentials["Web"] + "?WSDL"
)

USERNAME = credentials["Username"]
PASSWORD = credentials["Password"]
