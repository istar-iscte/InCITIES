from utils.get_api_data import get_eurostat_api_data
from streamlit_echarts import st_echarts
from utils.echarts import *
import streamlit as st
import plotly.express as px


def line_chart_inclusion(kpi):
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        df = get_eurostat_api_data(kpi, "nat")
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = get_eurostat_api_data(kpi, "nuts2")
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        color_mapping = {
            "Germany": "#6272A4",
            "Finland": "#8BE9FD",
            "Slovakia": "#FFB86C",
            "Portugal": "#FF79C6",
            "France": "#BD93F9"
        } 
        if kpi == "tessi190":
            kpi = "Gini coefficient of equivalized disposable income (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile de France"
        }
        color_mapping = {
            "Köln": "#6272A4",
            "Helsinki-U.": "#8BE9FD",
            "S. Slovensko": "#FFB86C",
            "A. M. Lisboa": "#FF79C6",
            "Ile de France": "#BD93F9"
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Young people neither in employment nor in education and training (%)"
        
    df = df[["values", "geo", "time"]]
    df['geo'] = df['geo'].replace(geo_name)

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['geo']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return st_echarts(options=option, height="500px")



def map_inclusion(kpi):
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        df = get_eurostat_api_data(kpi, 'nat')
        
        geo_name = {
            'PT': 'Portugal',
            'DE': 'Germany',
            'FR': 'France',
            'FI': 'Finland',
            'SK': 'Slovakia'
        }
        df['geo_name'] = df['geo'].replace(geo_name)
        
        geo_code = {
            'PT': 'PRT',
            'DE': 'DEU',
            'FR': 'FRA',
            'FI': 'FIN',
            'SK': 'SVK'
        }
        
        if kpi == "tessi190":
            kpi = "Gini coefficient (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = get_eurostat_api_data(kpi, 'nuts2')
        geo_name = {
            'PT17': 'A. M. Lisboa',
            'DEA2': 'Köln',
            'FR10': 'Ile de France',
            'FI1B': 'Helsinki-U.',
            'SK03': 'S. Slovensko'
        }
        df['geo_name'] = df['geo'].replace(geo_name)
        geo_code = {
            'PT17': 'PRT',
            'DEA2': 'DEU',
            'FR10': 'FRA',
            'FI1B': 'FIN',
            'SK03': 'SVK'
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment (%)"
        
    df = df[['geo', 'time', 'geo_name', 'values']]
    
    df['geo'] = df['geo'].replace(geo_code)
    
    df = df.sort_values(by='time')
        
    geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'
    
    fig = px.choropleth_mapbox(
        df, 
        geojson=geojson_url, 
        locations='geo', 
        color='values',
        color_continuous_scale="YlGnBu",
        mapbox_style="open-street-map",
        zoom=2.2, 
        center = {"lat": 54.5260, "lon": 15.2551},
        opacity=0.5,
        hover_name="geo_name",
        labels={'values': kpi, 'geo': 'country_code', 'time': 'year'},
        animation_frame="time",
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return st.plotly_chart(fig)


def bar_chart_inclusion(kpi):
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        df = get_eurostat_api_data(kpi, 'nat')
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = get_eurostat_api_data(kpi, 'nuts2')

    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        color_mapping = {
            "Germany": "#6272A4",
            "Finland": "#8BE9FD",
            "Slovakia": "#FFB86C",
            "Portugal": "#FF79C6",
            "France": "#BD93F9"
        }  
        if kpi == "tessi190":
            kpi = "Gini coefficient (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile de France"
        }
        color_mapping = {
            "Köln": "#6272A4",
            "Helsinki-U.": "#8BE9FD",
            "S. Slovensko": "#FFB86C",
            "A. M. Lisboa": "#FF79C6",
            "Ile de France": "#BD93F9"
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment (%)"
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart(kpi, f"Year: {max_year}", geo_list, values_list, colors)
    
    return st_echarts(options=option, height="500px")