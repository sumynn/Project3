# -*- coding: utf-8 -*-

import requests
import pandas as pd
import json
import datetime
import pymysql
from sqlalchemy import create_engine
import sqlalchemy

pymysql.install_as_MySQLdb()

# country 목록 (ISO3 code)
countries=['AUT', 'BEL', 'HRV', 'CZE', 'DNK', 'FRA', 'DEU', 'GRC', 'ISL', 'IRL', 'ITA', 'NLD', 'NOR', 'POL', 'PRT', 'ESP', 'SWE', 'CHE', 'TUR', 'GBR']

def status():
    # api 사용 (https://disease.sh/docs/)
    url = 'https://disease.sh/v3/covid-19/countries'
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame()

    # 해당 나라 데이터 추출
    for d in data:
        if d['countryInfo']['iso3'] in countries:
            df = df.append(d, ignore_index=True)

    # 나라, 누적확진자, 신규확진자, 100만명당확진자
    df = df[['country', 'cases', 'todayCases', 'casesPerOneMillion']]

    # 오늘 날짜 추가
    date = datetime.date.today()
    df['date'] = date

    # column 이름, 순서 변경
    df.columns = ['country', 'cases', 'today_cases', 'cases_per_million', 'date']
    df.loc[df['country']=='Czechia', ['country']] = 'Czech'
    df = df[['country', 'date', 'cases', 'today_cases', 'cases_per_million']]
    
    # MySQL 저장
    engine = create_engine("mysql+mysqldb://team4:team4_test@52.198.86.88:3306/Covid", encoding='utf-8')
    conn = engine.connect()
    dtypesql = {'country':sqlalchemy.types.VARCHAR(50),
                'date':sqlalchemy.Date(), 
                'cases':sqlalchemy.Integer(),
                'today_cases':sqlalchemy.Integer(), 
                'cases_per_million':sqlalchemy.Integer()
                }
    df.to_sql(name='status', con=engine, if_exists='append', index=False, dtype=dtypesql)


def vaccine():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)

    df = df[df['iso_code'].isin(countries)]
    df = df.reset_index(drop=True)

    df_vaccine = pd.DataFrame()

    for i in range(20):
        row = df['data'][i][-1]
        try:
            # 나라, 업데이트일, 누적 1차 접종자 수, 누적 접종 완료자 수, 1차 접종률, 접종 완료율
            vaccine_data = {'country':df['country'][i],
                            'date':row['date'],
                            'vaccinated':row['people_vaccinated'], 
                            'fully_vaccinated':row['people_fully_vaccinated'],
                            'vaccination_rate':row['people_vaccinated_per_hundred'],
                            'fully_vaccination_rate':row['people_fully_vaccinated_per_hundred'],
                            }
        except:
            continue
        
        df_vaccine = df_vaccine.append(vaccine_data, ignore_index=True)

    # 나라 이름, column 순서 변경
    df_vaccine.loc[df_vaccine['country']=='Czechia', ['country']] = 'Czech'
    df_vaccine.loc[df_vaccine['country']=='United Kingdom', ['country']] = 'UK'
    df_vaccine = df_vaccine[['country', 'date', 'vaccinated', 'fully_vaccinated', 'vaccination_rate', 'fully_vaccination_rate']]

    # MySQL 저장
    engine = create_engine("mysql+mysqldb://team4:team4_test@52.198.86.88:3306/Covid", encoding='utf-8')
    conn = engine.connect()
    dtypesql = {'country':sqlalchemy.types.VARCHAR(50),
                'date':sqlalchemy.Date(), 
                'vaccinated':sqlalchemy.Integer(),
                'fully_vaccinated':sqlalchemy.Integer(), 
                'vaccination_rate':sqlalchemy.Float(),
                'fully_vaccination_rate':sqlalchemy.Float()
                }
    df_vaccine.to_sql(name='vaccine', con=engine, if_exists='append', index=False, dtype=dtypesql)


if __name__ == "__main__":
    status()
    vaccine()
    print("Update Covid Info ---", datetime.datetime.now())