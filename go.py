<!DOCTYPE html>

<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EvacuGuide - 대피소 안내</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

```
    body {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .app {
        max-width: 414px;
        margin: 0 auto;
        background: white;
        min-height: 100vh;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    
    .header {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 20px;
        text-align: center;
    }
    
    .header h1 {
        font-size: 24px;
        margin-bottom: 5px;
    }
    
    .location {
        background: #f8f9fa;
        padding: 15px;
        margin: 20px;
        border-radius: 10px;
        border-left: 4px solid #007bff;
    }
    
    .emergency-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        padding: 20px;
    }
    
    .emergency-btn {
        background: #dc3545;
        color: white;
        border: none;
        padding: 20px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .emergency-btn:hover {
        transform: translateY(-2px);
        background: #c82333;
    }
    
    .shelter-section {
        padding: 20px;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #333;
    }
    
    .shelter-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .shelter-card:hover {
        transform: translateY(-2px);
    }
    
    .shelter-name {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    
    .shelter-info {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 15px;
        font-size: 14px;
        color: #666;
    }
    
    .capacity {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    .capacity-bar {
        background: #e9ecef;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 5px;
    }
    
    .capacity-fill {
        height: 100%;
        background: #28a745;
        transition: width 0.3s;
    }
    
    .facilities {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }
    
    .facility {
        background: #e8f5e8;
        color: #2e7d32;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
    }
    
    .facility.unavailable {
        background: #ffebee;
        color: #c62828;
    }
    
    .actions {
        display: flex;
        gap: 10px;
    }
    
    .action-btn {
        flex: 1;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .directions {
        background: #007bff;
        color: white;
    }
    
    .directions:hover {
        background: #0056b3;
    }
    
    .call {
        background: #28a745;
        color: white;
    }
    
    .call:hover {
        background: #1e7e34;
    }
    
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 414px;
        background: white;
        border-top: 1px solid #ddd;
        display: flex;
        justify-content: space-around;
        padding: 15px 0;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        cursor: pointer;
        padding: 10px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    
    .nav-item.active {
        background: #e3f2fd;
        color: #1976d2;
    }
    
    .nav-icon {
        font-size: 20px;
    }
    
    .nav-text {
        font-size: 12px;
    }
    
    .hidden {
        display: none;
    }
    
    .guide-section {
        background: #fff3cd;
        padding: 20px;
        margin: 20px;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
    }
    
    .guide-steps {
        list-style: none;
    }
    
    .guide-step {
        background: white;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .step-number {
        background: #ffc107;
        color: #856404;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
    }
</style>
```

</head>
<body>
    <div class="app">
        <div class="header">
            <h1>🛡️ EvacuGuide</h1>
            <p>스마트 대피소 안내 시스템</p>
        </div>

