import pandas as pd
import glob

def stay(day, time):
    csv_dir = glob.glob(f"data/**/stay_{day}_1.csv", recursive = True)
    data = pd.read_csv(csv_dir[0])
    
    # 서울시에 해당하는 행만 필터링
    data = data[(data['hdong_cd'] >= 1100000000) & (data['hdong_cd'] <= 1174070000)] 
    
    # 시간 형식을 변환 (예: 13:00 -> 13)
    data.loc[:, 'time'] = pd.to_datetime(data['time'], format='%H:%M').dt.hour 
    
    # input 시간에 해당하는 데이터만 필터링
    data = data[data['time'].astype("str") == time]
    
    # 행정동 코드와 시간을 기준으로 그룹화하고, 체류인원 합산
    data_grouped = data.groupby(['hdong_cd', 'time'], as_index=False).agg({'stay_cnts': 'sum'})
    
    # 결과를 행정동 코드와 시간으로 정렬
    data_grouped = data_grouped.sort_values(by=['hdong_cd'])
    data_grouped = data_grouped.drop(columns=['time'])
    return data_grouped