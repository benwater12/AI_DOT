from datetime import datetime
import pandas as pd
from time_util import *

def like_percentage_calculate(dataframe,date_iso_str):
    if dataframe.empty:
        return 0,0
    like_dataframe=dataframe
    like_dataframe["count.like"] = pd.to_numeric(like_dataframe["count.like"].str.replace(",", ""))
    like_dataframe['posttime'] = pd.to_datetime(like_dataframe['posttime'], format="%Y/%m/%d %H:%M")
    average = like_dataframe["count.like"].mean()
    like_dataframe = like_dataframe[like_dataframe["count.like"] < average*5]

    head_date = like_dataframe['posttime'].min()
    tail_date = like_dataframe['posttime'].max()
    current_date = datetime.fromisoformat(date_iso_str)
    current_date = date_basic_transform(head_date,tail_date,current_date)
    before_iso_datetime,after_iso_datetime = get_span_date_tuple(current_date,14,head_date,tail_date)
    master_before_iso_datetime,master_after_iso_datetime = get_span_date_tuple(current_date,60,head_date,tail_date)
    
    target_mask = (like_dataframe["posttime"] >= before_iso_datetime) & (like_dataframe["posttime"] <= after_iso_datetime)
    target_filtered_like_dataframe = like_dataframe.loc[target_mask]
    master_mask = (like_dataframe["posttime"] >= master_before_iso_datetime) & (like_dataframe["posttime"] <= master_after_iso_datetime)
    master_filtered_like_dataframe = like_dataframe.loc[master_mask]
    if master_filtered_like_dataframe["count.like"].sum()==0:
        return 0,0
    percentage = target_filtered_like_dataframe["count.like"].sum()/master_filtered_like_dataframe["count.like"].sum()
    # print(pd.to_numeric(target_fixed_series),pd.to_numeric(master_fixed_series))
    return percentage,len(target_filtered_like_dataframe["count.like"])

    
if __name__ == '__main__':
    print("test for like_calcualte")
    csv_dataframe=pd.read_csv("C:\\Users\\benwa\\MasterPJ\\mongodb\\like過濾一覽 信義 國父紀念館.csv",encoding="utf-8")
    print(like_percentage_calculate(csv_dataframe.to_json(),"2021-04-07"))


