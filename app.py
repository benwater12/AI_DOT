from datetime import timedelta
from flask import Flask,request,jsonify,abort
from pymongo import MongoClient
from like_calulation import like_percentage_calculate
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import hashlib
from flask_cors import CORS
from bson import json_util,ObjectId
import json
from like_calulation import like_percentage_calculate
from event_list import get_event_list
import pandas as pd
from weather_request import get_weather_data
from mongodb_util import *
from time_util import js_date_to_datetime
from Hank_travel_time import *
import logging

logging.basicConfig(filename='log/flask.log', encoding='utf-8', level=logging.WARNING)
logger = logging.getLogger('waitress')
logger.setLevel(logging.WARNING)
jwt = JWTManager()
app = Flask(__name__)
CORS(app,resources={r"/.*": {"origins": ["http://172.105.239.153"]}})
# 設定 JWT 密鑰
app.config['JWT_SECRET_KEY'] = 'XXXXX'
app.config['CORS_HEADERS'] = 'Content-Type'
jwt.init_app(app)

# trusted_ips = ['172.105.239.153']
# @app.before_request
# def limit_remote_addr():
#     if request.remote_addr not in trusted_ips:
#         abort(404)  # Not Found

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/popularity",methods=["POST"])
def poplulatity():
    sight_name=str(request.json.get('location_str',None))
    db_name=get_sightseeing_host_database_str(sight_name)
    if db_name is None:
        return {"error":1}
    db=get_database_obj(str(db_name))
    name = "人潮"
    collection=db[name]
    poplulatity_list=collection.find_one({"地點":sight_name})

    return {"人潮清單":poplulatity_list["資料"]}


@app.route("/location_data",methods=["POST"])
def location_data():
    sight_name=str(request.json.get('location_str',None))
    db_name=get_sightseeing_host_database_str(sight_name)
    if db_name is None:
        return {"error":1}
    db=get_database_obj(str(db_name))
    name = "地點"
    collection=db[name]
    location_data=collection.find_one({"地點":sight_name})
    return {"地點資訊":location_data["資料"]}


@app.route("/event_list", methods=['POST'])
def event_list():
    date_str=request.json.get("date_str",None)
    general_location_str=str(request.json.get('general_location_str',None))
    general_location_str=get_by_address_dbname_str(general_location_str)
    db=get_database_obj(str(general_location_str))
    name = "活動" 
    collection=db[str(name)]
    cursor=collection.find({})
    dataframe =  pd.DataFrame(list(cursor))
    if dataframe.empty:
        return {"error":1}
    point_datetime=js_date_to_datetime(date_str)
    event_list=get_event_list(dataframe,point_datetime.isoformat())
    return {"event_list":event_list, "event_number":len(event_list)}


@app.route("/weather_data",methods=["POST"])
def weather_data():
    postoffice_location_str=request.json.get("location_str",None)
    date_str=request.json.get("date_str",None)
    point_datetime=js_date_to_datetime(date_str)
    weather_data_str=get_weather_data(point_datetime,postoffice_location_str)
    return {"weather_str":weather_data_str}


@app.route("/fame_percent", methods=['POST'])
def fame_percent():
    date_str=request.json.get("date_str",None)
    sight_name=str(request.json.get('location_str',None))
    db_name=get_sightseeing_host_database_str(sight_name)
    if db_name is None:
        return {"error":1}
    db=get_database_obj(str(db_name))
    name = "聲量"
    collection=db[str(name)]
    cursor=collection.find({"地點":sight_name})
    dataframe =  pd.DataFrame(list(cursor))
    point_datetime=js_date_to_datetime(date_str)
    percentage,total_article_num=like_percentage_calculate(dataframe,point_datetime.isoformat())
    return{"percetnage":percentage,"total_article_count":total_article_num}


@app.route("/put_new_user", methods=['POST'])
def Add_new_user():
    username=request.json.get("username",None)
    password=request.json.get("password",None)
    nickname=request.json.get("nickname",None)
    hash_processor = hashlib.new('sha256')
    hash_processor.update(bytes(str(password), "utf8"))
    hash_password = hash_processor.hexdigest()
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata=collection.find_one({"username":username})
    if userdata is not None:
        return {"message":"the email is used, please use another one."}
    collection.insert_one({"username":username,"password":hash_password,"name":nickname,"interest":[],"favspot":[]})
    return {"message":"successfully added user.","username":username}