```
    <!-- 메인 화면 -->
    <div id="main-screen">
        <div class="location">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">📍 현재 위치</div>
            <div style="font-size: 16px; font-weight: bold;">서울특별시 강남구 역삼동 123-45</div>
        </div>

        <div class="emergency-buttons">
            <button class="emergency-btn" onclick="emergency('119')">
                🚨 119 신고
            </button>
            <button class="emergency-btn" onclick="emergency('family')">
                📞 가족 연락
            </button>
        </div>

        <div class="guide-section">
            <div style="font-size: 18px; font-weight: bold; color: #856404; margin-bottom: 15px;">
                ⚡ 즉시 행동 지침
            </div>
            <ul class="guide-steps">
                <li class="guide-step">
                    <div class="step-number">1</div>
                    <div>안전한 곳으로 즉시 이동</div>
                </li>
                <li class="guide-step">
                    <div class="step-number">2</div>
                    <div>가족/지인에게 상황 알리기</div>
                </li>
                <li class="guide-step">
                    <div class="step-number">3</div>
                    <div>대피소 정보 확인 후 이동</div>
                </li>
            </ul>
        </div>
    </div>

    <!-- 대피소 목록 화면 -->
    <div id="shelter-screen" class="hidden">
        <div class="shelter-section">
            <div class="section-title">
                🏠 주변 대피소 <span style="color: #007bff;">(3곳)</span>
            </div>

            <div class="shelter-card">
                <div class="shelter-name">역삼초등학교 체육관</div>
                
                <div class="shelter-info">
                    <div>📍 180m · 도보 2분</div>
                    <div>📞 02-1234-5678</div>
                    <div>🏢 지상 1층</div>
                    <div>⏰ 24시간 운영</div>
                </div>

                <div class="capacity">
                    <div style="font-size: 14px; margin-bottom: 5px;">수용 현황: 234명/500명 (46.8%)</div>
                    <div class="capacity-bar">
                        <div class="capacity-fill" style="width: 46.8%"></div>
                    </div>
                </div>

                <div class="facilities">
                    <span class="facility">♿ 휠체어 접근</span>
                    <span class="facility">🏥 의료진 상주</span>
                    <span class="facility">🚿 샤워시설</span>
                    <span class="facility unavailable">🐕 반려동물 불가</span>
                </div>

                <div class="actions">
                    <button class="action-btn directions" onclick="getDirections('역삼초등학교')">
                        🗺️ 길찾기
                    </button>
                    <button class="action-btn call" onclick="callShelter('02-1234-5678')">
                        📞 연락하기
                    </button>
                </div>
            </div>

            <div class="shelter-card">
                <div class="shelter-name">강남구민회관</div>
                
                <div class="shelter-info">
                    <div>📍 420m · 도보 5분</div>
                    <div>📞 02-2345-6789</div>
                    <div>🏢 지상 2층</div>
                    <div>⏰ 24시간 운영</div>
                </div>

                <div class="capacity">
                    <div style="font-size: 14px; margin-bottom: 5px;">수용 현황: 89명/200명 (44.5%)</div>
                    <div class="capacity-bar">
                        <div class="capacity-fill" style="width: 44.5%"></div>
                    </div>
                </div>

                <div class="facilities">
                    <span class="facility">🐕 반려동물 동반</span>
                    <span class="facility">🚿 샤워시설</span>
                    <span class="facility">🍽️ 급식 가능</span>
                    <span class="facility unavailable">♿ 휠체어 제한</span>
                </div>

                <div class="actions">
                    <button class="action-btn directions" onclick="getDirections('강남구민회관')">
                        🗺️ 길찾기
                    </button>
                    <button class="action-btn call" onclick="callShelter('02-2345-6789')">
                        📞 연락하기
                    </button>
                </div>
            </div>

            <div class="shelter-card">
                <div class="shelter-name">테헤란로 복합문화센터</div>
                
                <div class="shelter-info">
                    <div>📍 650m · 도보 8분</div>
                    <div>📞 02-3456-7890</div>
                    <div>🏢 지하 1층</div>
                    <div>🚇 지하철 연결</div>
                </div>

                <div class="capacity">
                    <div style="font-size: 14px; margin-bottom: 5px;">수용 현황: 156명/300명 (52.0%)</div>
                    <div class="capacity-bar">
                        <div class="capacity-fill" style="width: 52.0%"></div>
                    </div>
                </div>

                <div class="facilities">
                    <span class="facility">🏥 의료진 상주</span>
                    <span class="facility">💊 약품 보관</span>
                    <span class="facility">🌐 Wi-Fi</span>
                    <span class="facility">🍽️ 급식 가능</span>
                </div>

                <div class="actions">
                    <button class="action-btn directions" onclick="getDirections('테헤란로 복합문화센터')">
                        🗺️ 길찾기
                    </button>
                    <button class="action-btn call" onclick="callShelter('02-3456-7890')">
                        📞 연락하기
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- 행동지침 화면 -->
    <div id="guide-screen" class="hidden">
        <div class="shelter-section">
            <div class="section-title">📋 재난별 행동 지침</div>

            <div class="guide-section">
                <div style="font-size: 18px; font-weight: bold; color: #856404; margin-bottom: 15px;">
                    🌊 침수 발생 시 행동 요령
                </div>
                <ul class="guide-steps">
                    <li class="guide-step">
                        <div class="step-number">1</div>
                        <div>전기 차단기를 즉시 내리고 가스밸브를 잠그세요</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number">2</div>
                        <div>1층 이상 높은 곳으로 대피하세요</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number">3</div>
                        <div>지하공간(주차장, 지하실)은 절대 출입 금지</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number">4</div>
                        <div>차량 이용을 피하고 도보로 대피하세요</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number">5</div>
                        <div>휴대폰, 신분증, 상비약을 챙기세요</div>
                    </li>
                </ul>
            </div>

            <div class="guide-section" style="background: #ffe6e6; border-left-color: #dc3545;">
                <div style="font-size: 18px; font-weight: bold; color: #721c24; margin-bottom: 15px;">
                    🔥 화재 발생 시 행동 요령
                </div>
                <ul class="guide-steps">
                    <li class="guide-step">
                        <div class="step-number" style="background: #dc3545; color: white;">1</div>
                        <div>젖은 수건으로 코와 입을 막으세요</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number" style="background: #dc3545; color: white;">2</div>
                        <div>자세를 낮춰 연기 아래로 대피하세요</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number" style="background: #dc3545; color: white;">3</div>
                        <div>엘리베이터 사용 금지, 계단 이용하세요</div>
                    </li>
                    <li class="guide-step">
                        <div class="step-number" style="background: #dc3545; color: white;">4</div>
                        <div>문을 열기 전 손등으로 온도를 확인하세요</div>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <!-- 설정 화면 -->
    <div id="settings-screen" class="hidden">
        <div class="shelter-section">
            <div class="section-title">⚙️ 설정</div>
            
            <div class="shelter-card">
                <div class="shelter-name">개인 정보 설정</div>
                <div style="margin: 15px 0;">
                    <div style="margin-bottom: 10px;">👤 이름: 홍길동</div>
                    <div style="margin-bottom: 10px;">📞 연락처: 010-1234-5678</div>
                    <div style="margin-bottom: 10px;">🏠 주소: 서울 강남구 역삼동</div>
                    <div style="margin-bottom: 10px;">💊 복용약물: 고혈압약</div>
                </div>
                <button class="action-btn directions" style="width: 100%;">정보 수정</button>
            </div>

            <div class="shelter-card">
                <div class="shelter-name">비상 연락처</div>
                <div style="margin: 15px 0;">
                    <div style="margin-bottom: 10px;">👨 아버지: 010-1111-2222</div>
                    <div style="margin-bottom: 10px;">👩 어머니: 010-3333-4444</div>
                    <div style="margin-bottom: 10px;">👫 배우자: 010-5555-6666</div>
                </div>
                <button class="action-btn call" style="width: 100%;">연락처 수정</button>
            </div>
        </div>
    </div>

    <!-- 하단 네비게이션 -->
    <div class="bottom-nav">
        <div class="nav-item active" onclick="showScreen('main')">
            <div class="nav-icon">🏠</div>
            <div class="nav-text">홈</div>
        </div>
        <div class="nav-item" onclick="showScreen('shelter')">
            <div class="nav-icon">📍</div>
            <div class="nav-text">대피소</div>
        </div>
        <div class="nav-item" onclick="showScreen('guide')">
            <div class="nav-icon">📋</div>
            <div class="nav-text">행동지침</div>
        </div>
        <div class="nav-item" onclick="showScreen('settings')">
            <div class="nav-icon">⚙️</div>
            <div class="nav-text">설정</div>
        </div>
    </div>
</div>

<script>
    // 화면 전환 함수
    function showScreen(screenName) {
        // 모든 화면 숨기기
        const screens = ['main-screen', 'shelter-screen', 'guide-screen', 'settings-screen'];
        screens.forEach(screen => {
            document.getElementById(screen).classList.add('hidden');
        });

        // 선택된 화면 보이기
        document.getElementById(screenName + '-screen').classList.remove('hidden');

        // 네비게이션 활성화 상태 변경
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        event.target.closest('.nav-item').classList.add('active');
    }

    // 긴급 신고 함수
    function emergency(type) {
        if (type === '119') {
            alert('🚨 119에 신고되었습니다!\n현재 위치가 자동으로 전송됩니다.\n\n📍 위치: 서울 강남구 역삼동\n⏰ 신고 시간: ' + new Date().toLocaleTimeString());
        } else if (type === 'family') {
            alert('📱 등록된 가족에게 긴급 상황이 전송되었습니다!\n\n✅ 아버지 (010-1111-2222)\n✅ 어머니 (010-3333-4444)\n✅ 배우자 (010-5555-6666)');
        }
    }

    // 길찾기 함수
    function getDirections(shelterName) {
        alert(`🗺️ ${shelterName}까지의 길안내를 시작합니다!\n\n📍 현재 위치에서 출발\n🚶‍♂️ 예상 소요시간: 2-8분\n🛡️ 가장 안전한 경로로 안내해드립니다.\n\n▶️ 음성 안내가 시작됩니다.`);
    }

    // 대피소 연락 함수
    function callShelter(phoneNumber) {
        alert(`📞 ${phoneNumber}로 연결합니다.\n\n대피소 담당자와 연결되어 현재 상황과 수용 가능 여부를 확인할 수 있습니다.`);
    }

    // 앱 초기화
    document.addEventListener('DOMContentLoaded', function() {
        console.log('EvacuGuide 앱이 시작되었습니다.');
        
        // 실시간 수용현황 업데이트 시뮬레이션
        setInterval(function() {
            const capacityBars = document.querySelectorAll('.capacity-fill');
            capacityBars.forEach(bar => {
                const currentWidth = parseFloat(bar.style.width) || 50;
                const change = (Math.random() - 0.5) * 2; // 작은 변화
                const newWidth = Math.max(10, Math.min(90, currentWidth + change));
                bar.style.width = newWidth + '%';
            });
        }, 5000); // 5초마다 업데이트
    });
</script>
```

</body>
</html>
