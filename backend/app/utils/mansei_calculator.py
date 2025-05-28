from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import date, time
from app.schemas.mansei import Gender

@dataclass
class SajuPillar:
    """사주 기둥 (연주, 월주, 일주, 시주)"""
    heavenly_stem: str  # 천간
    earthly_branch: str  # 지지

    def __str__(self):
        return f"{self.heavenly_stem}{self.earthly_branch}"

class ManseiCalculator:
    # 천간 (10개)
    HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]

    # 지지 (12개)
    EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

    # 오행
    FIVE_ELEMENTS = {
        "갑": "목", "을": "목", "병": "화", "정": "화", "무": "토",
        "기": "토", "경": "금", "신": "금", "임": "수", "계": "수",
        "자": "수", "축": "토", "인": "목", "묘": "목", "진": "토",
        "사": "화", "오": "화", "미": "토", "신": "금", "유": "금",
        "술": "토", "해": "수"
    }

    # 음양
    YIN_YANG = {
        "갑": "양", "을": "음", "병": "양", "정": "음", "무": "양",
        "기": "음", "경": "양", "신": "음", "임": "양", "계": "음",
        "자": "양", "축": "음", "인": "양", "묘": "음", "진": "양",
        "사": "음", "오": "양", "미": "음", "신": "양", "유": "음",
        "술": "양", "해": "음"
    }

    def get_year_pillar(self, year: int) -> SajuPillar:
        """연주 계산 (갑자년 기준)"""
        # 1984년이 갑자년 (천간의 시작점)
        base_year = 1984
        year_diff = year - base_year

        stem_index = year_diff % 10
        branch_index = year_diff % 12

        return SajuPillar(
            self.HEAVENLY_STEMS[stem_index],
            self.EARTHLY_BRANCHES[branch_index]
        )

    def get_month_pillar(self, year: int, month: int) -> SajuPillar:
        """월주 계산"""
        # 갑자년 정월(인월)을 기준으로 계산
        base_month = (year - 1984) * 12 + (month - 3)
        if month < 3:
            base_month -= 12

        stem_index = base_month % 10
        branch_index = base_month % 12

        return SajuPillar(
            self.HEAVENLY_STEMS[stem_index],
            self.EARTHLY_BRANCHES[branch_index]
        )

    def get_day_pillar(self, birth_date: date) -> SajuPillar:
        """일주 계산 (갑자일 기준)"""
        # 1984년 2월 2일이 갑자일
        base_date = date(1984, 2, 2)
        days_diff = (birth_date - base_date).days

        stem_index = days_diff % 10
        branch_index = days_diff % 12

        return SajuPillar(
            self.HEAVENLY_STEMS[stem_index],
            self.EARTHLY_BRANCHES[branch_index]
        )

    def get_hour_pillar(self, birth_time: Optional[time], day_stem: str) -> SajuPillar:
        """시주 계산"""
        if not birth_time:
            hour = 12  # 정오
        else:
            hour = birth_time.hour

        # 시지 결정
        if hour == 23 or hour < 1:
            branch_index = 0  # 자시
        else:
            branch_index = (hour + 1) // 2

        # 시간 천간은 일간에 따라 결정
        day_stem_index = self.HEAVENLY_STEMS.index(day_stem)
        hour_stem_base = (day_stem_index % 5) * 2
        hour_stem_index = (hour_stem_base + branch_index) % 10

        return SajuPillar(
            self.HEAVENLY_STEMS[hour_stem_index],
            self.EARTHLY_BRANCHES[branch_index]
        )

    def analyze_five_elements(self, pillars: List[SajuPillar]) -> Dict[str, int]:
        """오행 분석"""
        elements_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}

        for pillar in pillars:
            elements_count[self.FIVE_ELEMENTS[pillar.heavenly_stem]] += 1
            elements_count[self.FIVE_ELEMENTS[pillar.earthly_branch]] += 1

        return elements_count

    def get_interpretation(self, pillars: List[SajuPillar], gender: Gender,
                         five_elements: Dict[str, int]) -> Dict[str, Any]:
        """기본적인 해석 제공"""
        day_stem = pillars[2].heavenly_stem
        day_element = self.FIVE_ELEMENTS[day_stem]
        day_yin_yang = self.YIN_YANG[day_stem]

        max_element = max(five_elements.items(), key=lambda x: x[1])
        min_element = min(five_elements.items(), key=lambda x: x[1])

        interpretation = {
            "day_master": {
                "stem": day_stem,
                "element": day_element,
                "yin_yang": day_yin_yang,
                "description": f"{day_element}({day_yin_yang})의 기운을 가진 사람"
            },
            "five_elements_balance": {
                "strongest": max_element[0],
                "weakest": min_element[0],
                "analysis": f"{max_element[0]} 기운이 강하고 {min_element[0]} 기운이 부족함"
            },
            "general_traits": self.get_general_traits(day_stem),
            "recommendations": self.get_recommendations(day_element, five_elements)
        }

        return interpretation

    def get_general_traits(self, day_stem: str) -> List[str]:
        """일간별 기본 성격 특성"""
        traits = {
            "갑": ["리더십이 강함", "정직하고 꿋꿋함", "진취적이고 적극적"],
            "을": ["부드럽고 유연함", "배려심이 깊음", "예술적 감각"],
            "병": ["밝고 활발함", "사교적이고 열정적", "창의력이 뛰어남"],
            "정": ["세심하고 섬세함", "온화하고 친절함", "감정이 풍부함"],
            "무": ["안정적이고 신뢰감", "포용력이 크고 인내심", "실용적 사고"],
            "기": ["성실하고 근면함", "조화를 중시함", "꼼꼼하고 치밀함"],
            "경": ["의지가 강함", "원칙을 중시함", "결단력과 추진력"],
            "신": ["섬세하고 완벽주의", "미적 감각이 뛰어남", "변화를 추구함"],
            "임": ["포용력이 크고 관대함", "적응력이 뛰어남", "지혜롭고 깊이 있음"],
            "계": ["온순하고 부드러움", "직감력이 뛰어남", "감성적이고 낭만적"]
        }
        return traits.get(day_stem, ["분석 정보 부족"])

    def get_recommendations(self, day_element: str, five_elements: Dict[str, int]) -> List[str]:
        """오행 균형에 따른 조언"""
        recommendations = []

        sorted_elements = sorted(five_elements.items(), key=lambda x: x[1])
        weakest = sorted_elements[0][0]

        element_advice = {
            "목": "녹색 계열 색상, 나무 소재, 동쪽 방향 활용",
            "화": "빨간색 계열 색상, 햇빛, 남쪽 방향 활용",
            "토": "노란색, 갈색 계열, 도자기, 중앙 위치",
            "금": "흰색, 금속 소재, 서쪽 방향 활용",
            "수": "검은색, 파란색 계열, 물, 북쪽 방향"
        }

        recommendations.append(f"{weakest} 기운 보강: {element_advice[weakest]}")

        return recommendations
