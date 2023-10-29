from datetime import datetime
import json

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.cities.models import City, Weather
from sqlalchemy import insert, select, desc, and_
from sqlalchemy.sql.functions import func
from src.cities.schemas import Payload

router_weathers = APIRouter(
    prefix='/weathers',
    tags=['Weather']
)

router_cities = APIRouter(
    prefix='/cities',
    tags=['Cities']
)

router_tmp = APIRouter(
    prefix='/tmp',
    tags=['Tmp']
)


@router_weathers.post('/{city}')
async def add_city(city: str, session: AsyncSession = Depends(get_async_session)):
    """ Эндпоинт добавления нового города в БД """
    with open('src/parser/cities_id.json') as json_file:
        data = json.load(json_file)

        cities = {city['name']:city['id'] for city in data}
        
        if city not in cities:
            return {
                "status":"bad request"
            }

    stmt = insert(City).values({"city_name": city})
    await session.execute(stmt)
    await session.commit()

    return {
        "status": "ok"
    }


@router_weathers.get('/')
async def get_last_weathers(search: str = "", session: AsyncSession = Depends(get_async_session)):
    """ Эндпоинт получения всех городов с последней записанной температурой """
    t = select(
        (func.row_number().over(partition_by=City.city_name, order_by=desc(Weather.date))).label("rn"),
        City.city_name,
        Weather.date,
        Weather.temperature
    ).select_from(City).join(Weather)
    query = select(t.c.city_name, t.c.temperature).where(and_(t.c.rn == 1, t.c.city_name.contains(search)))

    result = await session.execute(query)
    data = []
    for item in result.all():
        data.append({'city_name': item[0], 'temperature': item[1]})

    return {
        'status': 'success',
        'data': data,
        'details': None
    }


@router_weathers.get('/all_by_city')
async def get_average(city: str, date1: str , date2: str, session: AsyncSession = Depends(get_async_session)):
    """ Эндпоинт для получения всех данных и средних значений за указанный период """
    left_date = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    right_date = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

    all = select(Weather).join(City).where(
        and_(City.city_name == city, left_date <= Weather.date, Weather.date <= right_date))
    result = await session.execute(all)
    all_data = []
    for item in result.all():
        all_data.append(item[0].__dict__)

    avg = select(func.avg(Weather.temperature), func.avg(Weather.pressure), func.avg(Weather.wind)).join(City).group_by(City.city_name).where(and_(City.city_name == city, left_date <= Weather.date, Weather.date <= right_date))
    result = await session.execute(avg)
    avg_data = []
    for item in result.all():
        avg_data.append({'avg_temp': item[0], 'avg_pressure':item[1], 'avg_wind':item[2]})

    return {
        'status': 'success',
        'all_data': all_data,
        'avg_data': avg_data,
        'details': None
    }

@router_cities.get('/')
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    """ Эндпоинт получения всех городов """
    query = select(City.id, City.city_name).select_from(City)

    result = await session.execute(query)
    data = []
    for item in result.all():
        data.append(
            {'id':item[0], 'city_name': item[1]}
        )

    return {
        'status': 'success',
        'data': data,
        'details': None
    }

@router_tmp.post('/post')
async def add_weathers(data:Payload, session: AsyncSession = Depends(get_async_session)):
    """ Эндпоинт добавления данных с парсера в БД"""
    stmt = insert(Weather).values(
        {'temperature': data.temperature, 
         'pressure': data.pressure, 
         'wind': data.wind, 
         'date': datetime.now(), 
         'city': data.id
        }
    )
    await session.execute(stmt)
    await session.commit()

    return {
        "status": "ok" 
    }