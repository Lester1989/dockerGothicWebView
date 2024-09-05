from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
import pathlib
import app.auth as auth

version = pathlib.Path("pyproject.toml").read_text(encoding="utf-8").splitlines()[2].split("=")[1].strip().strip('"')
print(f"Running version {version}")
app = FastAPI(version=version)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

uploaded_coordinates: list[tuple[float, float]] = []



@app.post("/upload_coordinates", include_in_schema=False)
async def upload_coordinates(coordinates_lat_lon: list[tuple[float, float]], _=Depends(auth.get_bot_key) ):
    uploaded_coordinates.clear()
    uploaded_coordinates.extend(coordinates_lat_lon)
    return Response(status_code=200)


@app.get(
    "/api/gothic_tales_players",
    summary="Get the coordinates of the players in Gothic Tales",
    response_model=list[tuple[float, float]],
)
async def get_coordinates(_=Depends(auth.get_api_key)) -> list[tuple[float, float]]:
    '''
    Returns the coordinates of the players in Gothic Tales from memory.

    If no coordinates have been uploaded since last restart, an empty list is returned. You can fix this by either
    * unlocking the bot with /plz_unlock and the keyfile (only allowed for discord server owner)
    * uploading a new datapoint with /plz_add and your own plz (every discord member can do this if the bot is unlocked)

    '''
    return uploaded_coordinates


@app.get("/standalone/gothic_tales_players", include_in_schema=False)
async def render_template(request: Request):
    print(uploaded_coordinates)
    return templates.TemplateResponse(
        "map.html", {"request": request, "coordinates": uploaded_coordinates}
    )
