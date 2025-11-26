import requests
import pandas as pd
from datetime import datetime
from eurostatapiclient import EurostatAPIClient


def get_eurostat_api_data(dataset_code, geo):
    
    VERSION = '1.0'
    FORMAT = 'json'
    LANGUAGE = 'en'
    
    client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
    
    dataset = client.get_dataset(dataset_code)
    df = dataset.to_dataframe()
    df["indicator_label"] = dataset.label
        
    if geo == "nat":
        geo = 'geo'
        geo_list = ["DE", "FI", "SK", "PT", "FR"]
    if geo == "nuts2":
        geo = 'geo'
        geo_list = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
    if geo == "nuts3":
        geo = 'cities'
        geo_list = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
    if geo == "nuts3_1":
        geo = 'geo'
        geo_list = ["FI1B1", "PT170", "FR101", "DEA23", "SK031"]
    
    df = df[df[geo].isin(geo_list)]
    
    df = df[(df['values'].notnull())]
    df['time'] = df['time'].astype(int)
    
    df = df[df['time'] >= 2014]
    
    return df


def get_openweather_api_data():
    cities_lat_lon_dict = {
        "Lisbon": ("38.7369","-9.1427"),
        "Helsinki": ("60.192059","24.945831"),
        "Paris": ("48.864716","2.349014"),
        "Zilina": ("49.22315", "18.73941"),
        "Cologne": ("50.935173","6.953101")
    }
    
    api_key = "05c1afa5a2f15e69b222f5cc7f1af802"
    data = []
    
    for city, (lat, lon) in cities_lat_lon_dict.items():
        weather_api_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        
        # Make the API request
        response = requests.get(weather_api_url)
        if response.status_code != 200:
            print(f"Failed to fetch data for {city}: {response.text}")
            continue
        
        json_data = response.json()
        
        for item in json_data.get('list', []):
            dt = datetime.utcfromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
            main_data = item['main']
            components = item['components']

            data.append({
                "cities": city,
                "date": dt,
                "aqi": main_data.get('aqi'),
                "co": components.get('co'),
                "no": components.get('no'),
                "no2": components.get('no2'),
                "o3": components.get('o3'),
                "so2": components.get('so2'),
                "pm2_5": components.get('pm2_5'),
                "pm10": components.get('pm10'),
                "nh3": components.get('nh3')
            })

    if not data:
        print("No data retrieved from the API")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    df = df[['cities', 'aqi', 'no2', 'pm10', 'pm2_5', 'date']]
    df = pd.melt(df, id_vars=["cities", "date"], var_name="indicator_name", value_name="values")

    return df
