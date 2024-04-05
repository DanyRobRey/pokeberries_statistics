# from fastapi import Depends
from dotenv import load_dotenv
from fastapi import HTTPException, status
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import asyncio
import httpx
import os
import statistics
from schemas.schema_poker_berry import PokerBerrysStats

load_dotenv()
poke_api_berries = os.getenv("POKE_API_BERRIES")
total_count_berries = os.getenv("TOTAL_COUNT_BERRIES")


async def get_berry(berry: str) -> dict:
    """
    Retrieve berry information from the Poke API.

    Args:
        berry (str): The name of the berry to retrieve.

    Returns:
        dict: JSON data containing information about the berry.

    Raises:
        HTTPException: If there is an error accessing the Poke API,
            with status code 500 (Internal Server Error).
    """
    async with httpx.AsyncClient() as client:
        berry = await client.get(poke_api_berries + berry)
    if berry.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Poke API Error"
        )

    return berry.json()


async def get_berries(offset: int = 0, limit: int = total_count_berries) -> dict:
    """
    Retrieve all berries information from the Poke API.

    Args:
        offset (int, optional): The index to start retrieving berries from. Default is 0.
        limit (int, optional): The maximum number of berries to retrieve. Default is total_count_berries.

    Returns:
        dict: JSON data containing information about the berries.

    Raises:
        HTTPException: If there is an error accessing the Poke API,
            with status code 500 (Internal Server Error).
    """
    async with httpx.AsyncClient() as client:
        params = {"offset": offset, "limit": limit}
        berries = await client.get(poke_api_berries, params=params)
    if berries.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Poke API Error"
        )

    return berries.json()


async def get_berries_statistics():
    """
    Retrieves statistics of berries from the Poke API.

    Returns:
        dict: A dictionary containing statistics about the berries:
            - 'berries_names' (list): Names of the retrieved berries.
            - 'min_growth_time' (str): Minimum growth time among the retrieved berries.
            - 'median_growth_time' (str): Median growth time among the retrieved berries.
            - 'max_growth_time' (str): Maximum growth time among the retrieved berries.
            - 'variance_growth_time' (str): Variance of growth times among the retrieved berries.
            - 'mean_growth_time' (str): Mean growth time among the retrieved berries.
            - 'frequency_growth_time' (str): Most frequent growth time among the retrieved berries.

    Raises:
        HTTPException: If there is an error accessing the Poke API,
            with status code 500 (Internal Server Error).
    """
    try:
        berries_names = []
        berries_growth_times = []
        berries = await get_berries()

        get_berries_tasks = [
            get_berry(berry.get("name", "")) for berry in berries.get("results", [])
        ]
        berry_stats = await asyncio.gather(*get_berries_tasks)

        for berry_stat in berry_stats:
            berry_name = berry_stat.get("name", "")
            berry_growth_time = berry_stat.get("growth_time", 0)
            berries_names.append(berry_name)
            berries_growth_times.append(berry_growth_time)

        berries_stats = {
            "berries_names": berries_names,
            "min_growth_time": f"{min(berries_growth_times)} hours",
            "median_growth_time": f"{np.median(berries_growth_times)} hours",
            "max_growth_time": f"{max(berries_growth_times)} hours",
            "variance_growth_time": f"{round(np.var(berries_growth_times), 2)} hours",
            "mean_growth_time": f"{round(np.mean(berries_growth_times), 2)} hours",
            "frequency_growth_time": f"{statistics.mode(berries_growth_times)} hours",
        }
        poker_berries_stats = PokerBerrysStats(**berries_stats)
    except HTTPException as e:
        raise

    return poker_berries_stats, berries_growth_times


async def get_berries_statistics_plot():
    """
    Retrieve statistics of Pokemon berries and generate a combined histogram and boxplot plot.

    Returns:
    -------
    io.BytesIO:
        A BytesIO object containing the generated plot image.
    """
    try:
        poker_berrys_stats, berries_growth_times = await get_berries_statistics()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 10))

        ax1.hist(berries_growth_times, bins=10, color="blue", edgecolor="black")
        ax1.set_title("Histogram and Boxplot of Pokemon Berry Growth Times")
        ax1.set_xlabel("Growth Times (Hours)")
        ax1.set_ylabel("Frequency")

        ax2.boxplot(berries_growth_times)
        ax2.set_ylabel("Growth Times (Hours)")

        plt.tight_layout()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format="png")
        img_buffer.seek(0)
    except HTTPException as e:
        raise

    return img_buffer
