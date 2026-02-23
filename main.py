import datetime

from fastapi import FastAPI
import asyncio
from fastapi.responses import HTMLResponse
from service import check_new_incidents, html_page

app = FastAPI()

latest_response = []

@app.get("/")
async def root():
    return {"message": "Hello API status checker!"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_incidents())
  
async def monitor_incidents():
    global latest_response
    now = datetime.datetime.now()
    while True:
        response = await check_new_incidents()
        latest_response = response
        cutoff_time = now - datetime.timedelta(days=30)
        latest_response = [r for r in latest_response if datetime.datetime.strptime(r.split(']')[0][1:], "%Y-%m-%dT%H:%M:%SZ") >= cutoff_time]
        await asyncio.sleep(300)  # Check every 60 seconds

@app.get("/status", response_class=HTMLResponse)
async def status():
    content = "<br>".join(latest_response) if latest_response else "No new incidents."
    return html_page(content)
  

            
    

