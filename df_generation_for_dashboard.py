import pandas as pd
import numpy as np
import data_rev
from preprocessing_pkg import stay, od
from region import code_to_region

def trunc(data,alpha): #alpha is truncation constant: data < alpha => data = 0
    data=data.to_numpy()
    data=data.copy()
    for i in range(len(data)):
        if data[i]-alpha<0: data[i]=0
    return data

def gen_df_stay(day, time):
    df = data_rev.df_revised
    df2 = stay.stay(day, time)
    df2['hdong_cd'] = df2['hdong_cd'].astype(str)
    df = pd.merge(df, df2, left_on='code', right_on='hdong_cd', how='inner')
    df = df.drop(columns=['hdong_cd'])
    df = df.rename(columns={'stay_cnts': 'pop'})
    
    seoularea=pd.read_csv('data/seoularea.csv')
    seoularea=seoularea[['행정동코드','면적']]
    
    seoularea.columns=['code','area']
    seoularea.head()
    sc = 150000
    
    df['pop'] = df["pop"].fillna(0)
    df['scaled_pop']=df['pop'] / sc  ##scale parameter
    df['area']=seoularea['area']
    df['pop_density']=df['pop']/df['area']
    df['scaled_pop_density']=df['pop'] / sc
    
    return df

def gen_arr(day, time):
    df = gen_df_stay(day, time)

    #central lon, lat 계산
    coordinates=df['coordinates'].to_numpy()
    lon = np.zeros(426);lat = np.zeros(426)
    for i in range(426):
        lonlat=np.mean(coordinates[i],axis=0)
        lon[i],lat[i]=lonlat[0],lonlat[1]  
    df['lat']=lat
    df['lon']=lon
    df1=df[['code','lat','lon']]
    
    arr=df1.to_numpy()
    arr_ft=np.zeros((426*426,6))
    for i,f in enumerate(arr):
        for j,t in enumerate(arr):
            arr_ft[i*426+j]=np.hstack((f,t))
    
    return arr
     
def gen_df_in(day, time, code_int, alpha):
    arr = gen_arr(day, time)
    
    other_coord=list()
    for i in arr:
        if i[0]!=code_int: other_coord.append(i)
        else: coordlst=i
    coord=coordlst
    for i in range(425-1):
        coord=np.vstack((coord,coordlst))
    
    arr_in=np.hstack((other_coord,coord))
    df_in=pd.DataFrame(arr_in)
    df_in.columns = ['from','from_lat','from_lon','to','to_lat','to_lon']
    
    sc = 150
    
    in_pop = od.od_in(date=day, end_time=time, dest=code_int, from_seoul=True)
    df_in = pd.merge(df_in, in_pop, how="left", left_on="from", right_on="origin_hdong_cd")
    del df_in["origin_hdong_cd"]
    df_in.rename(columns={"od_cnts": "pop"}, inplace=True)
    df_in['pop'] = df_in['pop'].fillna(0)
    df_in['scaled_pop']=df_in['pop'] / sc
    df_in['trunc_scaled_pop']=trunc(df_in['scaled_pop'],alpha)
    
    df_in['from_region'] = df_in['from'].apply(code_to_region)
    df_in['to_region'] = df_in['to'].apply(code_to_region)
    
    return df_in

def gen_df_out(day, time, code_int, alpha):
    arr = gen_arr(day, time)
    
    other_coord=list()
    for i in arr:
        if i[0]!=code_int: other_coord.append(i)
        else: coordlst=i
    coord=coordlst
    for i in range(425-1):
        coord=np.vstack((coord,coordlst))
        
    arr_out=np.hstack((coord,other_coord))
    df_out=pd.DataFrame(arr_out)
    df_out.columns = ['from','from_lat','from_lon','to','to_lat','to_lon']
    
    sc = 150
    
    out_pop = od.od_out(date=day, start_time=time, origin=code_int, to_seoul=True)
    df_out = pd.merge(df_out, out_pop, how="left", left_on="to", right_on="dest_hdong_cd")
    del df_out["dest_hdong_cd"]
    df_out.rename(columns={"od_cnts": "pop"}, inplace=True)
    df_out['pop'] = df_out["pop"].fillna(0)
    df_out['scaled_pop']=df_out['pop'] / sc
    df_out['trunc_scaled_pop']=trunc(df_out['scaled_pop'],alpha)
    
    df_out['from_region'] = df_out['from'].apply(code_to_region)
    df_out['to_region'] = df_out['to'].apply(code_to_region) 
    
    return df_out 

def plus(data):
    data=data.to_numpy()
    data=data.copy()
    for i in range(len(data)):
        if data[i]<0: data[i]=0
    return data

def minus(data): 
    data=data.to_numpy()
    data=data.copy()
    for i in range(len(data)):
        if data[i]>0: data[i]=0
    return -1*data

def gen_df_diff(day, time, code_int, alpha):
    df_diff = gen_df_in(day, time, code_int, alpha)
    df_out = gen_df_out(day, time, code_int, alpha)
    df_diff["pop"] = df_diff["pop"] - df_out["pop"]
    
    sc = 150
    
    df_diff['scaled_pop']=df_diff['pop'] / sc
    df_diff['scaled_pop_p']=plus(df_diff['scaled_pop'])
    df_diff['scaled_pop_m']=minus(df_diff['scaled_pop'])
    df_diff['trunc_scaled_pop']=trunc(abs(df_diff['scaled_pop']),alpha)
    df_diff['abs_scaled_pop']=abs(df_diff['scaled_pop'])
    df_diff['trunc_abs_scaled_pop']=abs(df_diff['trunc_scaled_pop'])  
    
    df_diff['from_region'] = df_diff['from'].apply(code_to_region)
    df_diff['to_region'] = df_diff['to'].apply(code_to_region)
    
    return df_diff  
