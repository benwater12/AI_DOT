import time
import datetime
import os
from selenium import webdriver
from bs4 import BeautifulSoup as soup 
import json
from math import floor
import requests


def __driving_history_from_to(start_datetime,from_str, destination_str):
    if destination_str=="信義商圈":
        destination_str="110台北市信義區信義路五段7號"
    if destination_str=="象山":
        destination_str="一線天"
    if destination_str=="四四南村":
        destination_str="110台北市信義區信義路五段24巷5弄"
    if destination_str=="故宮博物院":
        destination_str="111台北市士林區至善路二段221號"
    params = {
    "origin": from_str,
    "departure_time": str(floor(time.mktime(start_datetime.timetuple()))),
    "destination":destination_str,
    "mode":"driving",
    "key":"???"
    }
    base_url="https://maps.googleapis.com/maps/api/directions/json"
    json_response=requests.get(base_url, params=params)
    json_response_str=json_response.content
    json_response.close()
    drive_time=__get_time_in_min(json_response_str)

    return drive_time

def __walking_history_from_to(start_datetime,from_str, destination_str):
    params = {
    "origin": from_str,
    "departure_time": str(floor(time.mktime(start_datetime.timetuple()))),
    "destination":destination_str,
    "mode":"walking",
    "key":"???"
    }
    base_url="https://maps.googleapis.com/maps/api/directions/json"
    json_response=requests.get(base_url, params=params)
    json_response_str=json_response.content
    json_response.close()
    walking_time=__get_time_in_min(json_response_str)
    return walking_time

def __biking_history_from_to(start_datetime,from_str, destination_str):
    params = {
    "origin": from_str,
    "departure_time": str(floor(time.mktime(start_datetime.timetuple()))),
    "destination":destination_str,
    "mode":"biking",
    "key":"???"
    }
    base_url="https://maps.googleapis.com/maps/api/directions/json"
    json_response=requests.get(base_url, params=params)
    json_response_str=json_response.content
    json_response.close()
    biking_time=__get_time_in_min(json_response_str)
    return biking_time

def __transit_history_from_to(start_datetime,from_str, destination_str):
    params = {
    "origin": from_str,
    "departure_time": str(floor(time.mktime(start_datetime.timetuple()))),
    "destination":destination_str,
    "mode":"transit",
    "key":"???"
    }
    base_url="https://maps.googleapis.com/maps/api/directions/json"
    json_response=requests.get(base_url, params=params)
    json_response_str=json_response.content
    json_response.close()
    transit_time=__get_time_in_min(json_response_str)
    return transit_time

def __get_time_in_min(json_response_str):
    json_dict=json.loads(json_response_str)
    in_second_int=json_dict["routes"][0]["legs"][0]["duration"]["value"]
    return floor(in_second_int/60)
    
def get_traffic_time(start_datetime,from_str, destination_str):
    # transit_time=__transit_history_from_to(start_datetime,from_str, destination_str)
    # walking_time=__walking_history_from_to(start_datetime,from_str, destination_str)
    drive_time=__driving_history_from_to(start_datetime,from_str, destination_str)
    # biking_time=__biking_history_from_to(start_datetime,from_str, destination_str)


    return {"spot": destination_str,
    # "transit_time(min)": transit_time,
    # "biking_time(min)": biking_time,
    "drive_time(min)": drive_time
    }


def history_from_to(start_datetime,from_str, destination_str):
    os.chmod((os.getcwd()+"/chromedriver"), 755)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path = (os.getcwd()+"/chromedriver"),chrome_options=chrome_options)
    start_unix_datetime=time.mktime(start_datetime.timetuple())
    start_unix_str=str(start_unix_datetime)
    if destination_str == "烏來瀑布":
        url = f'https://www.google.com/maps/dir/{from_str}/烏來區/data=!4m6!4m5!2m3!6e0!7e0!8j{start_unix_str}!3e0'
    elif destination_str == "內洞森林遊樂區":
        url = f'https://www.google.com/maps/dir/{from_str}/烏來區/data=!4m6!4m5!2m3!6e0!7e0!8j{start_unix_str}!3e0'
    else:
        url = f'https://www.google.com/maps/dir/{from_str}/{destination_str}/data=!4m6!4m5!2m3!6e0!7e0!8j{start_unix_str}!3e0'
    
    driver.get(url)
    page_soup = soup(driver.page_source, "html.parser")
    # if page_soup.find(class_="XdKEzd") is not None:
    #     travel_text=page_soup.find(class_="XdKEzd").text
    #     driver.close()
    #     driver.quit()
    # else:
    #     driver.close()
    #     driver.quit()
    #     return -1
    time.sleep(0.5)
    travel_text=page_soup.find(class_="XdKEzd").text
    driver.close()
    
    # print(to+" trans :"+travel_text)
    travel_text_list=travel_text.split("預估行車時間：")
    if travel_text_list[0].strip()=="":
        min_time_span=travel_text_list[1].split(" -")[0].strip()
    else:
        min_time_span=travel_text_list[0].strip()
    time_list=min_time_span.split(" 小時")
    if len(time_list)>1:
        hr=int(time_list[0])
        if "分" not in time_list[1]:
            min=0
        else:
            min=int(time_list[1].split(" 分")[0])
    elif len(time_list)==1:
        hr=0
        min=int(time_list[0].split(" 分")[0])
    drive_time=hr*60+min

    result = {"spot":destination_str,"drive_time(min)": drive_time}
    
    driver.quit()

    # # 要殺死程式名稱，最好全名
    # program_name = "webdriver"
    # # 終端執行的命令
    # order_str = "ps -aux|grep %s" % program_name
    # # 執行
    # strs_obj = os.popen(order_str)
    # t_strs = strs_obj.read()
    # # 通過正則獲取pid
    # pid_list = re.findall(r"(\d+).+webdriver --port=\d+", t_strs, re.I)
    # print(pid_list)
    # for j in pid_list:
    #     # print(j)
    #     # 殺死程序
    #     os.kill(int(j), signal.SIGKILL)
    # print(result)
    return result

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
    print(get_traffic_time(datetime.datetime(2022,6,28),"兒童新樂園","淡水站"))
