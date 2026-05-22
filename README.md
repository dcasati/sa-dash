# Calgary Situational Awareness Dashboard

Lightweight dashboard generator providing situational awareness information for Calgary, Alberta.

## Quick start

1. Create a virtualenv and install dependencies:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. Generate Calgary dashboard:
   - `python3 -m src.generate --location calgary`

3. Run a single scraper (for testing):
   - `python3 -m src.generate --scraper weather_calgary`

Outputs are written to `site/`:
- `site/index.html`

## Offline mode

If the network is unavailable, you can render from cached data:
- `python3 -m src.generate --location calgary --offline`

## Data Sources

- Environment Canada (weather)
- City of Calgary Open Data (transit, traffic, river levels, air quality)
- CBC Calgary RSS (news)
- ENMAX (power outages)
- S2 Underground Wire (global events)

## Secrets

Put keys in a **`.env`** file at the repo root (see `.env.example`). When you run `python3 -m src.generate ...`, that file is loaded automatically via `python-dotenv`.

## Notes

- Scrapers prioritize resilience. If a source fails, the last known cache is used and the output will show when it was last retrieved.
- Source URLs are centralized in `src/config.py`.
