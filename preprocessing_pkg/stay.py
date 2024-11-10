import pandas as pd
import glob
import zipfile

stay_zip = zipfile.ZipFile("data/stay.zip")
stay_list = stay_zip.namelist()

def stay(date: int, time: int):
    # 해당 날짜 csv 파일 압축 풀고 읽기
    if not glob.glob(f"data/**/stay_{date}_1.csv", recursive=True):
        target = [file for file in stay_list if str(date) in file][0]
        stay_zip.extract(target, "data/stay")
        csv_dir = f"data/stay/{target}"
    else:
        csv_dir = glob.glob(f"data/**/stay_{date}_1.csv", recursive=True)[0]
    
    data = pd.read_csv(csv_dir)
    
    # 서울시에 해당하는 행만 필터링
    data["hdong_cd"] = data["hdong_cd"].astype("str")
    data = data[data["hdong_cd"].str.startswith("11")]
    
    # 시간 형식을 변환 (예: 13:00 -> 13)
    data.loc[:, 'time'] = pd.to_datetime(data['time'], format='%H:%M').dt.hour 
    
    # input 시간에 해당하는 데이터만 필터링
    data = data[data['time'].astype("str") == str(time)]
    
    # 행정동 코드와 시간을 기준으로 그룹화하고, 체류인원 합산
    data_grouped = data.groupby(['hdong_cd', 'time'], as_index=False).agg({'stay_cnts': 'sum'})
    
    # 결과를 행정동 코드와 시간으로 정렬
    data_grouped = data_grouped.sort_values(by=['hdong_cd'])
    data_grouped = data_grouped.drop(columns=['time'])
    return data_grouped