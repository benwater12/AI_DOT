from mongodb_util import get_database_obj

def __get_sightseeing_host_database_list():
    minor_location_collection=get_database_obj("Hank_Tour")["Locations"]
    main_location_cursor=minor_location_collection.find({})
    main_location_list=[main_location for main_location in main_location_cursor]
    return main_location_list

def __get_sightseeing_location_list():
    minor_location_collection=get_database_obj("Hank_Tour")["Main_Locations"]
    main_location_cursor=minor_location_collection.find({})
    main_location_list=[main_location["景點"] for main_location in main_location_cursor]
    return main_location_list

def update_Sightseeing_Location_data(query_value_update_dict):
    minor_location_collection=get_database_obj("Hank_Tour")["Main_Locations"]
    for query in query_value_update_dict:       
        result = minor_location_collection.update_many(
    {
        "景點":  query  
    },

    {
        "$set": { "地址區域" : query_value_update_dict[query] }
    }
        )
    return result

def update_Location_data(query_value_update_list):
    minor_location_collection=get_database_obj("Hank_Tour")["Main_Locations"]
    for query in query_value_update_list:      
        result = minor_location_collection.update_many(
    {
        "景點":  query["spot"]  
    },

    {
        "$set": { "std_time(min)" : query["std_time(min)"] ,"walk_std_time(min)" : query["walk_std_time(min)"],"trans_std_time(min)" : query["trans_std_time(min)"],"bike_std_time(min)" : query["bike_std_time(min)"] }
    }
        )
    return result


