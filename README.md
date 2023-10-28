# Weather API with parser
___
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi)
![PyPI](https://img.shields.io/pypi/v/FastAPI?label=fastapi&color=gree)
![PyPI](https://img.shields.io/pypi/v/sqlalchemy?label=sqlalchemy&color=purple)
![PyPI](https://img.shields.io/pypi/v/alembic?label=alembic&color=pink)
![PyPI](https://img.shields.io/pypi/v/asyncpg?label=asyncpg&color=brown)
![PyPI](https://img.shields.io/pypi/v/pydantic?label=pydantic&color=yellow)
![PyPI](https://img.shields.io/pypi/v/httpx?label=httpx&color=red)
![PyPI](https://img.shields.io/pypi/v/beautifulsoup4?label=beautifulsoup4&color=orange)
![PyPI](https://img.shields.io/pypi/v/selenium?label=selenium&color=black)


## :sparkles: Описание проекта
___
В проекте реализовано 2 сервиса: API и парсер.

Парсер каждую минуту сохраняет в БД сведения о погоде с сайта openweather.org (температура в этом городе, атмосферное давление и скорость ветра).

В API реализованы возможности добавления новых городов, получение информации о всех записанных значениях о погоде в городах.

Для хранения информация была выбрана БД PostgreSQL, поскольку она является высокопроизводительным, современным opensource решением, гарантируя тем самым эффективную и комфортную работы с массивами данных.

Для проекта написаны Docker и Make file'ы.

## :clipboard: Использование
Если приложение собирается впервые используйте:
```
make build
```
Для стандартного запуска уже собранного приложения используйте:
```
make run
```
Для того, чтобы запустить парсер используйте:
```
make run_parser
```
___

## :pushpin: API Endpoints

### WEATHERS
Группа эндпоинтов для работы с погодой и городами: добавление новых городов, получение статистики о погоде по городам
#### POST - /weathers/{city}
Эндпоинт добавления нового города в БД

Example Input:
```
{
    "city": "Moscow"
} 
```
Example Response:
```
{
  "status": "ok"
}
```
#### GET - /weathers?search={search}
Эндпоинт получения всех городов с последней записанной температурой с фильтрацией

Example Response:
```
{
  "status": "success",
  "data": [
    {
      "city_name": "Moscow",
      "temperature": 2
    }
  ],
  "details": null
}
```

#### GET - /weathers/all_by_city
Эндпоинт для получения всех данных и средних значений за указанный период

Example Input:
```
{
    "city": "Moscow",
    "date1": "2023-10-27 00:00:00",
    "date2": "2023-10-29 00:00:00"
} 
```
Example Response:
```
{
  "status": "success",
  "all_data": [
    {
      "date": "2023-10-28T22:41:33.632902",
      "id": 1,
      "wind": 1.5,
      "temperature": 1,
      "pressure": 1034,
      "city": 1
    },
    {
      "date": "2023-10-28T22:42:54.180544",
      "id": 2,
      "wind": 1.3,
      "temperature": 2,
      "pressure": 1034,
      "city": 1
    }
  ],
  "avg_data": [
    {
      "avg_temp": 1.5,
      "avg_pressure": 1034,
      "avg_wind": 1.4
    }
  ],
  "details": null
}
```
