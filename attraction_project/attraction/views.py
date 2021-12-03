from django.db.models.fields import CharField
from django.shortcuts import render
from django.http import HttpResponse
from .models import ScoreInfo, Status, Vaccine
import folium
import pandas as pd
import json
from django.db import connection
from django.db.models import Count

# Create your views here.


def get_attraction_count_sql():

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT attraction_type, count(attraction_type) FROM Covid.attraction GROUP BY attraction_type;")
        row = cursor.fetchall()
    print(row)

    return row

# 사용자 쿼리문


def get_covid_status_list():

    with connection.cursor() as cursor:
        cursor.execute(
            "select * from(select * from status where (country, date) in (select country, max(date) as date from status group by country) order by date desc) t group by t.country")
        row = cursor.fetchall()

    return row

# 사용자 쿼리문


def get_covid_vaccine_list():

    with connection.cursor() as cursor:
        cursor.execute("select country, date, vaccinated, fully_vaccinated, vaccination_rate, fully_vaccination_rate from(select * from vaccine where (country, date) in (select country, max(date) as date from vaccine group by country) order by date desc) t group by t.country")
        row = cursor.fetchone()

    print(row)

    return row


def get_covid_status_list2():
    # covid_status_list = CovidStatus.objects.all()

    sqlResult = ""

    try:
        cursor = connection.cursor()

        strSql = "SELECT * FROM covid_status"
        result = cursor.execute(strSql)
        sqlResult = cursor.fetall()
        print(sqlResult)

        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed selecting in covid_status")

    return sqlResult


def get_covid_vaccine_list2():
    # covid_status_list = CovidStatus.objects.all()

    sqlResult = ""

    try:
        cursor = connection.cursor()

        strSql = "SELECT * FROM covid_vaccine;"
        result = cursor.execute(strSql)

        sqlResult = cursor.fetall()
        print(sqlResult)

        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed selecting in covid_vaccine")

    return sqlResult


def index(request):
    return render(request, 'attraction/index.html')


def attraction_page1(request):

    #covid_status_list = get_covid_status_list()
    #covid_vaccine_list = get_covid_vaccine_list()

    covid_status_list = Status.objects.all()
    covid_vaccine_list = Vaccine.objects.all()

    data = pd.read_csv("attraction/DS/score.csv")
    data.loc[3, "country"] = "Czech Republic"
    data.loc[18, "country"] = "United Kingdom"

    geo_data = 'attraction/geo.geojson'

    geo_data1 = json.load(open(geo_data), encoding='utf-8')

    for idx, country_dict in enumerate(geo_data1['features']):
        country = country_dict['properties']['NAME']
        score = data.loc[(data.country == country), 'score'].iloc[0]
        vader_neg = data.loc[(data.country == country), 'vader_neg'].iloc[0]
        vader_neu = data.loc[(data.country == country), 'vader_neu'].iloc[0]
        vader_pos = data.loc[(data.country == country), 'vader_pos'].iloc[0]
        vader_com = data.loc[(data.country == country), 'vader_com'].iloc[0]

        cases = ""
        today_cases = ""
        cases_per_million = ""

        for covid_status in covid_status_list:

            if covid_status.country == country:

                cases = covid_status.cases
                today_cases = covid_status.today_cases
                cases_per_million = covid_status.cases_per_million

                break

        vaccinated = ""
        fully_vaccinated = ""
        vaccination_rate = ""
        fully_vaccination_rate = ""

        for covid_vaccine in covid_vaccine_list:
            if covid_vaccine.country == country:
                vaccinated = covid_vaccine.vaccinated
                fully_vaccinated = covid_vaccine.fully_vaccinated
                vaccination_rate = covid_vaccine.vaccination_rate
                fully_vaccination_rate = covid_vaccine.fully_vaccination_rate

        # vader_neg	vader_neu	vader_pos	vader_com

        txt = f'<b><h4>{country}</h4><b>score : {score:.6f}<br>vader_neg : {vader_neg:.6f}<br>vader_neu : {vader_neu:.6f}<br>vader_pos : {vader_pos:.6f}<br>vader_com : {vader_com:.6f}<br>-------------<br>전체 확진자 : {cases}<br>일일 확진자 : {today_cases}<br>백만명당 확진자 : {cases_per_million}<br>-------------<br>1차 접종 : {vaccinated}<br>접종 완료 : {fully_vaccinated}<br>1차 접종률 : {vaccination_rate}%<br>접종 완료율 : {fully_vaccination_rate}%'

        geo_data1['features'][idx]['properties']['tooltip1'] = txt

    center = [57.0316, 12.7966]

    map = folium.Map(location=center, zoom_start=3)

    choropleth = folium.Choropleth(
        geo_data=geo_data1,
        data=data,
        columns=('country', 'vader_com'),
        key_on='feature.properties.NAME',
        fill_color='YlGn'
    ).add_to(map)

    def style_function(x): return {'fillColor': '#ffffff',
                                   'color': '#000000',
                                   'fillOpacity': 0.1,
                                   'weight': 0.1}

    def highlight_function(x): return {'fillColor': '#000000',
                                       'color': '#000000',
                                       'fillOpacity': 0.1,
                                       'weight': 1}
    NIL = folium.features.GeoJson(
        geo_data1,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,


        tooltip=folium.features.GeoJsonTooltip(['tooltip1'],  labels=False)

    )

    map.add_child(NIL)
    map.keep_in_front(NIL)
    folium.LayerControl().add_to(map)

    maps = map._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

    return render(request, 'attraction/attraction1.html', {'map': maps, 'covid_status_list': get_covid_status_list(), "covid_vaccine_list": covid_vaccine_list})


def attraction_page2(request):

    return render(request, "attraction/attraction2.html")
