# TODO: Implement this function.
# You must use the requests library to get the public holidays for the given year.
# The url is public_holidays_url/{year}/BR.
# You must delete the columns "types" and "counties" from the dataframe.
# You must convert the "date" column to datetime.
# You must raise a SystemExit if the request fails. Research the raise_for_status
# method from the requests library.

from typing import Dict

import requests
from pandas import DataFrame, read_csv, read_json, to_datetime
from pathlib import Path


def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    url = f"{public_holidays_url}/{year}/BR"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise SystemExit(exc)

    df = read_json(response.text)
    df = df.drop(columns=["types", "counties"])
    df["date"] = to_datetime(df["date"])

    return df


def extract(
    csv_folder: str,
    csv_table_mapping: Dict[str, str],
    public_holidays_url: str,
) -> Dict[str, DataFrame]:

    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    holidays = get_public_holidays(public_holidays_url, "2017")
    dataframes["public_holidays"] = holidays

    return dataframes
