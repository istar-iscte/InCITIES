import pandas as pd
import streamlit as st
import plotly.express as px
from utils.utils import *
from utils.echarts import *
from utils.get_api_data import get_eurostat_api_data
from streamlit_echarts import st_echarts


# ----------------------- Social Resilience -----------------------

# Educational equality

def line_chart_educational_equality(kpi):
    
    if kpi in ["tgs00109", "edat_lfse_04"]:
        
        df = get_eurostat_api_data(kpi, "nuts2")

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
        
        if kpi == "tgs00109":
            kpi = "Tertiary educational attainment"
            df = df[(df['sex'] == 'T')]
        else:
            kpi = "% of population with only 0-2 educational levels"
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y25-64') & (df['isced11'] == 'ED0-2')]

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


def bar_chart_educational_equality(kpi):
    
    if kpi in ["tgs00109", "edat_lfse_04"]:
        
        df = get_eurostat_api_data(kpi, "nuts2")

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
        
        if kpi == "tgs00109":
            kpi = "Tertiary educational attainment"
            df = df[(df['sex'] == 'T')]
        else:
            kpi = "% of population with only 0-2 educational levels"
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y25-64') & (df['isced11'] == 'ED0-2')]
    
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


# Demography

def donut_chart_demo_pop_productive_age():

    df = get_eurostat_api_data("demo_r_pjangrp3", "nuts3_1")

    df = df[
        (df['sex']== 'T') &
        (df['age'].isin([
            'Y15-19','Y20-24','Y25-29',
            'Y30-34','Y35-39','Y40-44',
            'Y45-49','Y50-54', 'Y55-59', 'Y60-64'])
        )
    ]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisbon",
        "FR101":"Paris",
        "DEA23":"Cologne",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }

    df = df[["values", "geo"]]
    
    df = df.groupby('geo')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    data = [
        {
            'value': row['normalized_values'], 
            'name': row['geo'],
            'itemStyle': {'color': color_mapping.get(row['geo'])}
        }
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Population in productive age (%)", 'Year: ' + str(max_year), data)
    
    return st_echarts(options=option, height="500px")


def donut_chart_demo_pop_aged_65():

    df = get_eurostat_api_data("demo_r_pjangrp3", "nuts3_1")

    df = df[
        (df['sex']== 'T') &
        (~df['age'].isin([ 'TOTAL', 'Y_LT5', 'Y5-9', 'Y10-14',
            'Y15-19','Y20-24','Y25-29',
            'Y30-34','Y35-39','Y40-44',
            'Y45-49','Y50-54', 'Y55-59', 'Y60-64', 'UNK'])
        )
    ]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisbon",
        "FR101":"Paris",
        "DEA23":"Cologne",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    df = df[["values", "geo"]]
    
    df = df.groupby('geo')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    data = [
        {
            'value': row['normalized_values'], 
            'name': row['geo'],
            'itemStyle': {'color': color_mapping.get(row['geo'])}
        }
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Population aged 65 years and older (%)", 'Year: ' + str(max_year), data)
    
    return st_echarts(options=option, height="500px")


def bar_chart_demo_pop_density():

    df = get_eurostat_api_data("demo_r_d3dens", "nuts3_1")
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisbon",
        "FR101":"Paris",
        "DEA23":"Cologne",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    df = df[["values", "geo"]]
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Population density", "Number of Residents per km² - " + str(max_year), geo_list, values_list, colors)
    
    return st_echarts(options=option, height="500px")


# Transportation access

def donut_chart_transportation_access():
    
    df = get_eurostat_api_data("tran_r_vehst", 'nuts2')

    df = df[(df['vehicle'] == 'TOT_X_TM') & (df['unit'] == 'NR')]

    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", 'geo']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    }
    
    df = df.groupby('geo')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    data = [
        {
            'value': row['normalized_values'], 
            'name': row['geo'],
            'itemStyle': {'color': color_mapping.get(row['geo'])}
        }
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Stock of Vehicles (%)", 'Year: ' + str(max_year), data)
    
    return st_echarts(options=option, height="500px")


# ----------------------- Economic Resilience -----------------------

def line_chart_economic_resilience(kpi):

    df = get_eurostat_api_data(kpi, "nuts2")
        
    if kpi in ["hlth_rs_physreg", "tgs00006"]:
        
        if kpi == "hlth_rs_physreg":
            df = df[(df['unit'] == 'P_HTHAB')]
            df = df[['values', 'geo', 'time']]
            kpi = "Number of Physicians (per 100,000 inhabitants)"
        else:
            df = df[['values', 'geo', 'time']]
            kpi = "Regional gross domestic product"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    } 

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


def bar_chart_economic_resilience(kpi):

    df = get_eurostat_api_data(kpi, "nuts2")
        
    if kpi in ["hlth_rs_physreg", "tgs00006"]:
        if kpi == "hlth_rs_physreg":
            df = df[(df['unit'] == 'P_HTHAB')]
            kpi = "Number of Physicians (per 100,000 inhabitants)"
        else:
            kpi = "Regional gross domestic product"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    }
    
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


# ----------------------- Infrastructure Resilience -----------------------


def line_chart_infrastructure_resilience():
    
    df = get_eurostat_api_data("tgs00064", "nuts2")
    df = df[['values', 'geo', 'time']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    } 

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
    
    option = line_chart("Number of hospital beds", "Per 100,000 inhabitants", geo_list, year_list, result)
    return st_echarts(options=option, height="500px")


def bar_chart_infrastructure_resilience():

    df = get_eurostat_api_data("tgs00064", "nuts2")

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    }
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Number of hospital beds", f"Per 100,000 inhabitant - {max_year}", geo_list, values_list, colors)
    
    return st_echarts(options=option, height="500px")


