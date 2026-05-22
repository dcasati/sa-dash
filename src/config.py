"""Source configuration for locations and providers."""

LOCATIONS = {
    "calgary": {
        "name": "Calgary",
        "scrapers": [
            "time_wheel_calgary",
            "info_calgary",
            "weather_calgary",
            "calgary_air_quality",
            "calgary_river_levels",
            "calgary_transit",
            "calgary_traffic",
            "enmax_power",
            "calgary_news",
            "global_events_wire",
        ],
    }
}
