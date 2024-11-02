from df_generation_for_dashboard import gen_df_stay, gen_df_in, gen_df_out, gen_df_diff
import pydeck as pdk

def vis_stay_2d(day, time):
    df = gen_df_stay(day, time)
    
    layer = pdk.Layer(
        'PolygonLayer', # 사용할 Layer 타입
        df, # 시각화에 쓰일 데이터프레임
        get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
        get_fill_color='[255, 255*(1-scaled_pop_density), 255*(1-scaled_pop_density)]', ## or scaled_pop
        get_line_color='[0, 0, 0]', # 각 데이터 별 rgb 또는 rgba 값 (0~255) [경계선]
        get_line_width=50, # 경계선 굵기
        pickable=True, # 지도와 interactive 한 동작 on
        auto_highlight=True # 마우스 오버(hover) 시 박스 출력
    )

    # Set the viewport location
    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    #마우스 오버시 툴팁 columns 출력
    tooltip = {
        "text": "행정지: {name} \n행정동코드: {code} \n인구: {pop}"    
    }

    # Render
    stay_2d = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
    return stay_2d

def vis_stay_3d(day, time):
    df = gen_df_stay(day, time)
    
    layer = pdk.Layer(
        'PolygonLayer', # 사용할 Layer 타입
        df, # 시각화에 쓰일 데이터프레임
        get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
        get_fill_color='[255, 255*(1-scaled_pop_density), 255*(1-scaled_pop_density)]', ## or scaled_pop
        get_line_color='[0, 0, 0]',
        pickable=True, # 지도와 interactive 한 동작 on
        auto_highlight=True, # 마우스 오버(hover) 시 박스 출력
        extruded= True, #3D plot
        get_elevation='scaled_pop_density', ## or scaled_pop
        elevation_scale=6000, #elevation scale
        wireframe=True #경계선 표시
    )
    
    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    view_state.bearing=15 #시점 좌우 각도
    view_state.pitch=45 #시점 상하 각도

    tooltip = {
        "text": "행정지: {name} \n행정동코드: {code} \n인구: {pop}"    
    }

    stay_3d = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
    return stay_3d

def vis_in_2d(day, time, code, alpha):
    df = gen_df_stay(day, time)
    df_in = gen_df_in(day, time, code, alpha)
    
    layer = pdk.Layer(# od in data Line layer
        'LineLayer',
        df_in, # od in dataframe
        get_source_position='[from_lon, from_lat]', #from position
        get_target_position='[to_lon, to_lat]', #to position
        get_width ='3*trunc_scaled_pop', ## or scaled_pop
        get_color='[255*scaled_pop, 0, 0]',
        pickable=True, # interactive map
        auto_highlight=True, #mouse over
        highlight_color=[255, 255, 0] #mouse over color
    )

    layerP = pdk.Layer( #배경 행정구 그림
        'PolygonLayer', 
        df,
        get_polygon='coordinates',
        get_fill_color='[255, 255, 255]',
        get_line_color='[0, 0, 0]',
        get_line_width=100,
        opacity=0.1
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    tooltip = {
        "text": "from: {from_region} \nto: {to_region} \n인구수: {pop}"    
    }

    od_in_2d = pdk.Deck(layers=[layerP,layer], initial_view_state=view_state, tooltip=tooltip)
    return od_in_2d

def vis_in_3d(day, time, code, alpha):
    df = gen_df_stay(day, time)
    df_in = gen_df_in(day, time, code, alpha)
    
    layer = pdk.Layer(
        'ArcLayer',
        df_in,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width ='3*trunc_scaled_pop', ## or scaled_pop
        get_source_color='[0, 0, 0]', #출발 rgb
        get_target_color='[255*scaled_pop, 0, 0]', #도착 rgb
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0]
    )
    
    layerP = pdk.Layer( #배경 행정구 그림
        'PolygonLayer', 
        df,
        get_polygon='coordinates',
        get_fill_color='[255, 255, 255]',
        get_line_color='[0, 0, 0]',
        get_line_width=100,
        opacity=0.1
    )
    
    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    view_state.bearing = 15
    view_state.pitch = 45

    tooltip = {
        "text": "from: {from_region} \nto: {to_region} \n인구수: {pop}"    
    }

    od_in_3d = pdk.Deck(layers=[layerP,layer], initial_view_state=view_state, tooltip=tooltip)
    return od_in_3d

