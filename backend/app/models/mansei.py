from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models import Base

class ManseiResult(Base):
    __tablename__ = "mansei_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    birth_time = Column(String, nullable=True)
    gender = Column(String, nullable=False)
    calendar_type = Column(String, nullable=False)
    month_type = Column(String, nullable=False)
    saju_data = Column(JSON, nullable=False)  # 사주 계산 결과
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="mansei_results")
