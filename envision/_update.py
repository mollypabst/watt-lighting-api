from importlib import resources
from os.path import join

from pandas import DataFrame, concat
from requests import Session
from zeep import Client
from zeep.cache import SqliteCache
from zeep.helpers import serialize_object as serialize
from zeep.transports import Transport

from envision._credentials import REST_URL, WEB_URL, USERNAME, PASSWORD


def update() -> str:
    """Update stored areas in areas.json.

    :return: None
    """
    session = Session()
    session.auth = USERNAME, PASSWORD
    session.verify = False

    # Fetch areas from the Web API.
    web = serialize(
        Client(
            WEB_URL, transport=Transport(session=session, cache=SqliteCache())
        ).service.getBuildingNavigation("Building")
    )

    with resources.path(
            "envision", "areas.json"
    ) as path, open(path, "w") as file:

        # Create a DataFrame from the REST API, and join it with Web API
        DataFrame(
            session.get(
                join(REST_URL, "getAllLocations")
            ).json()["Area_List"],
            dtype="object"
        ).join(concat([
            # Building
            DataFrame([web])
        ] + [
            # Floors
            DataFrame(web["childLocations"]["childLocations"])
        ] + [
            # Rooms
            DataFrame(
                web["childLocations"]["childLocations"]
                [i]["childLocations"]["childLocations"]
            )
            for i, _ in enumerate(web["childLocations"]["childLocations"])
        ]).set_index(keys="name"), how="outer", on="name").reset_index()[
            ["name", "isUserAuthorized", "areaID", "id"]
        ].rename(
            columns={
                "name": "Room Name",
                "isUserAuthorized": "Access",
                "areaID": "REST ID",
                "id": "Web ID"
            }
        ).sort_values(
            ["REST ID", "Web ID"]
        ).to_json(path_or_buf=file, orient="records", indent=4)

    session.close()
    return str(path) + " updated"
