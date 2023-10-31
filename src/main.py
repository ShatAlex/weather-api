from fastapi import FastAPI

from src.cities.router import router_weathers, router_cities

app = FastAPI(
    title='WeatherAPI',
    description='Микросервис погоды по городам',
    version='1.0.0',
)

origins = [
    "http://localhost:3000",
]

app.include_router(router_weathers)
app.include_router(router_cities)