@app.route("/insert_fav_spot", methods=['POST'])
def Insert_Fav_spot():
    userobjID_str = request.json.get('userobjID', None)
    fav_location_str = request.json.get('item_str', None)
    photo_str=request.json.get("photo",None)
    preface_str=request.json.get("preface",None)
    fav_location_dict_data={"location":fav_location_str,"photo":photo_str,"preface":preface_str}
    userobjID = ObjectId(userobjID_str)
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata_dict=collection.find_one({"_id":userobjID})
    fav_location_dict_list=userdata_dict["favspot"]
    if len(fav_location_dict_list)!=0: 
        for fav_location_dict in fav_location_dict_list:
            if fav_location_str == fav_location_dict["location"]:
                return{"message":"You already added this favspot"}
    fav_location_dict_list.append(fav_location_dict_data)
    new_fav_location_command= { "$set": { "favspot": fav_location_dict_list} }
    collection.update_one({"_id":userobjID},new_fav_location_command)
    return {"result":"We did it, added fav item" }

@app.route("/delete_interest", methods=['POST'])
def Delete_interest():
    userobjID_str = request.json.get('userobjID', None)
    insert_interest_str = request.json.get('item_str', None)
    userobjID = ObjectId(userobjID_str)
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata_dict=collection.find_one({"_id":userobjID})
    interest_list=userdata_dict["interest"]
    if insert_interest_str not in interest_list:
        return{"message":"You tried to remove something that doesn't exist"}
    interest_list.remove(insert_interest_str)
    new_insert_command = { "$set": { "interest": interest_list} }
    collection.update_one({"_id":userobjID},new_insert_command)
    return {"result":"We did it, removed inserted item" }

@app.route("/delete_Fav_spot", methods=['POST'])
def Delete_Fav_spot():
    userobjID_str = request.json.get('userobjID', None)
    fav_location_str = request.json.get('item_str', None)
    userobjID = ObjectId(userobjID_str)
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata_dict=collection.find_one({"_id":userobjID})
    fav_location_dict_list=userdata_dict["favspot"]
    if len(fav_location_dict_list)==0:
        return{"message":"the list is empty"}
    for fav_location_dict in fav_location_dict_list:
        if fav_location_str == fav_location_dict["location"]:
            break
        return{"message":"You tried to remove something that doesn't exist"}
    fav_location_dict_list.remove(fav_location_dict)
    new_fav_location_command= { "$set": { "favspot": fav_location_dict_list} }
    collection.update_one({"_id":userobjID},new_fav_location_command)
    return {"result":"We did it, remove fav item" }



@app.route("/fav_spot_list", methods=['POST'])
def Get_Fav_spot_list():
    userobjID_str = request.json.get('userobjID', None)
    userobjID = ObjectId(userobjID_str)
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata_dict=collection.find_one({"_id":userobjID})
    if userdata_dict is None:
        return {"error":1}
    return {"result":userdata_dict["favspot"]}

@app.route("/interest_list", methods=['POST'])
def Get_interest_list():
    userobjID_str = request.json.get('userobjID', None)
    userobjID = ObjectId(userobjID_str)
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata_dict=collection.find_one({"_id":userobjID})
    if userdata_dict is None:
        return {"error":1}
    return {"result":userdata_dict["interest"]}



@app.route("/login", methods=['POST'])
def login():
    username = request.json.get('username', None) 
    password = request.json.get('password', None) 
    hash_processor = hashlib.new('sha256')
    hash_processor.update(bytes(str(password), "utf8"))
    hash_password = hash_processor.hexdigest()
    db=get_database_obj("使用者資料庫")
    name = "使用者資料"
    collection=db[name]
    userdata_dict=collection.find_one({"password":hash_password,"username":username})
    if userdata_dict is None:
        return {"error":1}
    token_life_span=timedelta(hours=2)
    payload_dict={"id":userdata_dict["_id"],"userName":userdata_dict["username"],"name":userdata_dict["name"]}
    access_token = create_access_token(identity=json_util.dumps(payload_dict),expires_delta=token_life_span )
    return jsonify(access_token=access_token)

