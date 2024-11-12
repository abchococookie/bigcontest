import pandas as pd
import glob
import zipfile
import gdown

od_sep_id = "1ybpsiqFpOJoypOYryJs_FQs1Z6RctL6F"
od_oct_id = "1ZPBWomi-ghDy0S8FoHk0KLZBDkJwq9ce"

od_sep_download = f"https://drive.google.com/uc?id={od_sep_id}"
od_oct_download = f"https://drive.google.com/uc?id={od_oct_id}"

od_sep_path = "data/od_sep.zip"
od_oct_path = "data/od_oct.zip"

gdown.download(od_sep_download, od_sep_path, quiet=False)
gdown.download(od_oct_download, od_oct_path, quiet=False)

od_zip_sep = zipfile.ZipFile("data/od_sep.zip")
od_zip_oct = zipfile.ZipFile("data/od_oct.zip")
od_list = od_zip_sep.namelist() + od_zip_oct.namelist()

def od_in(date: int, end_time: int, dest: int, from_seoul: bool):
    # 해당 날짜 csv 파일 압축 풀고 읽기
    if not glob.glob(f"data/**/od_{date}_1.csv", recursive=True):
        target = [file for file in od_list if str(date) in file][0]
        if "202309" in target:
            od_zip_sep.extract(target, "data/od")
        else:
            od_zip_oct.extract(target, "data/od")
        csv_dir = f"data/od/{target}"
    else:
        csv_dir = glob.glob(f"data/**/od_{date}_1.csv", recursive=True)[0]
    
    df = pd.read_csv(csv_dir)
    
    # 행정동 코드 문자열로 바꾸기 (시각화 때 merged_df 생성 위해)
    df["dest_hdong_cd"] = df["dest_hdong_cd"].astype(str)
    df["origin_hdong_cd"] = df["origin_hdong_cd"].astype(str)
    
    # origin_hdong_cd 서울시 한정
    if from_seoul == True:
        df = df[df["origin_hdong_cd"].str.startswith("11")]
    
    # dest_hdong_cd 필터링 & end_time 필터링
    df.loc[:, 'end_time'] = pd.to_datetime(df['end_time'], format='%H:%M').dt.hour 
    df = df[(df["dest_hdong_cd"] == str(dest)) & (df["end_time"].astype("str") == str(end_time))]
    
    # 해당되는 모든 데이터의 이동인원 summation
    df = df.groupby("origin_hdong_cd")["od_cnts"].sum().sort_values(ascending=False).reset_index()
    
    return df


def od_out(date: int, start_time: int, origin: int, to_seoul: bool):
    # 해당 날짜 csv 파일 압축 풀고 읽기
    if not glob.glob(f"data/**/od_{date}_1.csv", recursive=True):
        target = [file for file in od_list if str(date) in file][0]
        if "202309" in target:
            od_zip_sep.extract(target, "data/od")
        else:
            od_zip_oct.extract(target, "data/od")
        csv_dir = f"data/od/{target}"
    else:
        csv_dir = glob.glob(f"data/**/od_{date}_1.csv", recursive=True)[0]
    
    df = pd.read_csv(csv_dir)
    
    # 행정동 코드 문자열로 바꾸기 (시각화 때 merged_df 생성 위해)
    df["dest_hdong_cd"] = df["dest_hdong_cd"].astype(str)
    df["origin_hdong_cd"] = df["origin_hdong_cd"].astype(str)
    
    # dest_hdong_cd 서울시 한정
    if to_seoul == True:
        df = df[df["dest_hdong_cd"].str.startswith("11")]
        
    # origin_hdong_cd 필터링 & start_time 필터링
    df.loc[:, 'start_time'] = pd.to_datetime(df['start_time'], format='%H:%M').dt.hour 
    df = df[(df["origin_hdong_cd"] == str(origin)) & (df["start_time"].astype("str") == str(start_time))]
    
    # 해당되는 모든 데이터의 이동인원 summation
    df = df.groupby("dest_hdong_cd")["od_cnts"].sum().sort_values(ascending=False).reset_index()

    
    return df