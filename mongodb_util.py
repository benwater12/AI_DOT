from pymongo import MongoClient
def get_database_obj(database_name_str):
    CONNECTION_STRING = "DONTKNOW"
    client = MongoClient(CONNECTION_STRING)
    return client[database_name_str]

def get_sightseeing_host_database_str(sightseeing_location):
      minor_location_collection=get_database_obj("Hank_Tour")["Main_Locations"]
      main_location_dict=minor_location_collection.find_one({"景點":sightseeing_location})
      return main_location_dict["大地點"]

def get_by_address_dbname_str(local_address):
      minor_location_collection=get_database_obj("Hank_Tour")["Locations"]
      main_location_dict=minor_location_collection.find_one({"地址區域":local_address})
      return main_location_dict["地點"]

def get_location_str_format(location_str):
    location_list=location_str.split("、")
    location_processed_list=[]
    format_str=None
    for location in location_list:
        location_processed_list.append(location[:len(location)-1])
    if len(location_processed_list)>1:
        format_str="_".join(location_processed_list)
        return format_str
    format_str=location_processed_list[0]
    if format_str=="瑞芳":
        format_str="九份"
    return format_str