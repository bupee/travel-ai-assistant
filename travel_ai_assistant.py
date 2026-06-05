"""
여행 맞춤 추천 AI 비서 - 통합 프로그램
Google Gemini API를 활용하여 여행 추천을 제공하는 터미널 기반 프로그램입니다.
"""

import google.generativeai as genai

# ============================================================================
# API 키 설정
# ============================================================================
# 사용자가 여기에 자신의 Google Gemini API 키를 입력해주세요
my_key = "your_api_key_here"

# API 키를 설정합니다
genai.configure(api_key=my_key)

# Gemini 모델을 초기화합니다
model = genai.GenerativeModel("gemini-2.5-flash")


# ============================================================================
# 프롬프트 템플릿
# ============================================================================

def get_restaurant_prompt(destination):
    """여행지 정보 조회용 프롬프트를 생성합니다"""
    prompt = f"""
당신은 여행 전문 AI 비서입니다.
사용자가 입력한 '{destination}' 지역에 대해 다음을 구분하여 추천해주세요.

1. 식당 추천 (5개): 지역 특색 있는 음식점
2. 가볼 만한 곳 (5개): 관광지 및 명소
3. 숙소 추천 지역 (3개): 숙박하기 좋은 지역

각 항목마다 이름과 간단한 설명(2-3줄)을 포함해주세요.
한국어로 답변해주세요.
"""
    return prompt


def get_itinerary_prompt(accommodation, travelers, duration):
    """여행 일정 생성용 프롬프트를 생성합니다"""
    prompt = f"""
당신은 여행 일정 전문가입니다.
다음 정보를 바탕으로 최적의 여행 일정을 짜주세요.

숙소 위치: {accommodation}
여행 인원: {travelers}명
여행 기간: {duration}일

다음을 포함해주세요:
1. 날짜별 여행 일정 (일별로 구분)
2. 장소 간 이동경로 (첫 번째 장소 → 두 번째 장소 등)
3. 각 이동 구간의 추천 이동수단 (대중교통, 택시, 렌터카 등)
4. 예상 소요 시간

한국어로 답변해주세요.
"""
    return prompt


def get_recommendation_prompt(destination, conditions):
    """조건 기반 장소 추천용 프롬프트를 생성합니다"""
    prompt = f"""
당신은 여행지 추천 전문가입니다.
사용자의 요구사항에 맞는 장소를 추천해주세요.

여행지: {destination}
원하는 조건: {conditions}

다음을 포함해주세요:
1. 추천 장소 (3-5개)
2. 각 장소별 추천 이유 (2-3줄)
3. 각 장소의 방문 팁 (운영 시간, 예약 필요 여부, 복장 등)

한국어로 답변해주세요.
"""
    return prompt


# ============================================================================
# 기능별 함수
# ============================================================================

def print_header(title):
    """헤더를 출력합니다"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_loading():
    """로딩 메시지를 출력합니다"""
    print("\n⏳ AI가 응답을 생성 중입니다. 잠시만 기다려주세요...\n")


def print_error(message):
    """에러 메시지를 출력합니다"""
    print(f"\n❌ 오류: {message}\n")


def call_gemini_api(prompt):
    """
    Gemini API를 호출하고 응답을 반환합니다.
    
    Args:
        prompt (str): API에 전달할 프롬프트
    
    Returns:
        str: AI의 응답 텍스트 또는 None (오류 발생 시)
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print_error(f"API 호출 중 오류 발생: {str(e)}")
        return None


# ============================================================================
# 기능 1: 여행지 정보 조회
# ============================================================================

def feature_1_restaurant_guide():
    """
    기능 1: 여행지 정보 조회
    사용자가 입력한 여행지의 식당, 관광지, 숙소를 추천합니다.
    """
    print_header("기능 1: 여행지 정보 조회")
    
    # 사용자 입력 받기
    destination = input("🌍 여행지를 입력해주세요: ").strip()
    
    # 입력값 검증
    if not destination:
        print_error("여행지를 입력해주세요.")
        return
    
    # AI에게 요청할 프롬프트 생성
    prompt = get_restaurant_prompt(destination)
    
    # API 호출
    print_loading()
    response = call_gemini_api(prompt)
    
    # 결과 출력
    if response:
        print_header(f"{destination} 여행 정보")
        print(response)


# ============================================================================
# 기능 2: 여행 일정 생성
# ============================================================================

def feature_2_travel_itinerary():
    """
    기능 2: 여행 일정 생성
    숙소 위치, 인원, 기간을 입력받아 맞춤 일정을 생성합니다.
    """
    print_header("기능 2: 여행 일정 생성")
    
    # 사용자 입력 받기
    accommodation = input("🏨 숙소 위치를 입력해주세요: ").strip()
    travelers = input("👥 여행 인원 (명)을 입력해주세요: ").strip()
    duration = input("📅 여행 기간 (일)을 입력해주세요: ").strip()
    
    # 입력값 검증
    if not accommodation:
        print_error("숙소 위치를 입력해주세요.")
        return
    
    if not travelers:
        print_error("여행 인원을 입력해주세요.")
        return
    
    if not duration:
        print_error("여행 기간을 입력해주세요.")
        return
    
    # 숫자 검증
    try:
        travelers_int = int(travelers)
        duration_int = int(duration)
        
        if travelers_int <= 0:
            print_error("여행 인원은 1명 이상이어야 합니다.")
            return
        
        if duration_int <= 0:
            print_error("여행 기간은 1일 이상이어야 합니다.")
            return
    
    except ValueError:
        print_error("인원과 기간은 숫자로 입력해주세요.")
        return
    
    # AI에게 요청할 프롬프트 생성
    prompt = get_itinerary_prompt(accommodation, travelers, duration)
    
    # API 호출
    print_loading()
    response = call_gemini_api(prompt)
    
    # 결과 출력
    if response:
        print_header("생성된 여행 일정")
        print(response)


