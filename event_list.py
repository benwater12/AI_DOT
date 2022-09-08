from datetime import datetime,date,timedelta
import pandas as pd
from time_util import *
pd.options.mode.chained_assignment = None  # default='warn'
def get_event_list(dataframe,date_iso_str):
    event_dataframe=dataframe
    event_dataframe['開始時間'] = pd.to_datetime(event_dataframe['開始時間'], format="%Y-%m-%d %H:%M:%S+08:00")
    event_dataframe['結束時間'] = pd.to_datetime(event_dataframe['結束時間'], format="%Y-%m-%d %H:%M:%S+08:00")
    head_date=event_dataframe['開始時間'].min()
    tail_date=event_dataframe['結束時間'].max()
    current_date = datetime.fromisoformat(date_iso_str)
    current_date = date_basic_transform(head_date,tail_date,current_date)
    before_iso_datetime,after_iso_datetime  =get_span_date_tuple(current_date,14,head_date,tail_date)
    target_mask = (event_dataframe["結束時間"] >= before_iso_datetime) & (event_dataframe["開始時間"] <= after_iso_datetime)
    target_filtered_dataframe = event_dataframe.loc[target_mask]
    try:
        target_filtered_dataframe.drop(columns=["結束時間", "開始時間","_id"],inplace=True)
        event_list=target_filtered_dataframe.values.tolist()
    except:
        return None
    return event_list
        


