"""Scraper registry — maps scraper IDs to their entry-point functions."""

from src.scrape.time_wheel_calgary import scrape as time_wheel_calgary_scrape
from src.scrape.info_calgary import scrape as info_calgary_scrape
from src.scrape.weather_calgary import scrape as weather_calgary_scrape
from src.scrape.calgary_air_quality import scrape as calgary_air_quality_scrape
from src.scrape.calgary_river_levels import scrape as calgary_river_levels_scrape
from src.scrape.calgary_transit import scrape as calgary_transit_scrape
from src.scrape.calgary_traffic import scrape as calgary_traffic_scrape
from src.scrape.enmax_power import scrape as enmax_power_scrape
from src.scrape.calgary_news import scrape as calgary_news_scrape
from src.scrape.global_events_wire import scrape as global_events_wire_scrape

_REGISTRY: dict[str, callable] = {
    "time_wheel_calgary": time_wheel_calgary_scrape,
    "info_calgary": info_calgary_scrape,
    "weather_calgary": weather_calgary_scrape,
    "calgary_air_quality": calgary_air_quality_scrape,
    "calgary_river_levels": calgary_river_levels_scrape,
    "calgary_transit": calgary_transit_scrape,
    "calgary_traffic": calgary_traffic_scrape,
    "enmax_power": enmax_power_scrape,
    "calgary_news": calgary_news_scrape,
    "global_events_wire": global_events_wire_scrape,
}


def get_scraper(name: str):
    """Return the scrape function for the given scraper ID."""
    if name not in _REGISTRY:
        raise KeyError(f"Unknown scraper: {name!r}. Available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]