@app.route("/Travel_time", methods=['POST'])
def get_Travel_time():
    sight_name_str=str(request.json.get('location_str',None))
    date_str=str(request.json.get('date_str',None))
    # mode_str=str(request.json.get('mode_str',None))
    # mode_str: driving, walking, transit
    now_datetime=js_date_to_datetime(date_str)
    eta_dict=get_traffic_time(now_datetime,"台北市電腦商業同業公會",sight_name_str)
    # now_time_in_min=history_from_to(now_datetime,"台北市電腦商業同業公會",sight_name_str)
    db=get_database_obj("Hank_Tour")
    name = "Main_Locations" 
    collection=db[name]
    drive_time_in_minutes=collection.find_one({"景點":sight_name_str})["std_time(min)"]
    drive_score=traffic_time_cal(drive_time_in_minutes,eta_dict["drive_time(min)"])
    # walking_time_in_minutes=collection.find_one({"景點":sight_name_str})["walk_std_time(min)"]
    # walking_score=traffic_time_cal(walking_time_in_minutes,now_time_in_min["walking_time(min)"])
    # biking_time_in_minutes=collection.find_one({"景點":sight_name_str})["bike_std_time(min)"]
    # biking_score=traffic_time_cal(biking_time_in_minutes,now_time_in_min["biking_time(min)"])
    # transit_time_in_minutes=collection.find_one({"景點":sight_name_str})["trans_std_time(min)"]
    # transit_score=traffic_time_cal(transit_time_in_minutes,now_time_in_min["transit_time(min)"])
    # return {"drive_score":drive_score}
    return {"drive_score":drive_score,
    # "biking_score":biking_score,"transit_score":transit_score
    }


@app.route("/get_article", methods=['POST'])
def get_article():
  sight_name=str(request.json.get('sightseeing_location'))
  db_name_str=get_sightseeing_host_database_str(sight_name)
  if db_name_str is None:
    return {"error":1,"input":sight_name}
  db=get_database_obj(str(db_name_str))
  name = "文章"
  sightseeing_location="無"
  sightseeing_location=sight_name
  collection=db[str(name)]
  article_json = json_util.dumps(collection.find_one({"title":sightseeing_location}))
  return json.dumps(json.loads(article_json))


@app.route("/get_hotel_list", methods=['POST'])
def get_hotel_list():
  sight_name=str(request.json.get('sightseeing_location'))
  db_name_str=get_sightseeing_host_database_str(sight_name)
  if db_name_str is None:
    return {"error":1}
  db=get_database_obj(db_name_str)
  name = "住宿"
  sightseeing_location="無"
  sightseeing_location=request.json.get('sightseeing_location')
  collection=db[str(name)]
  hotel_list_json=json_util.dumps(collection.find_one({"景點":sightseeing_location})["附近旅館清單"])
  return hotel_list_json
  
@app.route("/sightdata", methods=['POST'])
def get_sight_datas():
    sight_name=str(request.json.get('sightseeing_location'))
    db_name_str=get_sightseeing_host_database_str(sight_name)
    name="地點"
    db=get_database_obj(db_name_str)
    collection=db[str(name)]
    sight_data_dict=collection.find_one({"地點":sight_name})["資料"]
    if sight_data_dict is None:
        return_msg={
            "error":"-1",
            "message":"this location doesn't exists on ptx."
        }
        return return_msg
    sight_data=json_util.dumps(sight_data_dict)
    return sight_data


def get_database_obj(database_name_str):
    CONNECTION_STRING = "SOMEWHEREYOURCONNECTIONSTR"
    client = MongoClient(CONNECTION_STRING)
    return client[database_name_str]

def get_sightseeing_host_database_str(sightseeing_location):
      minor_location_collection=get_database_obj("Hank_Tour")["Main_Locations"]
      main_location_dict=minor_location_collection.find_one({"景點":sightseeing_location})
      try:
        return main_location_dict["大地點"]
      except:
        return None


if __name__ == "__main__":
    from waitress import serve
    print("serving on 3007, using all host")
    serve(app, host="0.0.0.0", port=3007)
    # app.run(host='0.0.0.0', port=3007,debug=True)
