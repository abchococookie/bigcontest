import streamlit as st
import datetime
import logging

import region

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log')

# sidebar
with st.sidebar:
    st.title("빅콘 딸깍 🖱️")
    region_1 = st.selectbox("🧭 시/도를 선택하세요", options=region.region_1_list, key="region_1_selected")
    region_2 = st.selectbox("🧭 시/군/구를 선택하세요", options=region.display_region_2(st.session_state.region_1_selected), key="region_2_selected")
    region_3 = st.selectbox("🧭 읍/면/동을 선택하세요", options=region.display_region_3(st.session_state.region_1_selected, st.session_state.region_2_selected), key="region_3_selected")
    
with st.form("my form"):
    with st.sidebar:
        day = st.date_input("🗓️ 날짜를 선택하세요 (2023.09.01. ~ 10.15.)", datetime.date(2023, 10, 7))
        time = st.time_input("⏰ 시간대를 선택하세요", datetime.time(18, 0), step=datetime.timedelta(hours=1))
        alpha = st.number_input("🔢 절단계수를 입력하세요 (권장값: 0.1 ~ 0.3)", min_value=0.0, max_value=1.0, value=0.3)
        update = st.form_submit_button("확인")

code = region.find_code(st.session_state.region_1_selected, st.session_state.region_2_selected, st.session_state.region_3_selected)

# session initialization & update
if 'day' not in st.session_state:
    st.session_state['day'] = day.strftime("%Y%m%d")
if 'time' not in st.session_state:
    st.session_state['time'] = time.strftime("%H").lstrip("0")  # 한 자리로 변환
if 'region_1' not in st.session_state:
    st.session_state['region_1'] = region_1
if 'region_2' not in st.session_state:
    st.session_state['region_2'] = region_2
if 'region_3' not in st.session_state:
    st.session_state['region_3'] = region_3
if 'code' not in st.session_state:
    st.session_state['code'] = str(code)
if 'alpha' not in st.session_state:
    st.session_state['alpha'] = alpha
    
if update:
    st.session_state['day'] = day.strftime("%Y%m%d")
    st.session_state['time'] = time.strftime("%H").lstrip("0")  # 한 자리로 변환
    st.session_state['code'] = str(code)
    st.session_state['alpha'] = alpha
    st.rerun()

# main page
import BIGC_VIS_for_dashboard

tab1, tab2, tab3, tab4 = st.tabs(["STAY", "OD-IN", "OD-OUT", "OD-DIFF"])

with tab1:
    st.header("STAY Visualization")
    st.info(f"{day.strftime('%Y년 %m월 %d일')} {time.strftime('%H시')}의 인구수를 시각화하였습니다.", icon="ℹ️")
    try:
        st.subheader("STAY in 2D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_stay_2d(st.session_state['day'], st.session_state['time']))
        st.subheader("STAY in 3D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_stay_3d(st.session_state['day'], st.session_state['time']))
    except Exception as e:
        logging.error("Error in STAY Visualization: %s", e)
        st.error("해당 날짜 및 시간에 해당하는 데이터가 없습니다.", icon="🚨")

with tab2:
    st.header("OD-IN Visualization")
    st.info(f"{day.strftime('%Y년 %m월 %d일')} {time.strftime('%H시')}에 타 지역으로부터 {region_1} {region_2} {region_3}에 유입된 인구수를 시각화하였습니다.", icon="ℹ️")
    try:
        st.subheader("OD-IN in 2D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_in_2d(st.session_state['day'], st.session_state['time'], st.session_state['code'], st.session_state['alpha']))
        st.subheader("OD-IN in 3D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_in_3d(st.session_state['day'], st.session_state['time'], st.session_state['code'], st.session_state['alpha']))
    except Exception as e:
        logging.error("Error in STAY Visualization: %s", e)
        st.error("해당 날짜 및 시간에 해당하는 데이터가 없습니다.", icon="🚨")

with tab3:
    st.header("OD-OUT Visualization")
    st.info(f"{day.strftime('%Y년 %m월 %d일')} {time.strftime('%H시')}에 {region_1} {region_2} {region_3}으로부터 타 지역에 유출된 인구수를 시각화하였습니다.", icon="ℹ️")
    try:
        st.subheader("OD-OUT in 2D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_out_2d(st.session_state['day'], st.session_state['time'], st.session_state['code'], st.session_state['alpha']))
        st.subheader("OD-OUT in 3D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_out_3d(st.session_state['day'], st.session_state['time'], st.session_state['code'], st.session_state['alpha']))
    except Exception as e:
        logging.error("Error in STAY Visualization: %s", e)
        st.error("해당 날짜 및 시간에 해당하는 데이터가 없습니다.", icon="🚨")

with tab4:
    st.header("OD-DIFF Visualization")
    st.info(f"{day.strftime('%Y년 %m월 %d일')} {time.strftime('%H시')}에 {region_1} {region_2} {region_3}에서의 인구의 순이동을 시각화하였습니다.", icon="ℹ️")
    try:
        st.subheader("OD-DIFF in 2D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_diff_2d(st.session_state['day'], st.session_state['time'], st.session_state['code'], st.session_state['alpha']))
        st.subheader("OD-DIFF in 3D")
        st.pydeck_chart(BIGC_VIS_for_dashboard.vis_diff_3d(st.session_state['day'], st.session_state['time'], st.session_state['code'], st.session_state['alpha']))
    except Exception as e:
        logging.error("Error in STAY Visualization: %s", e)
        st.error("해당 날짜 및 시간에 해당하는 데이터가 없습니다.", icon="🚨")
