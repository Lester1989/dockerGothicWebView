from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

uploaded_coordinates: list[tuple[float, float]] = []

secret_key = os.environ.get("SECRET_KEY", None)

@app.post("/upload_coordinates")
async def upload_coordinates(request: Request,coordinates_lat_lon: list[tuple[float, float]]):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {secret_key}":
        return {"message": "Invalid key"}
    uploaded_coordinates.clear()
    uploaded_coordinates.extend(coordinates_lat_lon)
    return {"message": "Coordinates uploaded successfully"}


@app.get("/gothic_tales_coordinates")
async def render_template(request: Request):
    return templates.TemplateResponse(
        "map.html", {"request": request, "coordinates": uploaded_coordinates}
    )