json_temp=[
    {
        "spot": "象山",
        "std_time(min)": 7,
        "trans_std_time(min)": 46,
        "walk_std_time(min)": 47,
        "bike_std_time(min)": 14
    },
    {
        "spot": "四四南村",
        "std_time(min)": 6,
        "trans_std_time(min)": 37,
        "walk_std_time(min)": 38,
        "bike_std_time(min)": 14
    },
    {
        "spot": "信義商圈",
        "std_time(min)": 7,
        "trans_std_time(min)": 39,
        "walk_std_time(min)": 40,
        "bike_std_time(min)": 13
    },
    {
        "spot": "台北探索館",
        "std_time(min)": 5,
        "trans_std_time(min)": 31,
        "walk_std_time(min)": 32,
        "bike_std_time(min)": 10
    },
    {
        "spot": "臨江夜市",
        "std_time(min)": 6,
        "trans_std_time(min)": 31,
        "walk_std_time(min)": 31,
        "bike_std_time(min)": 13
    },
    {
        "spot": "西門紅樓",
        "std_time(min)": 8,
        "trans_std_time(min)": 21,
        "walk_std_time(min)": 64,
        "bike_std_time(min)": 23
    },
    {
        "spot": "西門町",
        "std_time(min)": 8,
        "trans_std_time(min)": 23,
        "walk_std_time(min)": 63,
        "bike_std_time(min)": 24
    },
    {
        "spot": "剝皮寮",
        "std_time(min)": 9,
        "trans_std_time(min)": 29,
        "walk_std_time(min)": 77,
        "bike_std_time(min)": 29
    },
    {
        "spot": "廣州街觀光夜市",
        "std_time(min)": 8,
        "trans_std_time(min)": 38,
        "walk_std_time(min)": 83,
        "bike_std_time(min)": 30
    },
    {
        "spot": "華西街夜市",
        "std_time(min)": 9,
        "trans_std_time(min)": 32,
        "walk_std_time(min)": 79,
        "bike_std_time(min)": 29
    },
    {
        "spot": "西昌街青草巷",
        "std_time(min)": 10,
        "trans_std_time(min)": 36,
        "walk_std_time(min)": 79,
        "bike_std_time(min)": 29
    },
    {
        "spot": "青山宮",
        "std_time(min)": 8,
        "trans_std_time(min)": 32,
        "walk_std_time(min)": 76,
        "bike_std_time(min)": 29
    },
    {
        "spot": "故宮博物院",
        "std_time(min)": 12,
        "trans_std_time(min)": 57,
        "walk_std_time(min)": 120,
        "bike_std_time(min)": 34
    },
    {
        "spot": "兒童新樂園",
        "std_time(min)": 9,
        "trans_std_time(min)": 54,
        "walk_std_time(min)": 107,
        "bike_std_time(min)": 38
    },
    {
        "spot": "天母古道",
        "std_time(min)": 16,
        "trans_std_time(min)": 64,
        "walk_std_time(min)": 162,
        "bike_std_time(min)": 59
    },
    {
        "spot": "翠峰瀑布",
        "std_time(min)": 24,
        "trans_std_time(min)": 84,
        "walk_std_time(min)": 196,
        "bike_std_time(min)": 79
    },
    {
        "spot": "北投溫泉博物館",
        "std_time(min)": 18,
        "trans_std_time(min)": 74,
        "walk_std_time(min)": 176,
        "bike_std_time(min)": 57
    },
    {
        "spot": "硫磺谷遊憩區",
        "std_time(min)": 20,
        "trans_std_time(min)": 76,
        "walk_std_time(min)": 203,
        "bike_std_time(min)": 71
    },
    {
        "spot": "亞尼克夢想村",
        "std_time(min)": 20,
        "trans_std_time(min)": 72,
        "walk_std_time(min)": 217,
        "bike_std_time(min)": 91
    },
    {
        "spot": "北投圖書館",
        "std_time(min)": 18,
        "trans_std_time(min)": 73,
        "walk_std_time(min)": 174,
        "bike_std_time(min)": 57
    },
    {
        "spot": "淡水老街",
        "std_time(min)": 26,
        "trans_std_time(min)": 76,
        "walk_std_time(min)": 269,
        "bike_std_time(min)": 75
    },
    {
        "spot": "淡水禮拜堂",
        "std_time(min)": 26,
        "trans_std_time(min)": 85,
        "walk_std_time(min)": 278,
        "bike_std_time(min)": 79
    },
    {
        "spot": "淡水小白宮",
        "std_time(min)": 26,
        "trans_std_time(min)": 90,
        "walk_std_time(min)": 284,
        "bike_std_time(min)": 83
    },
    {
        "spot": "淡水紅毛城",
        "std_time(min)": 28,
        "trans_std_time(min)": 90,
        "walk_std_time(min)": 285,
        "bike_std_time(min)": 80
    },
    {
        "spot": "淡水滬尾礮臺",
        "std_time(min)": 28,
        "trans_std_time(min)": 98,
        "walk_std_time(min)": 298,
        "bike_std_time(min)": 85
    },
    {
        "spot": "淡水漁人碼頭",
        "std_time(min)": 30,
        "trans_std_time(min)": 111,
        "walk_std_time(min)": 318,
        "bike_std_time(min)": 90
    },
    {
        "spot": "觀海長堤",
        "std_time(min)": 26,
        "trans_std_time(min)": 114,
        "walk_std_time(min)": 297,
        "bike_std_time(min)": 80
    },
    {
        "spot": "十三行博物館",
        "std_time(min)": 24,
        "trans_std_time(min)": 99,
        "walk_std_time(min)": 302,
        "bike_std_time(min)": 83
    },
    {
        "spot": "左岸公園",
        "std_time(min)": 24,
        "trans_std_time(min)": 106,
        "walk_std_time(min)": 272,
        "bike_std_time(min)": 75
    },
    {
        "spot": "烏來吊橋",
        "std_time(min)": 35,
        "trans_std_time(min)": 102,
        "walk_std_time(min)": 334,
        "bike_std_time(min)": 112
    },
    {
        "spot": "烏來老街",
        "std_time(min)": 40,
        "trans_std_time(min)": 104,
        "walk_std_time(min)": 337,
        "bike_std_time(min)": 112
    },
    {
        "spot": "林業生活館",
        "std_time(min)": 45,
        "trans_std_time(min)": 129,
        "walk_std_time(min)": 362,
        "bike_std_time(min)": 121
    },
    {
        "spot": "烏來瀑布",
        "std_time(min)": 35,
        "trans_std_time(min)": 103,
        "walk_std_time(min)": 333,
        "bike_std_time(min)": 111
    },
    {
        "spot": "雲仙樂園",
        "std_time(min)": 45,
        "trans_std_time(min)": 137,
        "walk_std_time(min)": 370,
        "bike_std_time(min)": 125
    },
    {
        "spot": "內洞森林遊樂區",
        "std_time(min)": 35,
        "trans_std_time(min)": 103,
        "walk_std_time(min)": 333,
        "bike_std_time(min)": 111
    },
    {
        "spot": "青立方咖啡店",
        "std_time(min)": 28,
        "trans_std_time(min)": 126,
        "walk_std_time(min)": 183,
        "bike_std_time(min)": 85
    },
    {
        "spot": "泰雅民族博物館",
        "std_time(min)": 40,
        "trans_std_time(min)": 104,
        "walk_std_time(min)": 337,
        "bike_std_time(min)": 112
    },
    {
        "spot": "銀河洞嶺月登山步道",
        "std_time(min)": 26,
        "trans_std_time(min)": 133,
        "walk_std_time(min)": 191,
        "bike_std_time(min)": 78
    },
    {
        "spot": "烏來台車",
        "std_time(min)": 40,
        "trans_std_time(min)": 110,
        "walk_std_time(min)": 342,
        "bike_std_time(min)": 116
    },
    {
        "spot": "十三層遺址",
        "std_time(min)": 35,
        "trans_std_time(min)": 139,
        "walk_std_time(min)": 518,
        "bike_std_time(min)": 146
    },
    {
        "spot": "茶壺山步道",
        "std_time(min)": 40,
        "trans_std_time(min)": 125,
        "walk_std_time(min)": 512,
        "bike_std_time(min)": 162
    },
    {
        "spot": "黃金博物館",
        "std_time(min)": 45,
        "trans_std_time(min)": 114,
        "walk_std_time(min)": 502,
        "bike_std_time(min)": 165
    },
    {
        "spot": "九份老街",
        "std_time(min)": 35,
        "trans_std_time(min)": 100,
        "walk_std_time(min)": 472,
        "bike_std_time(min)": 141
    },
    {
        "spot": "忘憂谷",
        "std_time(min)": 28,
        "trans_std_time(min)": 87,
        "walk_std_time(min)": 434,
        "bike_std_time(min)": 117
    },
    {
        "spot": "報時山步道",
        "std_time(min)": 40,
        "trans_std_time(min)": 122,
        "walk_std_time(min)": 510,
        "bike_std_time(min)": 162
    },
    {
        "spot": "無耳茶壺山",
        "std_time(min)": 40,
        "trans_std_time(min)": 125,
        "walk_std_time(min)": 512,
        "bike_std_time(min)": 162
    },
    {
        "spot": "侯硐貓村",
        "std_time(min)": 35,
        "trans_std_time(min)": 91,
        "walk_std_time(min)": 467,
        "bike_std_time(min)": 129
    }
]



if __name__ == '__main__':
    print(update_Location_data(json_temp))