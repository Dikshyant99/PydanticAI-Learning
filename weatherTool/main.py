import httpx
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent,ModelRetry,RunContext
from pydantic import BaseModel,Field
from pydantic_ai.messages import ToolCallPart

load_dotenv()

#Deps: A shared http client instead of memory
@dataclass
class WeatherDeps:
    client: httpx.Client
#Structured Output filled with real data from tools
class CityWeather(BaseModel):
    city:str
    high_c:float = Field (description= "Today's max temperature in °C")
    low_c:float = Field(description="Today's min temperature in °C ")
    rain_chance_percent:int
class TravelAdvice(BaseModel):
    cities:list[CityWeather]
    bring_umbrella:bool
    what_to_wear : str = Field(description="one or two sentence of clothing advice")
    
agent=Agent(
    'anthropic:claude-haiku-4-5',
    deps_type=WeatherDeps,
    output_type=TravelAdvice,
    instructions=(
        'You give travel weather advice. Always use the tools for real data and never '
        'invent numbers. Look up coordinates first, then get the forecast.'
    ),
    
)
#tool 1:  city name-> Coordinates
@agent.tool
def get_coordinates(ctx: RunContext[WeatherDeps], city: str) -> dict:
    "Find latitude and longitude of the city by its name"
    response = ctx.deps.client.get(
        'https://geocoding-api.open-meteo.com/v1/search',
        params={'name': city, 'count': 1},
    )
    response.raise_for_status()
    results = response.json().get('results')

    if not results:
        raise ModelRetry(f"No city named {city} found. Try a different spelling.")

    place = results[0]
    return {
        'name': place['name'],
        'country': place.get('country'),
        'latitude': place['latitude'],
        'longitude': place['longitude'],
    }

#Tool2 coordinates-> Forecast
@agent.tool
def get_forecast(ctx: RunContext[WeatherDeps], latitude: float, longitude: float) -> dict:
    """Get a 3-day forecast: daily max/min temperature (°C) and max rain probability (%).
    The first entry in each list is today."""
    response = ctx.deps.client.get(
        'https://api.open-meteo.com/v1/forecast',
        params={
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
            'timezone': 'auto',
            'forecast_days': 3,
        },
    )
    response.raise_for_status()
    return response.json()['daily']

#Run: The client is opened once and closed automatically

with httpx.Client(timeout=10)as client:
    result=agent.run_sync(
        "I'm traveling from Kathmandu to Pokhara today. Compare the weather and tell me what to pack.",
        deps=WeatherDeps(client=client),

    )
advice=result.output
print('=== Weather ===')
for c in advice.cities:
    print(f'{c.city:<12} {c.low_c:.0f}–{c.high_c:.0f}°C   rain {c.rain_chance_percent}%')
print(f'\nUmbrella? {"Yes" if advice.bring_umbrella else "No"}')
print(f'Wear: {advice.what_to_wear}')

print('\n=== Tool calls ===')
for message in result.all_messages():
    for part in message.parts:
        if isinstance(part, ToolCallPart):
            print(f'-> {part.tool_name}({part.args})')

print(f'\nUsage: {result.usage()}')
    
    
