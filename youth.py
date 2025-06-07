import streamlit as st
from utils.helper import get_topic_data, get_related_news
from googletrans import Translator
import time

# 페이지 설정

st.set_page_config(
page_title=“청년 실생활 정보 가이드”,
page_icon=“🎓”,
layout=“wide”,
initial_sidebar_state=“expanded”
)

# CSS 스타일링

st.markdown(”””

<style>
    /* 메인 컨테이너 스타일 */
    .main > div {
        padding-top: 2rem;
    }
    
    /* 제목 스타일 */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    /* 카드 형태의 컨테이너 */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* 뉴스 카드 스타일 */
    .news-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    /* 선택박스 스타일 */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
    }
    
    /* 텍스트 에리어 스타일 */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
    }
</style>

“””, unsafe_allow_html=True)

# 번역 함수 초기화

@st.cache_resource
def init_translator():
return Translator()

translator = init_translator()

def translate_text(text, target_lang):
“”“텍스트 번역 함수 (에러 처리 포함)”””
try:
if target_lang == “English”:
return translator.translate(text, dest=“en”).text
return text
except Exception as e:
st.error(f”번역 중 오류가 발생했습니다: {e}”)
return text

# 헤더 섹션

st.markdown(”””

<div class="title-container">
    <h1>🎓 청년 실생활 정보 도우미</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">청년, 대학생, 사회초년생을 위한 맞춤 정보 플랫폼</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 설정

with st.sidebar:
st.header(“🌐 설정”)
lang = st.selectbox(
“언어를 선택하세요”,
[“한국어”, “English”],
help=“원하는 언어를 선택해주세요”
)

```
st.markdown("---")
st.markdown("### 📊 사이트 통계")
col1, col2 = st.columns(2)
with col1:
    st.metric("총 방문자", "1,234", "+56")
with col2:
    st.metric("오늘 방문", "89", "+12")
```

# 메인 컨텐츠

col1, col2 = st.columns([2, 1])

with col1:
# 주제 선택 섹션
st.markdown(”### 🔍 관심 분야를 선택해주세요”)

```
topic_options = ["아르바이트", "부동산", "금융", "계약서"]
main_topic = st.selectbox(
    translate_text("궁금한 주제를 선택하세요", lang),
    topic_options,
    help="가장 관심있는 분야를 선택해주세요"
)
```

with col2:
# 도움말 카드
st.markdown(”””
<div class="info-card">
<h4>💡 이용 안내</h4>
<ul>
<li>주제를 선택하세요</li>
<li>세부 항목을 확인하세요</li>
<li>최신 뉴스를 확인하세요</li>
<li>궁금한 점을 남겨주세요</li>
</ul>
</div>
“””, unsafe_allow_html=True)

# 주제가 선택되었을 때

if main_topic:
try:
topic_data = get_topic_data(main_topic)

```
    if topic_data:
        st.markdown("---")
        
        # 세부 주제 선택
        st.markdown("### 📋 세부 항목")
        sub_topic = st.radio(
            translate_text("원하는 세부 항목을 선택하세요", lang),
            list(topic_data.keys()),
            horizontal=True
        )
        
        if sub_topic:
            # 정보 표시 섹션
            st.markdown("---")
            st.markdown("### 💡 상세 정보")
            
            item = topic_data.get(sub_topic, {})
            
            if isinstance(item, dict):
                content = item.get("내용", "정보를 준비 중입니다.")
                source = item.get("출처", "")
                
                # 정보 카드로 표시
                st.markdown(f"""
                <div class="info-card">
                    <h4>{translate_text(sub_topic, lang)}</h4>
                    <p>{translate_text(content, lang)}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if source:
                    st.markdown(f"**출처:** [{source}]({source})")
            else:
                st.success(translate_text(str(item), lang))
            
            # 관련 뉴스 섹션
            st.markdown("---")
            st.markdown("### 📰 최신 관련 뉴스")
            
            with st.spinner('최신 뉴스를 가져오는 중...'):
                news_list = get_related_news(main_topic, sub_topic)
            
            if news_list:
                for i, news in enumerate(news_list):
                    st.markdown(f"""
                    <div class="news-card">
                        <h5>📄 {translate_text(news['title'], lang)}</h5>
                        <a href="{news['url']}" target="_blank">기사 읽어보기 →</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(translate_text("관련 기사를 찾을 수 없습니다. 곧 업데이트 예정입니다!", lang))
    
    else:
        st.warning("선택한 주제의 데이터를 불러올 수 없습니다.")
        
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
```

# 피드백 섹션

st.markdown(”—”)
st.markdown(”### 💬 사용자 피드백”)

feedback_col1, feedback_col2 = st.columns([3, 1])

with feedback_col1:
st.info(translate_text(“더 나은 서비스를 위해 여러분의 소중한 의견을 들려주세요!”, lang))

```
feedback = st.text_area(
    translate_text("궁금한 점이나 개선사항을 자유롭게 작성해주세요", lang),
    placeholder=translate_text("예: OO 분야 정보가 더 필요해요", lang),
    height=100
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    if st.button(translate_text("📝 제출", lang)):
        if feedback.strip():
            st.success(translate_text("소중한 의견 감사합니다! 검토 후 빠르게 반영하겠습니다.", lang))
            st.balloons()  # 성공 애니메이션
        else:
            st.warning(translate_text("의견을 입력해주세요.", lang))

with col_btn2:
    if st.button(translate_text("🔄 초기화", lang)):
        st.rerun()
```

with feedback_col2:
st.markdown(”””
<div class="info-card">
<h5>📞 문의하기</h5>
<p>📧 info@youth-guide.com</p>
<p>📱 카카오톡: @청년도우미</p>
<p>⏰ 평일 9:00-18:00</p>
</div>
“””, unsafe_allow_html=True)

# 푸터

st.markdown(”—”)
st.markdown(”””

<div style="text-align: center; padding: 2rem; color: #666;">
    <p>© 2025 청년 실생활 정보 가이드. All rights reserved.</p>
    <p>🎯 청년의, 청년에 의한, 청년을 위한 정보 플랫폼</p>
</div>
""", unsafe_allow_html=True)