def vis_out_2d(day, time, code, alpha):
    df = gen_df_stay(day, time)
    df_out = gen_df_out(day, time, code, alpha)
    
    layer = pdk.Layer(
        'LineLayer',
        df_out,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width ='3*trunc_scaled_pop', ## or scaled_pop
        get_color='[0, 0, 255*scaled_pop]',
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0]
    )
    
    layerP = pdk.Layer( #배경 행정구 그림
        'PolygonLayer', 
        df,
        get_polygon='coordinates',
        get_fill_color='[255, 255, 255]',
        get_line_color='[0, 0, 0]',
        get_line_width=100,
        opacity=0.1
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    tooltip = {
        "text": "from: {from_region} \nto: {to_region} \n인구수: {pop}"    
    }

    od_out_2d = pdk.Deck(layers=[layerP,layer], initial_view_state=view_state, tooltip=tooltip)
    return od_out_2d

def vis_out_3d(day, time, code, alpha):
    df = gen_df_stay(day, time)
    df_out = gen_df_out(day, time, code, alpha)
    
    layer = pdk.Layer(
        'ArcLayer',
        df_out,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width ='3*trunc_scaled_pop', ## or scaled_pop
        get_source_color='[0, 0, 0]',
        get_target_color='[0, 0, 255*scaled_pop]',
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0]
    )
    
    layerP = pdk.Layer( #배경 행정구 그림
        'PolygonLayer', 
        df,
        get_polygon='coordinates',
        get_fill_color='[255, 255, 255]',
        get_line_color='[0, 0, 0]',
        get_line_width=100,
        opacity=0.1
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    view_state.bearing = 15
    view_state.pitch = 45

    tooltip = {
        "text": "from: {from_region} \nto: {to_region} \n인구수: {pop}"    
    }

    od_out_3d = pdk.Deck(layers=[layerP,layer], initial_view_state=view_state, tooltip=tooltip)
    return od_out_3d

def vis_diff_2d(day, time, code, alpha):
    df = gen_df_stay(day, time)
    df_diff = gen_df_diff(day, time, code, alpha)
    
    layer = pdk.Layer(
        'LineLayer',
        df_diff,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width ='3*trunc_abs_scaled_pop', ## or abs_scaled_pop 
        get_color='[255*scaled_pop_p, 0, 255*scaled_pop_m]', #차이의 절댓값에 굵기 비례, 차이가 양수일때 red 음수일때 blue
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0]
    )
    
    layerP = pdk.Layer( #배경 행정구 그림
        'PolygonLayer', 
        df,
        get_polygon='coordinates',
        get_fill_color='[255, 255, 255]',
        get_line_color='[0, 0, 0]',
        get_line_width=100,
        opacity=0.1
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    tooltip = {
        "text": "from: {from_region} \nto: {to_region} \n인구수: {pop}"    
    }

    od_diff_2d = pdk.Deck(layers=[layerP,layer], initial_view_state=view_state, tooltip=tooltip)
    return od_diff_2d

def vis_diff_3d(day, time, code, alpha):
    df = gen_df_stay(day, time)
    df_diff = gen_df_diff(day, time, code, alpha)
    
    layer = pdk.Layer(
        'ArcLayer',
        df_diff,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width ='3*trunc_abs_scaled_pop', ## or abs_scaled_pop
        get_source_color='[0, 0, 255*scaled_pop_m]',
        get_target_color='[255*scaled_pop_p, 0, 0]',
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0]
    )
    
    layerP = pdk.Layer( #배경 행정구 그림
        'PolygonLayer', 
        df,
        get_polygon='coordinates',
        get_fill_color='[255, 255, 255]',
        get_line_color='[0, 0, 0]',
        get_line_width=100,
        opacity=0.1
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    view_state.bearing = 15
    view_state.pitch = 45

    tooltip = {
        "text": "from: {from_region} \nto: {to_region} \n인구수: {pop}"    
    }

    od_diff_3d = pdk.Deck(layers=[layerP,layer], initial_view_state=view_state, tooltip=tooltip)
    return od_diff_3d