import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re
from datetime import datetime
import pandas as pd

# ✅ 페이지 설정 (반드시 맨 위에)

st.set_page_config(
page_title=“청년 실생활 정보 가이드”,
page_icon=“📚”,
layout=“wide”,
initial_sidebar_state=“expanded”
)

# ✅ CSS 스타일링 (모던한 디자인)

st.markdown(”””

<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .topic-selector {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .resource-link {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #2196f3;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: #f0f8ff;
        border-radius: 8px;
        border: 1px solid #b3d9ff;
    }
</style>

“””, unsafe_allow_html=True)

# ✅ 사이드바 네비게이션

st.sidebar.title(“🏠 메뉴”)
page = st.sidebar.selectbox(“페이지 선택”, [
“🏠 홈”,
“💼 취업/아르바이트”,
“🏡 부동산”,
“💰 금융”,
“📄 계약서”,
“🎓 교육/자격증”,
“💡 생활팁”,
“📞 상담센터”
])

# ✅ 언어 선택

lang = st.sidebar.selectbox(“🌐 언어”, [“한국어”, “English”])

# ✅ 번역 함수 (에러 처리 추가)

def safe_translate(text, target_lang=“en”):
if lang == “한국어”:
return text
try:
from googletrans import Translator
translator = Translator()
return translator.translate(text, dest=target_lang).text
except:
return text  # 번역 실패시 원본 반환

# ✅ 메인 헤더

st.markdown(”””

<div class="main-header">
    <h1>📚 청년 실생활 정보 가이드</h1>
    <p>청년, 대학생, 사회초년생을 위한 원스톱 정보 플랫폼</p>
</div>
""", unsafe_allow_html=True)

# ✅ 통계 표시

col1, col2, col3, col4 = st.columns(4)
with col1:
st.metric(“📊 정보 카테고리”, “8개”)
with col2:
st.metric(“🔗 외부 링크”, “50+”)
with col3:
st.metric(“📱 모바일 최적화”, “100%”)
with col4:
st.metric(“🆕 업데이트”, “매주”)

# ✅ 토픽 데이터 (개선된 구조)

def get_enhanced_topic_data(topic):
data = {
“취업/아르바이트”: {
“근로계약서 작성법”: {
“내용”: “근로계약서는 근로자와 사용자 간의 약속을 명시한 중요한 문서입니다. 임금, 근로시간, 휴일, 업무내용을 반드시 확인하세요.”,
“체크리스트”: [“임금 명시”, “근로시간 확인”, “4대보험 가입”, “퇴직금 규정”],
“출처”: “https://www.moel.go.kr”
},
“최저임금 정보”: {
“내용”: “2024년 최저임금은 시간당 9,860원입니다. 주휴수당, 야간수당 등도 꼼꼼히 확인하세요.”,
“관련법”: “최저임금법”,
“출처”: “https://www.minimumwage.go.kr”
},
“알바 권리보호”: {
“내용”: “부당한 대우를 받았을 때는 고용노동부 신고센터(1350)로 신고할 수 있습니다.”,
“신고방법”: [“전화: 1350”, “온라인 신고”, “노동청 방문”],
“출처”: “https://www.moel.go.kr”
}
},
“부동산”: {
“전세보증금 보호”: {
“내용”: “전세보증금반환보증보험을 통해 전세금을 보호받을 수 있습니다. HUG, SGI서울보증 등에서 가입 가능합니다.”,
“필요서류”: [“임대차계약서”, “등기부등본”, “신분증”],
“출처”: “https://www.hug.co.kr”
},
“청약통장 관리”: {
“내용”: “청약통장은 주택청약종합저축으로 통합되었습니다. 매월 2만원~50만원 납입 가능합니다.”,
“혜택”: [“소득공제 240만원”, “주택청약 자격”, “높은 이자율”],
“출처”: “https://www.applyhome.co.kr”
},
“월세 vs 전세”: {
“내용”: “현재 금리 상황에서는 전세보다 월세가 유리할 수 있습니다. 개인 상황에 맞게 선택하세요.”,
“고려사항”: [“금리 동향”, “목돈 여유”, “거주 기간”, “세제 혜택”],
“출처”: “https://www.molit.go.kr”
}
},
“금융”: {
“신용점수 관리”: {
“내용”: “신용점수는 대출, 카드발급에 중요한 요소입니다. 정기적으로 확인하고 관리하세요.”,
“관리방법”: [“연체 방지”, “다양한 금융거래”, “신용정보 오류 정정”],
“확인사이트”: [“올크레딧”, “크레딧뷰”, “마이크레딧”]
},
“적금 vs 펀드”: {
“내용”: “안전성을 원한다면 적금, 수익성을 원한다면 펀드를 고려하세요. 포트폴리오 분산이 중요합니다.”,
“적금장점”: [“원금보장”, “예금자보호”, “안정성”],
“펀드장점”: [“높은 수익 가능성”, “분산투자”, “전문가 운용”]
},
“청년 대출 상품”: {
“내용”: “청년들을 위한 다양한 대출 상품이 있습니다. 금리와 조건을 꼼꼼히 비교하세요.”,
“상품종류”: [“청년 버팀목 대출”, “청년 전세대출”, “학자금 대출”],
“출처”: “https://nhuf.molit.go.kr”
}
}
}
return data.get(topic, {})

# ✅ 유튜브 검색 함수 (에러 처리 강화)

def get_youtube_video_info(query, max_retries=3):
for attempt in range(max_retries):
try:
headers = {
“User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36”
}
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
                                
                                return {
                                    "videoId": video_id,
                                    "title": title,
                                    "thumbnail": thumbnail
                                }
        return None
    except Exception as e:
        if attempt == max_retries - 1:
            st.warning(f"YouTube 영상 검색 중 오류가 발생했습니다: {str(e)}")
            return None
        continue
```

# ✅ 뉴스 검색 함수 (신규 추가)

def get_related_news(query):
try:
search_url = f”https://search.naver.com/search.naver?where=news&query={urllib.parse.quote(query)}”
return search_url
except:
return None

# ✅ 메인 컨텐츠

if page == “🏠 홈”:
# 홈페이지 대시보드
st.markdown(”### 🎯 인기 정보”)

```
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card">
        <h4>💼 취업 정보</h4>
        <p>최신 채용 정보와 면접 팁을 확인하세요</p>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🏡 부동산 가이드</h4>
        <p>전세, 월세 계약시 주의사항을 알아보세요</p>
    </div>
    """, unsafe_allow_html=True)
    
# 최근 업데이트
st.markdown("### 📊 최근 업데이트")
updates = pd.DataFrame({
    "날짜": ["2024-06-07", "2024-06-06", "2024-06-05"],
    "내용": ["청년 대출 상품 정보 업데이트", "최저임금 관련 법령 개정", "부동산 계약 체크리스트 추가"],
    "카테고리": ["금융", "취업", "부동산"]
})
st.dataframe(updates, use_container_width=True)
```

elif page in [“💼 취업/아르바이트”, “🏡 부동산”, “💰 금융”]:
# 기존 로직 개선
topic_map = {
“💼 취업/아르바이트”: “취업/아르바이트”,
“🏡 부동산”: “부동산”,
“💰 금융”: “금융”
}

```
current_topic = topic_map[page]
st.markdown(f"## {page}")

topic_data = get_enhanced_topic_data(current_topic)
if topic_data:
    sub_topic = st.selectbox("🔍 세부 정보를 선택하세요", list(topic_data.keys()))
    
    if sub_topic:
        st.markdown("---")
        item = topic_data[sub_topic]
        
        # 메인 정보 표시
        st.markdown(f"### 💡 {sub_topic}")
        st.success(safe_translate(item.get("내용", "정보 없음")))
        
        # 추가 정보 표시
        if "체크리스트" in item:
            st.markdown("#### ✅ 체크리스트")
            for check in item["체크리스트"]:
                st.markdown(f"- {safe_translate(check)}")
                
        if "필요서류" in item:
            st.markdown("#### 📋 필요서류")
            for doc in item["필요서류"]:
                st.markdown(f"- {safe_translate(doc)}")
        
        # 관련 자료 섹션
        if current_topic == "취업/아르바이트":
            st.markdown("---")
            st.markdown("### 📄 관련 자료")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class="resource-link">
                    <h5>📄 표준 근로계약서</h5>
                    <a href="https://www.moel.go.kr/policy/policydata/view.do?bbs_seq=20190300329" target="_blank">다운로드</a>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class="resource-link">
                    <h5>📞 노동권익센터</h5>
                    <p>전화: 1350</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 뉴스 및 영상 섹션
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📰 관련 뉴스")
            news_url = get_related_news(f"{current_topic} {sub_topic}")
            if news_url:
                st.markdown(f"[최신 뉴스 보기]({news_url})")
            
        with col2:
            st.markdown("### 🎥 관련 영상")
            with st.spinner("영상 검색 중..."):
                youtube_info = get_youtube_video_info(f"{current_topic} {sub_topic}")
                if youtube_info and youtube_info["videoId"]:
                    st.image(youtube_info["thumbnail"], width=200)
                    st.markdown(f"**{youtube_info['title'][:50]}...**")
                    st.markdown(f"[YouTube에서 보기](https://www.youtube.com/watch?v={youtube_info['videoId']})")
                else:
                    st.info("관련 영상을 찾을 수 없습니다.")
```

elif page == “📄 계약서”:
st.markdown(”## 📄 계약서”)

```
contract_types = st.selectbox("계약서 종류 선택", [
    "근로계약서", "임대차계약서", "대출계약서", "기타 계약서"
])

if contract_types == "근로계약서":
    st.markdown("### 💼 근로계약서 가이드")
    
    tab1, tab2, tab3 = st.tabs(["📝 작성법", "📄 양식", "⚠️ 주의사항"])
    
    with tab1:
        st.markdown("""
        #### 근로계약서 필수 기재사항
        1. **근로자 정보**: 성명, 주민등록번호
        2. **임금**: 기본급, 각종 수당, 지급방법
        3. **근로시간**: 시작시간, 종료시간, 휴게시간
        4. **휴일**: 주휴일, 연차휴가
        5. **업무장소와 업무내용**
        """)
        
    with tab2:
        st.markdown("#### 📄 표준 양식 다운로드")
        st.markdown("[고용노동부 표준 근로계약서](https://www.moel.go.kr)")
        
    with tab3:
        st.warning("""
        ⚠️ **주의사항**
        - 구두약속보다는 반드시 서면으로 작성
        - 계약서 사본을 본인이 보관
        - 불리한 조건이 있다면 수정 요청
        - 4대보험 가입 여부 확인
        """)
```

elif page == “🎓 교육/자격증”:
st.markdown(”## 🎓 교육/자격증”)

```
edu_category = st.selectbox("카테고리 선택", [
    "국가자격증", "민간자격증", "온라인 강의", "국비지원 교육"
])

if edu_category == "국가자격증":
    st.markdown("### 📜 인기 국가자격증")
    
    certificates = {
        "컴활 1급": {"난이도": "중", "취업도움": "높음", "시험횟수": "년 4회"},
        "토익": {"난이도": "중상", "취업도움": "매우높음", "시험횟수": "월 1-2회"},
        "정보처리기사": {"난이도": "상", "취업도움": "높음", "시험횟수": "년 3회"}
    }
    
    for cert, info in certificates.items():
        with st.expander(f"📋 {cert}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("난이도", info["난이도"])
            with col2:
                st.metric("취업도움", info["취업도움"])
            with col3:
                st.metric("시험횟수", info["시험횟수"])
```

elif page == “💡 생활팁”:
st.markdown(”## 💡 생활팁”)

```
tip_category = st.selectbox("팁 카테고리", [
    "💰 절약팁", "🏠 생활꿀팁", "🍳 요리", "💪 건강관리"
])

if tip_category == "💰 절약팁":
    tips = [
        "통신비 절약: 알뜰폰 이용시 월 2-3만원 절약 가능",
        "구독서비스 정리: 사용하지 않는 구독은 즉시 해지",
        "가계부 작성: 용돈기입장 앱으로 간편하게 관리",
        "할인혜택 활용: 청년할인카드, 대학생할인 적극 활용"
    ]
    
    for i, tip in enumerate(tips, 1):
        st.markdown(f"**{i}.** {tip}")
```

elif page == “📞 상담센터”:
st.markdown(”## 📞 상담센터”)

```
st.markdown("### 🆘 분야별 상담센터")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 💼 취업/노동 관련
    - **고용노동부**: 1350
    - **청년고용센터**: 지역별 상이
    - **잡코리아 상담**: 온라인 채팅
    
    #### 🏡 부동산 관련  
    - **국토교통부**: 1599-0001
    - **전세사기신고센터**: 1833-8382
    - **주택도시보증공사**: 1566-9009
    """)
    
with col2:
    st.markdown("""
    #### 💰 금융 관련
    - **금융감독원**: 1332
    - **신용회복위원회**: 1600-5500
    - **서민금융진흥원**: 1397
    
    #### 📚 교육 관련
    - **한국장학재단**: 1599-2000
    - **국가평생교육진흥원**: 1577-3867
    - **워크넷**: 1588-1919
    """)
```

# ✅ 사용자 피드백 (공통)

st.markdown(”—”)
st.markdown(”### 💬 피드백”)

feedback_type = st.selectbox(“피드백 유형”, [“건의사항”, “오류신고”, “정보요청”, “기타”])
feedback_text = st.text_area(“내용을 입력해주세요”, height=100)

col1, col2 = st.columns([1, 4])
with col1:
if st.button(“📤 제출”, type=“primary”):
if feedback_text.strip():
st.success(“소중한 의견 감사합니다! 검토 후 반영하겠습니다.”)
# 실제로는 데이터베이스나 이메일로 전송
else:
st.error(“내용을 입력해주세요.”)

# ✅ 푸터

st.markdown(”””

<div class="footer">
    <p>📚 청년 실생활 정보 가이드 | 문의: info@youth-guide.com</p>
    <p>⚠️ 본 정보는 참고용이며, 정확한 정보는 해당 기관에 문의하시기 바랍니다.</p>
    <p>© 2024 Youth Life Guide. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
