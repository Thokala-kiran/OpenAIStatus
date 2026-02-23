<<<<<<< HEAD
# OpenAI Status Incident Viewer

A small FastAPI app that fetches incidents, outage, or degradation update data from OpenAI Status and renders it as a simple HTML page.

## What this project does
- Exposes a health route at `/`.
- Exposes `/status` to fetch incidents from:
  - `https://status.openai.com/api/v2/incidents.json`
- Renders incident `name` and `created_at` values in an HTML response.

## Current implementation notes
- File used: `main.py`
- `service.py` is currently empty.
- In the current response format, incidents are displayed under a fixed product label: `OpenAI API`.

## Known limitation (confirmed)
I confirmed (using direct API checks in Postman and AI Tools) that the current OpenAI incidents endpoint does not always include detailed component mapping in a way this app can directly render as per-product component detail for every incident.

Because of that, this project currently shows incident-level details (name + created time) instead of full component-level incident breakdown.


### Controlled polling policy
- Pull incidents from the status API on a schedule.
- Keep incident records for up to **30 days**.
- Delete records older than 30 days during each polling cycle.

Suggested retention cleanup logic:
1. Parse each incident timestamp (for example `created_at`).
2. Compute cutoff time = `now - 30 days`.
3. Remove any stored incident older than cutoff.
4. Keep only recent incidents for display/reporting.

## Webhooks
In a production environment, this polling mechanism could be replaced with:
- Webhook-based automation via services like Pipedream or IFTTT
- Or official webhook subscription if provided by the status provider

## Run locally
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/status`

## API behavior summary
- `GET /` -> JSON welcome message.
- `GET /status` -> HTML page containing recent incident lines in this format:
  - `[created_at] Product: OpenAI API, status : incident_name`

