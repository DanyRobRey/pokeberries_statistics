from pydantic import BaseModel


class PokerBerrysStats(BaseModel):
    """Model representing a Poker Berry Stats Response."""

    berries_names: list
    min_growth_time: str = ""
    median_growth_time: str = ""
    max_growth_time: str = ""
    variance_growth_time: str = ""
    mean_growth_time: str = ""
    frequency_growth_time: str = ""