# ----------------------- Hazard Resilience -----------------------

def hazard_resilience():
    
    df = pd.read_excel('/home/bfss/incities/InCITIES/data/Emdat_database.xlsx') 

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_list = ["Frequency of disaster", "Variety of natural disasters"]
        kpi = st.selectbox('Select KPI:', kpi_list)
        
    if kpi == "Frequency of disaster":
        
        df = df.groupby(['Start Year', 'Country']).size().reset_index(name='Frequency of Disasters')
        df = df.groupby('Country')['Frequency of Disasters'].mean().reset_index()
        df.columns = ['geo', 'values']
        df = df.sort_values(by='values').round(2)
        
        geo_list = df['geo'].unique().tolist()
        values_list = df['values'].tolist()
        
        color_mapping = {
            "Germany": "#6272A4",
            "Finland": "#8BE9FD",
            "Slovakia": "#FFB86C",
            "Portugal": "#FF79C6",
            "France": "#BD93F9"
        }
        colors = [color_mapping.get(region) for region in geo_list]
        
        series_data = [{"value": y, "itemStyle": {"color": c}} for y, c in zip(values_list, colors)]

        option = {
            "title": {"text": "Frequency of disasters", "subtext": "Average per year"},
            "grid": {'top': '15%', 'right': '5%', 'bottom': '5%', 'left': '5%', 'containLabel': 'true'},
            "tooltip": {},
            "xAxis": {
                "type": 'category',
                "data": geo_list,
            },
            "yAxis": {
                "type": 'value'
            },
            "series": [
                {
                    "data": series_data,
                    "type": 'bar'
                }
            ]
        }
        
        st_echarts(options=option, height="500px")
        
    else:
        with col2:
            df = df[df['Disaster Group'] == 'Natural']
            disaster_type_list = df['Disaster Type'].unique().tolist()
            disaster_type = st.selectbox('Select disaster type:', disaster_type_list)
        
        df = df[df['Disaster Type'] == disaster_type]
        
        color_mapping = {
            "Germany": "#6272A4",
            "Finland": "#8BE9FD",
            "Slovakia": "#FFB86C",
            "Portugal": "#FF79C6",
            "France": "#BD93F9"
        } 
        with col3:
            view_mode = st.radio("Select chart view:", options=["Stacked", "Split by Country"], index=0)

        if view_mode == "Stacked":
            fig = px.bar(
                df,
                x="Start Year",
                y="Total Deaths",
                color="Country",
                title="Total Deaths by Year and Country",
                labels={"Start Year": "Year", "Total Deaths": "Total Deaths"},
                hover_data=["Disaster Type", "Disaster Group"],
                color_discrete_map=color_mapping
            )
            fig.update_layout(
                height=500
            )
            
        else:
            fig = px.bar(
                df,
                x="Start Year",
                y="Total Deaths",
                color="Country",
                title="Total Deaths by Year and Country (Split by Country)",
                labels={"Start Year": "Year", "Total Deaths": "Total Deaths"},
                hover_data=["Disaster Type", "Disaster Group"],
                facet_col="Country",
                facet_col_wrap=2,
                color_discrete_map=color_mapping
            )
        
            fig.update_layout(
                height=800
            )
        
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="linear"
            ),
            xaxis_title="Year",
            yaxis_title="Total Deaths",
        )
        st.plotly_chart(fig)
    

# ----------------------- Institutional Resilience -----------------------

def line_chart_institutional_resilience():
    
    df = get_eurostat_api_data('tin00129', 'nat')
    df = df[df['ind_type'] == "IND_TOTAL"]

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
    
    option = line_chart(
        "Individuals using the internet for taking part in online consultations or voting", 
        "Percentage of individuals (%)", 
        geo_list, 
        year_list, 
        result)
    
    return st_echarts(options=option, height="500px")


def bar_chart_institutional_resilience():
    
    df = get_eurostat_api_data('tin00129', 'nat')
    df = df[df['ind_type'] == "IND_TOTAL"]
    
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
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart(
        "Individuals using the internet for taking part in online consultations or voting", 
        f"Percentage of individuals (%) - {max_year}", 
        geo_list, 
        values_list, 
        colors)
    
    return st_echarts(options=option, height="500px")
