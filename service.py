import httpx


STATUS_URL = "https://status.openai.com/api/v2/incidents.json"

def html_page(content: str) -> str:
    return f"""
    <html>
        <head>
            <title>OpenAI Status</title>
        </head>
      
      </head>
      <body>
        <header>
          <h1>OpenAI Status</h1>
          <p>Incident details</p>
          <hr />
        </header>
        <main>
          <section>
            {content}
          </section>
        </main>
        <footer>
          <hr />
          <small>Generated from status incident data</small>
        </footer>
      </body>
    </html>
    """

last_incident_ids = set()

async def check_new_incidents():
    global last_incident_ids
    
    async with httpx.AsyncClient() as client:
        response = await client.get(STATUS_URL)
        data = response.json()
    incidents = data.get("incidents", [])
    current_ids = {incident["id"] for incident in incidents}

    new_ids = current_ids - last_incident_ids

    last_incident_ids = current_ids

    OpenAPI_status = []
    product_names = "OpenAI API"
    for ids in new_ids:
        incident = next((i for i in incidents if i["id"] == ids), None)
        if incident:
            name = incident.get("name", "No name")
            created_at = incident.get("created_at", "No date")
            OpenAPI_status.append(f"[{created_at}] Product: {product_names}, status : {name}")
    return OpenAPI_status
