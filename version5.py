import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re
from datetime import datetime
import pandas as pd

# ✅ 페이지 설정

st.set_page_config(
page_title=“청년 실생활 정보 가이드”,
page_icon=“🌟”,
layout=“wide”,
initial_sidebar_state=“collapsed”
)

# ✅ CSS 스타일링 (서울청년 사이트 스타일 참고)

st.markdown(”””

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
    
    .category-card {
        background: white;
        border: 2px solid #f0f2f6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .category-card:hover {
        border-color: #2a5298;
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(42,82,152,0.15);
    }
    
    .category-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .category-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .category-desc {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
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
    
    .highlight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .footer-section {
        background: #2c3e50;
        color: white;
        padding: 3rem 2rem;
        margin: 3rem -1rem -1rem -1rem;
        text-align: center;
        border-radius: 30px 30px 0 0;
    }
    
    .btn-primary {
        background: #2a5298;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        background: #1e3c72;
        transform: translateY(-2px);
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
</style>

“””, unsafe_allow_html=True)

# ✅ 메인 히어로 섹션

st.markdown(”””

<div class="hero-section">
    <div class="hero-title">🌟 청년 실생활 정보 가이드</div>
    <div class="hero-subtitle">청년, 대학생, 사회초년생을 위한<br>원스톱 정보 플랫폼</div>
</div>
""", unsafe_allow_html=True)

# ✅ 언어 선택 (상단에 간단하게)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
lang = st.selectbox(“🌐 언어 선택”, [“한국어”, “English”], label_visibility=“collapsed”)

# ✅ 번역 함수

def safe_translate(text, target_lang=“en”):
if lang == “한국어”:
return text
try:
from googletrans import Translator
translator = Translator()
return translator.translate(text, dest=target_lang).text
except:
return text

# ✅ 통계 섹션

st.markdown(”””

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

st.markdown(’<div class="nav-container">’, unsafe_allow_html=True)
st.markdown(”### 🎯 원하는 정보를 선택하세요”)

# 카테고리 그리드

col1, col2, col3, col4 = st.columns(4)

selected_category = None

with col1:
if st.button(“💼\n취업/아르바이트”, key=“job”):
selected_category = “취업/아르바이트”

with col2:
if st.button(“🏡\n부동산”, key=“real_estate”):
selected_category = “부동산”

with col3:
if st.button(“💰\n금융”, key=“finance”):
selected_category = “금융”

with col4:
if st.button(“📄\n계약서”, key=“contract”):
selected_category = “계약서”

st.markdown(’</div>’, unsafe_allow_html=True)

# ✅ 세션 상태로 카테고리 관리

if “current_category” not in st.session_state:
st.session_state.current_category = None

if selected_category:
st.session_state.current_category = selected_category

# ✅ 토픽 데이터

def get_topic_data(topic):
data = {
“취업/아르바이트”: {
“근로계약서 작성법”: {
“content”: “근로계약서는 근로자와 사용자 간의 약속을 명시한 중요한 문서입니다. 임금, 근로시간, 휴일, 업무내용을 반드시 확인하세요.”,
“checklist”: [“임금 명시”, “근로시간 확인”, “4대보험 가입”, “퇴직금 규정”],
“source”: “고용노동부”
},
“최저임금 정보”: {
“content”: “2024년 최저임금은 시간당 9,860원입니다. 주휴수당, 야간수당 등도 꼼꼼히 확인하세요.”,
“law”: “최저임금법”,
“source”: “최저임금위원회”
},
“알바 권리보호”: {
“content”: “부당한 대우를 받았을 때는 고용노동부 신고센터(1350)로 신고할 수 있습니다.”,
“methods”: [“전화: 1350”, “온라인 신고”, “노동청 방문”],
“source”: “고용노동부”
}
},
“부동산”: {
“전세보증금 보호”: {
“content”: “전세보증금반환보증보험을 통해 전세금을 보호받을 수 있습니다. HUG, SGI서울보증 등에서 가입 가능합니다.”,
“documents”: [“임대차계약서”, “등기부등본”, “신분증”],
“source”: “주택도시보증공사”
},
“청약통장 관리”: {
“content”: “청약통장은 주택청약종합저축으로 통합되었습니다. 매월 2만원~50만원 납입 가능합니다.”,
“benefits”: [“소득공제 240만원”, “주택청약 자격”, “높은 이자율”],
“source”: “청약홈”
},
“월세 vs 전세”: {
“content”: “현재 금리 상황에서는 전세보다 월세가 유리할 수 있습니다. 개인 상황에 맞게 선택하세요.”,
“factors”: [“금리 동향”, “목돈 여유”, “거주 기간”, “세제 혜택”],
“source”: “국토교통부”
}
},
“금융”: {
“신용점수 관리”: {
“content”: “신용점수는 대출, 카드발급에 중요한 요소입니다. 정기적으로 확인하고 관리하세요.”,
“tips”: [“연체 방지”, “다양한 금융거래”, “신용정보 오류 정정”],
“sites”: [“올크레딧”, “크레딧뷰”, “마이크레딧”]
},
“적금 vs 펀드”: {
“content”: “안전성을 원한다면 적금, 수익성을 원한다면 펀드를 고려하세요. 포트폴리오 분산이 중요합니다.”,
“savings_pros”: [“원금보장”, “예금자보호”, “안정성”],
“fund_pros”: [“높은 수익 가능성”, “분산투자”, “전문가 운용”]
},
“청년 대출 상품”: {
“content”: “청년들을 위한 다양한 대출 상품이 있습니다. 금리와 조건을 꼼꼼히 비교하세요.”,
“products”: [“청년 버팀목 대출”, “청년 전세대출”, “학자금 대출”],
“source”: “주택도시기금”
}
},
“계약서”: {
“근로계약서”: {
“content”: “근로조건을 명확히 하는 필수 문서입니다. 반드시 서면으로 작성하세요.”,
“must_include”: [“임금”, “근로시간”, “업무내용”, “근무장소”],
“source”: “고용노동부”
},
“임대차계약서”: {
“content”: “주택 임대차 시 작성하는 계약서입니다. 특약사항을 꼼꼼히 확인하세요.”,
“cautions”: [“보증금 반환”, “임대료 인상”, “계약 갱신”, “수리 책임”],
“source”: “국토교통부”
}
}
}
return data.get(topic, {})

# ✅ 유튜브 검색 함수

def get_youtube_video_info(query):
try:
headers = {“User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36”}
search_query = urllib.parse.quote(query)
url = f”https://www.youtube.com/results?search_query={search_query}”

```
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
```

# ✅ 선택된 카테고리 내용 표시

if st.session_state.current_category:
current_topic = st.session_state.current_category
topic_data = get_topic_data(current_topic)

```
st.markdown(f"""
<div class="content-card">
    <h2 style="color: #2a5298; margin-bottom: 1rem;">📋 {current_topic} 정보</h2>
</div>
""", unsafe_allow_html=True)

if topic_data:
    # 세부 항목 선택
    sub_topics = list(topic_data.keys())
    selected_sub = st.selectbox("🔍 세부 정보를 선택하세요", sub_topics, key="sub_topic")
    
    if selected_sub:
        item = topic_data[selected_sub]
        
        # 메인 정보 표시
        st.markdown(f"""
        <div class="info-section">
            <h3 style="color: #2a5298; margin-bottom: 1rem;">💡 {selected_sub}</h3>
            <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">{safe_translate(item.get("content", "정보 없음"))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 추가 정보들을 탭으로 구성
        tab_names = ["📚 상세정보"]
        if any(key in item for key in ["checklist", "documents", "tips", "benefits"]):
            tab_names.append("✅ 체크리스트")
        if "source" in item:
            tab_names.append("🔗 관련 자료")
        
        tabs = st.tabs(tab_names)
        
        with tabs[0]:  # 상세정보
            if "law" in item:
                st.info(f"📜 관련 법령: {item['law']}")
            if "methods" in item:
                st.markdown("#### 📞 신고 방법")
                for method in item["methods"]:
                    st.markdown(f"- {method}")
            if "factors" in item:
                st.markdown("#### 🤔 고려사항")
                for factor in item["factors"]:
                    st.markdown(f"- {factor}")
            if "savings_pros" in item:
                col1, col2 = st.columns(2)
                with col1:
                    st.success("**💰 적금 장점**")
                    for pro in item["savings_pros"]:
                        st.markdown(f"- {pro}")
                with col2:
                    st.info("**📈 펀드 장점**")
                    for pro in item["fund_pros"]:
                        st.markdown(f"- {pro}")
        
        if len(tabs) > 1:  # 체크리스트 탭
            with tabs[1]:
                if "checklist" in item:
                    st.markdown("#### ✅ 필수 확인사항")
                    for check in item["checklist"]:
                        st.checkbox(check, key=f"check_{check}")
                if "documents" in item:
                    st.markdown("#### 📋 필요서류")
                    for doc in item["documents"]:
                        st.markdown(f"- {doc}")
                if "tips" in item:
                    st.markdown("#### 💡 관리 팁")
                    for tip in item["tips"]:
                        st.markdown(f"- {tip}")
                if "benefits" in item:
                    st.markdown("#### 🎁 혜택")
                    for benefit in item["benefits"]:
                        st.markdown(f"- {benefit}")
        
        if len(tabs) > 2:  # 관련 자료 탭
            with tabs[2]:
                if "source" in item:
                    st.markdown(f"**📍 정보 제공:** {item['source']}")
                
                # 관련 링크들
                links = {
                    "취업/아르바이트": [
                        ("고용노동부", "https://www.moel.go.kr"),
                        ("근로복지공단", "https://www.comwel.or.kr"),
                        ("잡코리아", "https://www.jobkorea.co.kr")
                    ],
                    "부동산": [
                        ("청약홈", "https://www.applyhome.co.kr"),
                        ("국토교통부", "https://www.molit.go.kr"),
                        ("주택도시보증공사", "https://www.hug.co.kr")
                    ],
                    "금융": [
                        ("금융감독원", "https://www.fss.or.kr"),
                        ("한국은행", "https://www.bok.or.kr"),
                        ("신용회복위원회", "https://www.ccrs.or.kr")
                    ],
                    "계약서": [
                        ("법무부", "https://www.moj.go.kr"),
                        ("소비자24", "https://www.consumer.go.kr"),
                        ("법제처", "https://www.moleg.go.kr")
                    ]
                }
                
                if current_topic in links:
                    st.markdown("#### 🔗 관련 사이트")
                    link_cols = st.columns(len(links[current_topic]))
                    for i, (name, url) in enumerate(links[current_topic]):
                        with link_cols[i]:
                            st.markdown(f'<a href="{url}" class="resource-link" target="_blank">{name}</a>', unsafe_allow_html=True)
        
        # 관련 뉴스 및 영상
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📰 관련 뉴스")
            news_url = f"https://search.naver.com/search.naver?where=news&query={urllib.parse.quote(f'{current_topic} {selected_sub}')}"
            st.markdown(f'<a href="{news_url}" class="resource-link" target="_blank">최신 뉴스 보기</a>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎥 관련 영상")
            try:
                with st.spinner("영상 검색 중..."):
                    youtube_info = get_youtube_video_info(f"{current_topic} {selected_sub}")
                    if youtube_info and youtube_info["videoId"]:
                        st.image(youtube_info["thumbnail"], width=200)
                        st.markdown(f"**{youtube_info['title'][:50]}...**")
                        st.markdown(f'<a href="https://www.youtube.com/watch?v={youtube_info["videoId"]}" class="resource-link" target="_blank">YouTube에서 보기</a>', unsafe_allow_html=True)
                    else:
                        st.info("관련 영상을 찾을 수 없습니다.")
            except Exception as e:
                st.info("영상 검색 서비스가 일시적으로 이용할 수 없습니다.")
```

else:
# 기본 홈 화면
st.markdown(”””
<div class="quick-menu">
<h3 style="margin-bottom: 1rem;">🚀 빠른 메뉴</h3>
<p>위의 카테고리를 선택하여 필요한 정보를 확인하세요!</p>
</div>
“””, unsafe_allow_html=True)

```
# 인기 정보 미리보기
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
```

# ✅ 피드백 섹션

st.markdown(”—”)
st.markdown(”””

<div class="content-card">
    <h3 style="color: #2a5298; margin-bottom: 1rem;">💬 사용자 피드백</h3>
</div>
""", unsafe_allow_html=True)

feedback_type = st.selectbox(“피드백 유형”, [“건의사항”, “오류신고”, “정보요청”, “기타”])
feedback_text = st.text_area(“내용을 입력해주세요”, height=100, placeholder=“개선사항이나 추가하고 싶은 정보가 있다면 알려주세요!”)

col1, col2 = st.columns([1, 4])
with col1:
if st.button(“📤 제출”, type=“primary”):
if feedback_text.strip():
st.success(“소중한 의견 감사합니다! 검토 후 반영하겠습니다.”)
else:
st.error(“내용을 입력해주세요.”)

# ✅ 푸터

st.markdown(”””

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
