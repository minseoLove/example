import streamlit as st

# ✅ 페이지 설정 (반드시 가장 첫 번째 streamlit 명령어)
st.set_page_config(
    page_title="청년 실생활 정보 가이드", 
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import urllib.parse
import pandas as pd
from datetime import datetime

# utils.helper 모듈 import (없으면 기본 데이터 사용)
try:
    from utils.helper import get_topic_data
    HELPER_AVAILABLE = True
except ImportError:
    HELPER_AVAILABLE = False

# 선택적 import (없어도 작동하도록)
try:
    import requests
    from bs4 import BeautifulSoup
    import json
    import re
    EXTERNAL_LIBS_AVAILABLE = True
except ImportError:
    EXTERNAL_LIBS_AVAILABLE = False

# ✅ CSS 스타일링
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    .main {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .nav-container {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .info-section {
        background: #f8fafe;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 5px solid #2a5298;
    }
    
    .quick-menu {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e8eef5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #2a5298;
        display: block;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .content-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #f0f2f6;
    }
    
    .resource-link {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        margin: 0.25rem;
        font-size: 0.9rem;
        border: 1px solid #bbdefb;
    }
    
    .resource-link:hover {
        background: #1976d2;
        color: white;
    }
    
    .footer-section {
        background: #2c3e50;
        color: white;
        padding: 3rem 2rem;
        margin: 3rem -1rem -1rem -1rem;
        text-align: center;
        border-radius: 30px 30px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ✅ 메인 히어로 섹션
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🌟 청년 실생활 정보 가이드</div>
    <div class="hero-subtitle">청년, 대학생, 사회초년생을 위한<br>원스톱 정보 플랫폼</div>
</div>
""", unsafe_allow_html=True)

# ✅ 언어 선택
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    lang = st.selectbox("🌐 언어 선택", ["한국어", "English"], label_visibility="collapsed")

# ✅ 번역 함수
def safe_translate(text, target_lang="en"):
    if lang == "한국어":
        return text
    try:
        from googletrans import Translator
        translator = Translator()
        return translator.translate(text, dest=target_lang).text
    except:
        return text

# ✅ 통계 섹션
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <span class="stat-number">8+</span>
        <div class="stat-label">정보 카테고리</div>
    </div>
    <div class="stat-card">
        <span class="stat-number">50+</span>
        <div class="stat-label">외부 링크</div>
    </div>
    <div class="stat-card">
        <span class="stat-number">100%</span>
        <div class="stat-label">모바일 최적화</div>
    </div>
    <div class="stat-card">
        <span class="stat-number">매주</span>
        <div class="stat-label">업데이트</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ 카테고리 선택 섹션
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
st.markdown("### 🎯 원하는 정보를 선택하세요")

# 상태 경고 메시지
if not EXTERNAL_LIBS_AVAILABLE:
    st.info("💡 일부 외부 라이브러리가 없어 YouTube 검색 기능이 제한됩니다.")

if not HELPER_AVAILABLE:
    st.info("💡 utils.helper 모듈을 찾을 수 없어 기본 데이터를 사용합니다.")

# 카테고리 그리드
col1, col2, col3, col4 = st.columns(4)

selected_category = None

with col1:
    if st.button("💼\n취업/아르바이트", key="job"):
        selected_category = "취업/아르바이트"

with col2:
    if st.button("🏡\n부동산", key="real_estate"):
        selected_category = "부동산"

with col3:
    if st.button("💰\n금융", key="finance"):
        selected_category = "금융"

with col4:
    if st.button("📄\n계약서", key="contract"):
        selected_category = "계약서"

if st.button("🧑‍💼 아르바이트", key="arbeit"):
    selected_category = "아르바이트"

st.markdown('</div>', unsafe_allow_html=True)

# ✅ 세션 상태로 카테고리 관리
if "current_category" not in st.session_state:
    st.session_state.current_category = None

if selected_category:
    st.session_state.current_category = selected_category

# ✅ 토픽 데이터
def get_enhanced_topic_data(topic):
    if HELPER_AVAILABLE:
        try:
            return get_topic_data(topic)
        except:
            pass
    
    # 기본 데이터
    data = {
        "아르바이트": {
            "근로계약서 작성법": {
                "내용": "근로계약서는 근로자와 사용자 간의 약속을 명시한 중요한 문서입니다.",
                "체크리스트": ["임금 명시", "근로시간 확인", "4대보험 가입"],
                "출처": "고용노동부"
            },
            "최저임금 정보": {
                "내용": "2024년 최저임금은 시간당 9,860원입니다.",
                "출처": "최저임금위원회"
            }
        },
        "취업/아르바이트": {
            "근로계약서 작성법": {
                "content": "근로계약서는 근로자와 사용자 간의 약속을 명시한 중요한 문서입니다.",
                "checklist": ["임금 명시", "근로시간 확인", "4대보험 가입"],
                "source": "고용노동부"
            },
            "최저임금 정보": {
                "content": "2024년 최저임금은 시간당 9,860원입니다.",
                "source": "최저임금위원회"
            }
        },
        "부동산": {
            "전세보증금 보호": {
                "content": "전세보증금반환보증보험을 통해 전세금을 보호받을 수 있습니다.",
                "source": "주택도시보증공사"
            }
        },
        "금융": {
            "신용점수 관리": {
                "content": "신용점수는 대출, 카드발급에 중요한 요소입니다.",
                "tips": ["연체 방지", "다양한 금융거래"]
            }
        },
        "계약서": {
            "근로계약서": {
                "content": "근로조건을 명확히 하는 필수 문서입니다.",
                "source": "고용노동부"
            }
        }
    }
    return data.get(topic, {})

# ✅ 유튜브 검색 함수
def get_youtube_video_info(query):
    if not EXTERNAL_LIBS_AVAILABLE:
        return None
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        search_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={search_query}"
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for script in soup.find_all("script"):
            if script.string and "var ytInitialData" in script.string:
                match = re.search(r'var ytInitialData = ({.*?});', script.string, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
                    contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                    
                    if contents:
                        items = contents[0].get("itemSectionRenderer", {}).get("contents", [])
                        for item in items:
                            if "videoRenderer" in item:
                                video = item["videoRenderer"]
                                title = video.get("title", {}).get("runs", [{}])[0].get("text", "제목 없음")
                                video_id = video.get("videoId", "")
                                thumbnails = video.get("thumbnail", {}).get("thumbnails", [])
                                thumbnail = thumbnails[-1].get("url", "") if thumbnails else ""
                                
                                return {"videoId": video_id, "title": title, "thumbnail": thumbnail}
        return None
    except:
        return None

# ✅ 선택된 카테고리 내용 표시
if st.session_state.current_category:
    current_topic = st.session_state.current_category
    topic_data = get_enhanced_topic_data(current_topic)
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="color: #2a5298; margin-bottom: 1rem;">📋 {current_topic} 정보</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if topic_data:
        sub_topics = list(topic_data.keys())
        selected_sub = st.selectbox("🔍 세부 정보를 선택하세요", sub_topics, key="sub_topic")
        
        if selected_sub:
            item = topic_data[selected_sub]
            
            # 메인 정보 표시
            content_text = item.get("content", item.get("내용", "정보 없음"))
            st.markdown(f"""
            <div class="info-section">
                <h3 style="color: #2a5298; margin-bottom: 1rem;">💡 {selected_sub}</h3>
                <p style="font-size: 1.1rem; line-height: 1.6;">{safe_translate(content_text)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 계약서 관련 특별 섹션
            if current_topic in ["계약서", "아르바이트", "취업/아르바이트"]:
                st.markdown("---")
                st.subheader("📄 계약서 양식")
                st.markdown("[📄 고용노동부 표준계약서](https://www.moel.go.kr)")
                st.info("💡 근로계약서 작성시 임금, 근로시간을 반드시 명시하세요.")
                
            # 부동산 관련 특별 섹션
            if current_topic == "부동산":
                st.markdown("---")
                st.subheader("🏠 관련 사이트")
                st.markdown("- [청약홈](https://www.applyhome.co.kr)")
                st.markdown("- [국토교통부](https://www.molit.go.kr)")
            
            # 관련 뉴스 및 영상
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📰 관련 뉴스")
                news_url = f"https://search.naver.com/search.naver?where=news&query={urllib.parse.quote(f'{current_topic} {selected_sub}')}"
                st.markdown(f'<a href="{news_url}" class="resource-link" target="_blank">최신 뉴스 보기</a>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 🎥 관련 영상")
                if EXTERNAL_LIBS_AVAILABLE:
                    try:
                        youtube_info = get_youtube_video_info(f"{current_topic} {selected_sub}")
                        if youtube_info and youtube_info["videoId"]:
                            st.image(youtube_info["thumbnail"], width=200)
                            st.markdown(f"**{youtube_info['title'][:50]}...**")
                            st.markdown(f'<a href="https://www.youtube.com/watch?v={youtube_info["videoId"]}" class="resource-link" target="_blank">YouTube에서 보기</a>', unsafe_allow_html=True)
                        else:
                            st.info("관련 영상을 찾을 수 없습니다.")
                    except:
                        st.info("영상 검색 중 오류가 발생했습니다.")
                else:
                    search_query = urllib.parse.quote(f"{current_topic} {selected_sub}")
                    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
                    st.markdown(f'<a href="{youtube_url}" class="resource-link" target="_blank">YouTube에서 검색하기</a>', unsafe_allow_html=True)

else:
    # 기본 홈 화면
    st.markdown("""
    <div class="quick-menu">
        <h3 style="margin-bottom: 1rem;">🚀 빠른 메뉴</h3>
        <p>위의 카테고리를 선택하여 필요한 정보를 확인하세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 인기 정보
    st.markdown("### 🔥 인기 정보")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="content-card">
            <h4 style="color: #2a5298;">💼 취업 정보</h4>
            <p>최신 근로계약서 작성법과 최저임금 정보를 확인하세요</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="content-card">
            <h4 style="color: #2a5298;">🏡 부동산 가이드</h4>
            <p>전세보증금 보호와 청약통장 관리 방법을 알아보세요</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 최근 업데이트
    st.markdown("### 📊 최근 업데이트")
    updates = pd.DataFrame({
        "날짜": ["2024-06-07", "2024-06-06", "2024-06-05"],
        "업데이트 내용": ["청년 대출 상품 정보 업데이트", "최저임금 관련 법령 개정", "부동산 계약 체크리스트 추가"],
        "카테고리": ["💰 금융", "💼 취업", "🏡 부동산"]
    })
    st.dataframe(updates, use_container_width=True, hide_index=True)

# ✅ 피드백 섹션
st.markdown("---")
st.markdown("""
<div class="content-card">
    <h3 style="color: #2a5298; margin-bottom: 1rem;">💬 사용자 피드백</h3>
</div>
""", unsafe_allow_html=True)

st.info("원하는 정보가 부족하다면 아래에 의견을 남겨주세요!")
feedback_type = st.selectbox("피드백 유형", ["건의사항", "오류신고", "정보요청", "기타"])
feedback_text = st.text_area("내용을 입력해주세요", height=100, placeholder="궁금한 점이나 요청하고 싶은 내용을 적어주세요")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("📤 제출", type="primary"):
        if feedback_text.strip():
            st.success("소중한 의견 감사합니다! 빠른 시일 내 반영하겠습니다.")
        else:
            st.error("내용을 입력해주세요.")

# ✅ 푸터
st.markdown("""
<div class="footer-section">
    <h3 style="margin-bottom: 1rem;">🌟 청년 실생활 정보 가이드</h3>
    <p style="margin-bottom: 1rem;">청년들의 실생활에 필요한 모든 정보를 한 곳에서</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        📧 문의: info@youth-guide.com | 
        ⚠️ 본 정보는 참고용이며, 정확한 정보는 해당 기관에 문의하시기 바랍니다.
    </p>
    <p style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.6;">
        © 2024 Youth Life Guide. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
