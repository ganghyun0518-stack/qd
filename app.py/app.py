import streamlit as st
import streamlit.components.v1 as components
import os

# --- 페이지 설정 ---
# Streamlit 페이지의 기본 레이아웃을 'wide'로 설정하여
# 보고서 형식의 웹페이지가 화면에 꽉 차도록 합니다.
st.set_page_config(
    page_title="인터랙티브 연구 보고서",
    page_icon="🚌",
    layout="wide"
)

# --- HTML 파일 로드 ---
# 이 함수는 현재 디렉토리에 있는 index.html 파일을 읽어 그 내용을 반환합니다.
def load_html_file(file_path="index.html"):
    """
    Reads a single HTML file and returns its content as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # index.html 파일이 없을 경우 에러 메시지를 표시합니다.
        st.error(f"오류: '{file_path}' 파일을 찾을 수 없습니다. app.py와 동일한 디렉토리에 있는지 확인하세요.")
        return None

# --- 메인 애플리케이션 실행 ---
# index.html 파일의 내용을 불러옵니다.
report_html = load_html_file()

if report_html:
    # st.components.v1.html을 사용하여 HTML 콘텐츠를 Streamlit 앱에 렌더링합니다.
    # height와 scrolling=True 설정을 통해 앱 내에서 전체 페이지를 스크롤하며 볼 수 있습니다.
    components.html(report_html, height=1200, scrolling=True)

