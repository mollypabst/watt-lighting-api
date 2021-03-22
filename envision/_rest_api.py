from asyncio import run, gather
from importlib import resources
from os.path import join

from httpx import AsyncClient
from pandas import DataFrame, Series, read_json as load

from envision._credentials import REST_URL, USERNAME, PASSWORD


# Collect lighting data on a single given area.
async def get_area(area: Series, client: AsyncClient) -> dict:
    response = (await client.get(
        url=join(REST_URL, f"getCurrentStatus/{int(area['REST ID'])}")
    )).json()

    # Return a dictionary where keys are the respective column headers.
    try:
        return {
            # Each key: value pair is a column in the final DataFrame
            "Area Name": area["Room Name"],
            "Area ID": area["REST ID"],
            "Area Level": response["areaLevel"],
            **{
                key + 1: value["luminaireLevel"]
                for key, value in enumerate(response["luminaireLevels"])
            }
        }

    # This will happen if data contains no luminaire levels.
    except KeyError:
        return {
            "Area Name": area["Room Name"],
            "Area ID": area["REST ID"],
            "Area Level": response["areaLevel"]
        }


# Run all areas asynchronously.
async def rest_interface() -> DataFrame:
    async with AsyncClient(auth=(USERNAME, PASSWORD), verify=False) as client:
        with resources.path(
                package="envision", resource="areas.json"
        ) as path, open(path, "r") as file:
            # Iterate through every area in areas.json, fetching lighting data.
            return DataFrame(await gather(*[
                get_area(area, client)
                for _, area in load(path_or_buf=file).drop_duplicates(
                    subset="Room Name"
                ).dropna(subset=["REST ID"]).iterrows()
                if area["Access"]
            ]), dtype="int").set_index(keys="Area ID").sort_index()


def lighting() -> DataFrame:
    """Efficiently get lighting levels for all areas.

    :return: Pandas DataFrame object with all area lighting levels
    """
    return run(rest_interface())
