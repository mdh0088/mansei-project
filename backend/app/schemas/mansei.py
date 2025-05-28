from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime, date, time
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class CalendarType(str, Enum):
    SOLAR = "solar"
    LUNAR = "lunar"

class MonthType(str, Enum):
    REGULAR = "regular"
    LEAP = "leap"

class ManseiRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    gender: Gender
    calendar_type: CalendarType
    month_type: MonthType = MonthType.REGULAR
    birth_date: date
    birth_time: Optional[time] = None
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v > date.today():
            raise ValueError('생년월일은 오늘 이전이어야 합니다')
        if v.year < 1900:
            raise ValueError('1900년 이후 생년월일만 지원합니다')
        return v

class ManseiResponse(BaseModel):
    id: int
    name: str
    gender: str
    birth_info: Dict[str, Any]
    saju_pillars: Dict[str, str]
    lunar_info: Dict[str, Any]
    five_elements: Dict[str, int]
    interpretation: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
