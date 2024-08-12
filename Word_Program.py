import time
import streamlit as st

if 'display' not in st.session_state :
    st.session_state.display = 0

if st.session_state.display :
    st.session_state.display = 0 
    st.rerun()

def display_home():
    GREETING = "## Welcome to Vocabulary Learning"

    ENCOUARGE = """ Even if studying is difficult, consistent effort will eventually bring you success.\
        I hope you achieve your desired goals today.
    """

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


    #stream_header(GREETING)

    st.write_stream(stream_data(GREETING))

    st.divider()

    st.write_stream(stream_data(ENCOUARGE))

    st.text('\n')
    st.text('\n')

    stream_subheader("Hello, Hooby 🙂")

st.set_page_config(
    page_title="Word Program", # Tab page title
    page_icon="👋",
)

st.sidebar.success("Select a Page above.")
st.empty()
display_home()
st.session_state.display = 1 
