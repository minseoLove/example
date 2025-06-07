import streamlit as st
import urllib.parse
from datetime import datetime
import pandas as pd

# ✅ 페이지 설정
st.set_page_config(
    page_title="청년 실생활 정보 가이드", 
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ CSS 스타일링 (서울청년 사이트 스타일 참고)
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
    
    .footer-section {
        background: #2c3e50;
        color: white;
        padding: 3rem 2rem;
        margin: 3rem -1rem -1rem -1rem;
        text-align: center;
        border-radius: 30px 30px 0 0;
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
    
    .highlight-tip {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
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

# ✅ 언어 선택 (상단에 간단하게)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    lang = st.selectbox("🌐 언어 선택", ["한국어", "English"], label_visibility="collapsed")

# ✅ 번역 함수 (간단화)
def safe_translate(text):
    if lang == "English":
        # 간단한 번역 매핑 (실제 번역 API 없이)
        translations = {
            "근로계약서는": "Employment contracts are",
            "전세보증금반환보증보험을": "Jeonse deposit return guarantee insurance",
            "신용점수는": "Credit scores are",
            "정보 없음": "No information available"
        }
        for ko, en in translations.items():
            if ko in text:
                text = text.replace(ko, en)
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

st.markdown('</div>', unsafe_allow_html=True)

# ✅ 세션 상태로 카테고리 관리
if "current_category" not in st.session_state:
    st.session_state.current_category = None

if selected_category:
    st.session_state.current_category = selected_category

# ✅ 토픽 데이터 (확장된 실용적 정보)
def get_topic_data(topic):
    data = {
        "취업/아르바이트": {
            "근로계약서 작성법": {
                "content": "근로계약서는 근로자와 사용자 간의 약속을 명시한 중요한 문서입니다. 임금, 근로시간, 휴일, 업무내용을 반드시 확인하세요.",
                "checklist": ["임금 명시 (시급/월급)", "근로시간 확인", "4대보험 가입", "퇴직금 규정", "휴가 규정"],
                "tips": ["구두약속은 증거가 없으니 반드시 서면 작성", "계약서 사본 보관 필수", "불리한 조건 발견시 수정 요청"],
                "source": "고용노동부",
                "phone": "1350"
            },
            "최저임금 정보": {
                "content": "2024년 최저임금은 시간당 9,860원입니다. 주휴수당, 야간수당, 연장근로수당 등도 꼼꼼히 확인하세요.",
                "details": ["주휴수당: 주 15시간 이상 근무시", "야간수당: 22시~06시 50% 가산", "연장근로: 주 40시간 초과시 50% 가산"],
                "law": "최저임금법",
                "source": "최저임금위원회"
            },
            "알바 권리보호": {
                "content": "부당한 대우를 받았을 때는 고용노동부 신고센터(1350)로 신고할 수 있습니다. 임금체불, 부당해고 등 권리침해 시 적극 신고하세요.",
                "methods": ["전화: 1350 (고용노동부)", "온라인: 고용노동부 홈페이지", "직접 방문: 관할 노동청"],
                "violations": ["임금체불", "부당해고", "근로시간 위반", "휴가 미제공"],
                "source": "고용노동부"
            }
        },
        "부동산": {
            "전세보증금 보호": {
                "content": "전세보증금반환보증보험을 통해 전세금을 보호받을 수 있습니다. HUG, SGI서울보증 등에서 가입 가능하며, 임
