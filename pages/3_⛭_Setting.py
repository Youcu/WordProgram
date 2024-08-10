import streamlit as st
import re
import time

# --------- Init ---------- # 
st.set_page_config(page_title="Word Master", page_icon="⛭")

# --------- Pre Define --------- #

# Text Animations
def stream_header(text):
        header_text = ""  # 초기화된 헤더 텍스트
        header_placeholder = st.empty()  # 빈 공간을 마련하여 업데이트할 준비를 합니다.
        
        for char in text:
            header_text += char  # 기존 텍스트에 한 글자씩 추가
            header_placeholder.header(header_text)  # 헤더를 업데이트
            time.sleep(0.1)  # 딜레이를 적용
def stream_data(string):
    # 문자열을 한 문자씩 스트리밍
    for char in string:
        yield char
        time.sleep(0.02)  # 0.1초 딜레이
def stream_subheader(text):
    subheader_text = ""  # 초기화된 헤더 텍스트
    subheader_placeholder = st.empty()  # 빈 공간을 마련하여 업데이트할 준비를 합니다.
    
    for char in text:
        subheader_text += char  # 기존 텍스트에 한 글자씩 추가
        subheader_placeholder.subheader(subheader_text)  # 헤더를 업데이트
        time.sleep(0.1)  # 딜레이를 적용

setting_text = """## The feature is not yet available.
"""
st.write_stream(stream_data(setting_text))
st.error("Comming Soon")




