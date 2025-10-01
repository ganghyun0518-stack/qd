import streamlit as st
import streamlit.components.v1 as components
import os

def load_html(file_path):
    """
    지정된 경로의 HTML 파일을 읽어와서 반환합니다.
    """
    if not os.path.exists(file_path):
        st.error(f"Error: '{file_path}' 파일을 찾을 수 없습니다. 'app.py'와 같은 레벨에 'htmls' 폴더를 만들고 그 안에 'index.html' 파일이 있는지 확인하세요.")
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Streamlit 페이지 설정
st.set_page_config(
    page_title="인터랙티브 연구 보고서",
    page_icon="🚌",
    layout="wide"
)

st.title("인터랙티브 연구 보고서 웹페이지")

# 'htmls' 폴더 안의 'index.html' 파일 경로 설정
# __file__은 현재 스크립트(app.py)의 경로를 나타냅니다.
# os.path.dirname()으로 디렉토리 경로를 얻고, os.path.join()으로 경로를 안전하게 결합합니다.
html_file_path = os.path.join(os.path.dirname(__file__), "htmls", "index.html")

# HTML 코드 로드 및 표시
html_code = load_html(html_file_path)

if html_code:
    components.html(html_code, height=1200, scrolling=True)

# 하단에 추가적인 내용
st.markdown("---")
st.markdown("### Streamlit에서 렌더링된 웹페이지")
st.info("이 페이지는 'htmls' 폴더 내의 HTML 파일을 불러와 Streamlit을 통해 표시한 것입니다. `app.py` 파일을 수정하여 다른 기능들을 추가할 수 있습니다.")