# ============================================================================
# 기능 3: 조건 기반 장소 추천
# ============================================================================

def feature_3_place_recommendation():
    """
    기능 3: 조건 기반 장소 추천
    사용자의 조건에 맞는 장소를 추천합니다.
    """
    print_header("기능 3: 조건 기반 장소 추천")
    
    # 조건 예시 안내
    print("💡 조건 예시: 가족 동반, 실내, 2시간 이내")
    print("         또는: 어드벤처, 높은 곳, 사진 명소\n")
    
    # 사용자 입력 받기
    destination = input("🌍 여행지를 입력해주세요: ").strip()
    conditions = input("🎯 원하는 조건을 입력해주세요: ").strip()
    
    # 입력값 검증
    if not destination:
        print_error("여행지를 입력해주세요.")
        return
    
    if not conditions:
        print_error("원하는 조건을 입력해주세요.")
        return
    
    # AI에게 요청할 프롬프트 생성
    prompt = get_recommendation_prompt(destination, conditions)
    
    # API 호출
    print_loading()
    response = call_gemini_api(prompt)
    
    # 결과 출력
    if response:
        print_header(f"{destination} - 조건 기반 장소 추천")
        print(response)


# ============================================================================
# 메뉴 출력 및 메인 루프
# ============================================================================

def display_menu():
    """
    메뉴를 출력하고 사용자 선택을 받습니다.
    
    Returns:
        str: 사용자가 선택한 메뉴 번호
    """
    menu_text = """
╔════════════════════════════════════════╗
║      여행 맞춤 추천 AI 비서      ║
╚════════════════════════════════════════╝

다음 중 원하는 기능을 선택해주세요:

1. 여행지 정보 조회
   - 식당, 가볼 만한 곳, 숙소 추천 지역을 구분하여 제공

2. 여행 일정 생성
   - 숙소 위치, 인원, 기간을 입력하면 일정표와 이동경로 생성

3. 장소 조건 기반 추천
   - 원하는 조건을 입력하면 맞는 장소와 팁 제공

4. 종료

선택 (1-4): """
    
    choice = input(menu_text).strip()
    return choice


def display_welcome():
    """환영 메시지를 표시합니다"""
    welcome_text = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        🌍 여행 맞춤 추천 AI 비서에 오신 것을 환영합니다! 🌍       ║
║                                                            ║
║  Google Gemini API를 활용한 개인화된 여행 추천 서비스입니다.     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """
    print(welcome_text)


def display_goodbye():
    """종료 메시지를 표시합니다"""
    goodbye_text = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          감사합니다! 즐거운 여행 되세요! 👋                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """
    print(goodbye_text)


def handle_menu_choice(choice):
    """
    사용자의 메뉴 선택을 처리합니다.
    
    Args:
        choice (str): 사용자가 선택한 메뉴 번호
    
    Returns:
        bool: 프로그램 계속 실행 여부 (False = 종료)
    """
    if choice == "1":
        # 기능 1: 여행지 정보 조회
        feature_1_restaurant_guide()
        return True
    
    elif choice == "2":
        # 기능 2: 여행 일정 생성
        feature_2_travel_itinerary()
        return True
    
    elif choice == "3":
        # 기능 3: 조건 기반 장소 추천
        feature_3_place_recommendation()
        return True
    
    elif choice == "4":
        # 프로그램 종료
        display_goodbye()
        return False
    
    else:
        # 잘못된 선택
        print_error("1-4 사이의 숫자를 선택해주세요.")
        return True


def main():
    """
    메인 함수 - 프로그램 시작점
    메뉴를 표시하고 사용자 선택에 따라 기능을 실행합니다.
    """
    try:
        # 환영 메시지 표시
        display_welcome()
        
        # 메뉴 루프
        while True:
            choice = display_menu()
            if not handle_menu_choice(choice):
                # 사용자가 4번(종료)을 선택한 경우
                break
            
            # 다음 메뉴로 돌아가기 전 일시정지
            input("\n(Enter 키를 눌러 메뉴로 돌아가세요...)")
            print("\n" * 2)
    
    except KeyboardInterrupt:
        # 사용자가 Ctrl+C로 중단한 경우
        print("\n")
        display_goodbye()
    except Exception as e:
        print_error(f"프로그램 실행 중 오류 발생: {str(e)}")


# ============================================================================
# 프로그램 시작
# ============================================================================

if __name__ == "__main__":
    main()
