from typing import Dict, Any, List
from datetime import date, time
from app.schemas.mansei import ManseiRequest
from app.utils.mansei_calculator import ManseiCalculator, SajuPillar

class ManseiService:
    def __init__(self):
        self.calculator = ManseiCalculator()
    
    async def calculate(self, request: ManseiRequest) -> Dict[str, Any]:
        """만세력 계산 메인 로직"""
        # 사주 네 기둥 계산
        year_pillar = self.calculator.get_year_pillar(request.birth_date.year)
        month_pillar = self.calculator.get_month_pillar(request.birth_date.year, request.birth_date.month)
        day_pillar = self.calculator.get_day_pillar(request.birth_date)
        hour_pillar = self.calculator.get_hour_pillar(request.birth_time, day_pillar.heavenly_stem)
        
        pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
        
        # 오행 분석
        five_elements = self.calculator.analyze_five_elements(pillars)
        
        # 해석
        interpretation = self.calculator.get_interpretation(pillars, request.gender, five_elements)
        
        # 음력 정보
        lunar_info = {
            "calendar_type": request.calendar_type.value,
            "month_type": request.month_type.value,
            "note": "정확한 음력 변환을 위해서는 한국천문연구원 API 연동이 필요합니다"
        }
        
        result = {
            "saju_pillars": {
                "year": str(year_pillar),
                "month": str(month_pillar),
                "day": str(day_pillar),
                "hour": str(hour_pillar)
            },
            "lunar_info": lunar_info,
            "five_elements": five_elements,
            "interpretation": interpretation
        }
        
        return result
