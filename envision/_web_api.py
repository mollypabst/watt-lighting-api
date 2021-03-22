from asyncio import run, gather
from datetime import datetime
from importlib import resources

import httpx
from httpx import ReadTimeout, ConnectTimeout
from pandas import DataFrame, concat, read_json as load
from zeep import AsyncClient
from zeep.cache import SqliteCache
from zeep.helpers import serialize_object as serialize
from zeep.transports import AsyncTransport

from envision._credentials import WEB_URL, USERNAME, PASSWORD


def energy(
        start: datetime, end: datetime, period: str = "Hour"
) -> DataFrame:
    """Efficiently get energy levels for all areas.

    :param start: start of sample
    :param end: end of sample
    :param period: period of time between data points
    :return: Pandas DataFrame object with all area energy levels
    """
    return run(web_interface(
        "Energy", "avgKW", start, end, period
    ))


def occupancy(
        start: datetime, end: datetime, period: str = "Hour"
) -> DataFrame:
    """Efficiently get occupancy levels for all areas.

    :param start: start of sample
    :param end: end of sample
    :param period: period of time between data points
    :return: Pandas DataFrame object with all area occupancy levels
    """
    return run(web_interface(
        "Occupancy", "occupiedPercentage", start, end, period
    ))


# Collect data on a single given areea.
async def get_area(
        area_name: str, label: str, client: AsyncClient, args: dict
) -> DataFrame:
    try:
        response = serialize(await client.service.getMetricReport(args))
        n = len(response["metricReportList"])
        return DataFrame({
            "Time": [args["fromDateTime"]] * n,
            "Web ID": [args["locationID"]] * n,
            "Area Name": [area_name] * n,
            args["metricType"]: [
                time[label]
                for time in response["metricReportList"]
            ]
        })
    except (ReadTimeout, ConnectTimeout):
        print("error")
        return DataFrame({
            "Time": [],
            "Web ID": [],
            "Area Name": [],
            args["metricType"]: []
        })


# Run all areas asynchronously.
async def web_interface(
        metric: str, label: str, start: datetime, end: datetime, period: str
) -> DataFrame:
    async with httpx.AsyncClient(
            verify=False, auth=(USERNAME, PASSWORD)
    ) as a_client:
        with httpx.Client(
                verify=False, auth=(USERNAME, PASSWORD)
        ) as wsdl_client, resources.path(
            "envision", "areas.json"
        ) as path, open(path, "r") as file:
            client = AsyncClient(
                WEB_URL,
                transport=AsyncTransport(
                    client=a_client,
                    wsdl_client=wsdl_client,
                    cache=SqliteCache()
                )
            )
            return concat(await gather(*[
                get_area(
                    area["Room Name"], label, client,
                    {
                        "fromDateTime": start,
                        "toDateTime": end,
                        "period": period,
                        "metricType": metric,
                        "locationID": area["Web ID"]
                    }
                )
                for _, area in load(file).drop_duplicates(
                    #keys="Room Name"
                ).dropna(subset=["Web ID"]).iterrows()
            ]))
