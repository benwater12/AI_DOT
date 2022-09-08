from math import floor
import requests
import datetime
import json
import time

def get_google_distance_json_str(datetime_arrive,start_location_str,end_location_str,mode):
    params = {
    "origin": start_location_str,
    "departure_time": str(floor(time.mktime(datetime_arrive.timetuple()))),
    "destination":end_location_str,
    "mode":mode,
    "key":"GOOGLEAPIKEY"
    }
    base_url="https://maps.googleapis.com/maps/api/directions/json"
    json_response=requests.get(base_url, params=params)
    json_response_str=json_response.content
    json_response.close()
    return json_response_str

def get_time_in_min(json_response_str):
    json_dict=json.loads(json_response_str)
    in_second_int=json_dict["routes"][0]["legs"][0]["duration"]["value"]
    return floor(in_second_int/60)

def traffic_time_cal(std_time,input_time):
    time_offset=input_time-std_time
    if time_offset>30:
        result=0.1
    elif time_offset<0:
        result=1
    else:
        result=round(1-time_offset*0.1/5,2)
    return result
if __name__ == '__main__':
    str_min=get_time_in_min(get_google_distance_json_str(datetime.datetime(2022,6,27),"淡水站","公館站","driving"))
    print(str_min)
