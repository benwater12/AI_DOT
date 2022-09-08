from math import floor
import requests
import datetime
import json
import pandas
def __get_weather_json(city_str):
    if  "、" in city_str:
        city_str=city_str.split("、")[0]+"區"
    if city_str=="淡水區" or city_str=="烏來區" or city_str=="瑞芳區":
       url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-071"
    else:
       url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-063"
    params = {
        "Authorization": "yourkey",
        "locationName": city_str,
        "elementName":"WeatherDescription"
    }
    weather_json_response = requests.get(url, params=params)
    weather_json_str=weather_json_response.content
    weather_json_response.close()
    return weather_json_str
def __get_condense_weather_list(postoffice_location_str):
    weather_json_str=__get_weather_json(postoffice_location_str)
    weather_dict=json.loads(weather_json_str)
    return weather_dict["records"]["locations"][0]['location'][0]["weatherElement"][0]['time']
def __get_weather_data_interval(point_datetime,start_datetime):
    interval_delta=datetime.timedelta(hours=12)
    actual_delta_time=point_datetime-start_datetime
    gap_number_int=floor(actual_delta_time.total_seconds()/interval_delta.total_seconds())
    return gap_number_int
def __get_weather_start_datetime(condense_weather_list):
    time_str = condense_weather_list[0]["startTime"]
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

def get_weather_data(point_datetime,postoffice_location_str):
    condense_weather_list=__get_condense_weather_list(postoffice_location_str)
    start_datetime = __get_weather_start_datetime(condense_weather_list)
    gap_number_int = __get_weather_data_interval(point_datetime,start_datetime)

    return condense_weather_list[gap_number_int]["elementValue"][0]["value"]

if __name__ == '__main__':
    names="大安區"
    something_list=__get_condense_weather_list(names)
    print(something_list)
    starttime=__get_weather_start_datetime(something_list)
    c=__get_weather_data_interval(datetime.datetime(2022,6,17,hour=18, minute=0, second=0),starttime)
    print(get_weather_data(c,something_list))





