from django.shortcuts import render
from django.http import HttpResponse
import folium
import pandas as pd

# Create your views here.


def index(request):
    return render(request, 'attraction/index.html')


def attraction_page(request):
    data = pd.read_csv("attraction/DS/score.csv")
    data.loc[3, "country"]="Czech Republic"
    data.loc[18, "country"]="United Kingdom"

    geo_data = 'attraction/geo.geojson'

    center = [57.0316, 12.7966]

    map = folium.Map(location=center, zoom_start=3)

    folium.Choropleth(
        geo_data=geo_data,
        data=data,
        columns=('country','vader_com'),
        key_on='feature.properties.NAME',
        fill_color='YlGn'
    ).add_to(map)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.1, 
                                    'weight': 1}
    NIL = folium.features.GeoJson(
        geo_data,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NAME'],
            aliases=['']
        )
    )

    map.add_child(NIL)
    map.keep_in_front(NIL)
    folium.LayerControl().add_to(map)

    maps=map._repr_html_() #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

    return render(request, 'attraction/attraction.html', {'map':maps})


def map_page(request):
    return render(request, 'attraction/eu_map.html')
