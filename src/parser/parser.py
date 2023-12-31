import json
import asyncio
import httpx

import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


GET_ALL_CITIES_URL = "http://127.0.0.1:8000/cities/"
INSERT_WEATHER_URL = "http://127.0.0.1:8000/cities/add_weather"

insert_data = []

async def get_cities_from_db(url: str):
    """ Метод получения городов из БД """
    data = await get_task(url)
    return data


async def get_task(url: str):
    """ Вспомогательный метод создания get запроса на API """
    async with httpx.AsyncClient() as client:
        result = await asyncio.gather(get_request(client, url))
        return result


async def get_request(client: httpx.AsyncClient, url: str):
    """ Вспомогательный метод получения ответа из get запроса на API """
    response = await client.get(url)
    return response.text


async def post_weather_data_to_db(url: str, data):
    """ Метод создания новых значений погоды в БД """
    await post_task(url, data)


async def post_task(url: str, data):
    """ Вспомогательный метод создания post запроса на API """
    async with httpx.AsyncClient() as client:
        await asyncio.gather(post_request(client, url, data))


async def post_request(client: httpx.AsyncClient, url: str, data):
    """ Вспомогательный метод получения ответа из post запроса на API """
    await client.post(url, json=data)


async def gather_urls():
    """ Метод получения готовых url для городов из БД """
    with open('src/parser/cities_id.json') as json_file:
        api_data = json.load(json_file)
        api_cities = {city['name']: city['id'] for city in api_data}

        cities_json = await get_cities_from_db(GET_ALL_CITIES_URL)
        db_cities = json.loads(cities_json[0])['data']

        urls = [{(city['id'], city['city_name']): f'https://openweathermap.org/city/{api_cities[city["city_name"]]}'}
                for city in db_cities]

        return urls


async def gather_data(urls: list[dict]):
    tasks = []
    sch = 1

    for url in urls:
        task = asyncio.create_task(get_city_data(url, sch))
        tasks.append(task)
        sch += 1
    await asyncio.gather(*tasks)


async def get_city_data(url: dict, sch: int):
    """ Метод парсинга необходимых данных с сайта """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote("http://chrome:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)
    for key, val in url.items():
        driver.get(val)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        temperature = int(soup.find(class_='current-temp').text.split('°C')[0])
        wind = float(soup.find('div', class_='wind-line').text.split('m')[0])
        pressure = int(soup.find('svg', class_='icon-pressure').find_previous().text.split('hPa')[0])

        insert_data.append({
            'id': key[0],
            'temperature': temperature,
            'wind': wind,
            'pressure': pressure
        })
    driver.close()
    driver.quit()

    print(f'[INFO] Город №{sch} записан. URL: {url}')


async def gather_insert(data: list):
    tasks = []
    for item in data:
        task = asyncio.create_task(post_weather_data_to_db(INSERT_WEATHER_URL, item))
        tasks.append(task)
    await asyncio.gather(*tasks)


def main(data: list):
    print("[INFO] Парсер начал работать")
    while True:
        urls = asyncio.run(gather_urls())
        asyncio.run(gather_data(urls))
        asyncio.run(gather_insert(data))
        data[:] = []
        print(f'[INFO] Парсер записал данные {datetime.now()}')
        time.sleep(60)


if __name__ == '__main__':
    main(insert_data)
