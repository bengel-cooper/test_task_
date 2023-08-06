#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup

# Читаем данные из txt файла в dataframe
df_input = pd.read_csv('gplay_urls.txt', sep='\s+', header=0)

# Чистим данные. Используем функцию insert_https для вставки "https://" перед "play" в столбце 'gplay_url'
def insert_https(row):
    if row['gplay_url'].startswith('play'):
        return 'https://' + row['gplay_url']
    else:
        return row['gplay_url']

# Применяем функцию insert_https к столбцу 'url' и обновляем значения
df_input['gplay_url'] = df_input.apply(insert_https, axis=1)

# Функция для парсинга данных о приложении
def parse_app_data(row):
    domain = row['domain']
    gplay_url = row['gplay_url']
    response = requests.get(gplay_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    average_rating = soup.select_one('div.TT9eCd').text
    review_count = soup.select_one('div.g1rdde').text
    install_count = soup.select('div.wVqUob div.ClM7O')[1].text

    return {
        'domain': domain,
        'average_rating': average_rating,
        'review_count': review_count,
        'install_count': install_count
    }

# Применяем функцию parse_app_data к каждой строке в dataframe и получаем список словарей
app_data_list = df_input.apply(parse_app_data, axis=1).tolist()

# Создаем dataframe из списка словарей
df = pd.DataFrame(app_data_list)

# Изменяем формат строк, и преобразуем их типы в целочисленный для столбцов 'review_count', 'install_count' и число с плавающей точкой для столбца 'average_rating'
df['average_rating'] = df['average_rating'].str.replace('star', '').str.strip().astype(float)
df['review_count'] = df['review_count'].str.replace('reviews', '').str.replace('K', '*1e3', regex=True).str.replace('M', '*1e6', regex=True).str.replace('+', '').map(pd.eval).astype(int)
df['install_count'] = df['install_count'].str.replace('K', '*1e3', regex=True).str.replace('M', '*1e6', regex=True).str.replace('+', '').map(pd.eval).astype(int)

# Устанавливаем подключение к базе данных и создаем новую схему 'test'. 
# Вместо db нужно указать название базы данных, вместо host - адрес хоста, вместо port - порт соединения
engine = create_engine("postgresql://db:login@host:port")
Session = sessionmaker(bind=engine)
session = Session()
engine.execute ("CREATE SCHEMA IF NOT EXISTS test")

#Удаляем таблицу gplay_stats если она была ранее создана
engine.execute ("DROP TABLE IF EXISTS test.gplay_stats")

# Создаем пустую таблицу gplay_stats
Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'gplay_stats'
    __table_args__ = {'schema': 'test'}

    id = Column(Integer, primary_key=True)
    domain = Column(String(200))
    average_rating = Column(Numeric(precision=4, scale=2))
    review_count = Column(Integer)
    install_count = Column(Integer)

Base.metadata.create_all(engine)

#Создаем словарь из dataframe для дальнейшего заполнения таблицы 
data = df.to_dict(orient='records')

#Заполняем таблицу значениями из словаря
for item in data:
    record = MyTable(**item)
    session.add(record)

session.commit()

