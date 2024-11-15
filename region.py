import pandas as pd
import importlib
import data_rev
importlib.reload(data_rev)
data = data_rev.df_revised
data[["시도명", "시군구명", "읍면동명"]] = data["name"].str.split(" ", expand=True)
data.head()

# data = pd.read_csv("data/KIKmix_20230701.csv", usecols=[0, 1, 2, 3]).dropna()
# data = data.drop_duplicates(subset=["읍면동명"])

region_1_list = ["서울특별시"]

def display_region_2(region_1):
    region_2_list = data[data["시도명"] == region_1].drop_duplicates(subset=["시군구명"])["시군구명"].tolist()
    return region_2_list

def display_region_3(region_1, region_2):
    region_3_list = data[(data["시도명"] == region_1) & (data["시군구명"] == region_2)].drop_duplicates(subset=["읍면동명"])["읍면동명"].tolist()
    return region_3_list

def region_to_code(region_1, region_2, region_3):
    code = int(data[(data["시도명"] == region_1) & (data["시군구명"] == region_2) & (data["읍면동명"] == region_3)]["code"].values)
    return code

def code_to_region(code):
    code = str(code)
    region_1 = data[data["code"] == code].iloc[0]["시도명"]
    region_2 = data[data["code"] == code].iloc[0]["시군구명"]
    region_3 = data[data["code"] == code].iloc[0]["읍면동명"]
    region = f"{region_1} {region_2} {region_3}"
    return region