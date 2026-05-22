"""Source configuration for locations and providers."""

LOCATIONS = {
    "calgary": {
        "name": "Calgary",
        "scrapers": [
            "info_calgary",
            "weather_calgary",
            "calgary_air_quality",
            "calgary_river_levels",
            "propagation_calgary",
            "calgary_transit",
            "calgary_traffic",
            "enmax_power",
            "calgary_emergency",
            "calgary_news",
            "cbc_canada",
            "cbc_world",
            "global_events_wire",
        ],
    }
}
