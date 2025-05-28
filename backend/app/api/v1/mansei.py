from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.mansei import ManseiResult
from app.schemas.mansei import ManseiRequest, ManseiResponse
from app.services.mansei import ManseiService
from app.services.redis import redis_service

router = APIRouter()

@router.post("/calculate", response_model=ManseiResponse)
async def calculate_mansei(
    request: ManseiRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """만세력 계산"""
    try:
        # 만세력 계산
        mansei_service = ManseiService()
        calculation_result = await mansei_service.calculate(request)
        
        # 데이터베이스에 저장
        db_result = ManseiResult(
            user_id=current_user.id,
            name=request.name,
            birth_date=request.birth_date.isoformat(),
            birth_time=request.birth_time.isoformat() if request.birth_time else None,
            gender=request.gender.value,
            calendar_type=request.calendar_type.value,
            month_type=request.month_type.value,
            saju_data=calculation_result
        )
        
        db.add(db_result)
        await db.commit()
        await db.refresh(db_result)
        
        # Redis에 캐시 저장
        cache_key = f"mansei:{current_user.id}:{db_result.id}"
        await redis_service.set_cache(cache_key, calculation_result, expire=3600)
        
        # 응답 생성
        response = ManseiResponse(
            id=db_result.id,
            name=db_result.name,
            gender=db_result.gender,
            birth_info={
                "date": db_result.birth_date,
                "time": db_result.birth_time,
                "calendar_type": db_result.calendar_type,
                "month_type": db_result.month_type
            },
            saju_pillars=calculation_result["saju_pillars"],
            lunar_info=calculation_result["lunar_info"],
            five_elements=calculation_result["five_elements"],
            interpretation=calculation_result["interpretation"],
            created_at=db_result.created_at
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"만세력 계산 중 오류 발생: {str(e)}"
        )

@router.get("/history", response_model=List[ManseiResponse])
async def get_mansei_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """사용자의 만세력 계산 기록 조회"""
    result = await db.execute(
        select(ManseiResult)
        .where(ManseiResult.user_id == current_user.id)
        .order_by(ManseiResult.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    mansei_results = result.scalars().all()
    
    responses = []
    for result in mansei_results:
        response = ManseiResponse(
            id=result.id,
            name=result.name,
            gender=result.gender,
            birth_info={
                "date": result.birth_date,
                "time": result.birth_time,
                "calendar_type": result.calendar_type,
                "month_type": result.month_type
            },
            saju_pillars=result.saju_data["saju_pillars"],
            lunar_info=result.saju_data["lunar_info"],
            five_elements=result.saju_data["five_elements"],
            interpretation=result.saju_data["interpretation"],
            created_at=result.created_at
        )
        responses.append(response)
    
    return responses

@router.get("/{mansei_id}", response_model=ManseiResponse)
async def get_mansei_result(
    mansei_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """특정 만세력 결과 조회"""
    # Redis 캐시 확인
    cache_key = f"mansei:{current_user.id}:{mansei_id}"
    cached_result = await redis_service.get_cache(cache_key)
    
    if cached_result:
        # 캐시된 데이터로 응답 생성
        result = await db.execute(
            select(ManseiResult)
            .where(ManseiResult.id == mansei_id, ManseiResult.user_id == current_user.id)
        )
        db_result = result.scalar_one_or_none()
        
        if not db_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="만세력 결과를 찾을 수 없습니다"
            )
        
        response = ManseiResponse(
            id=db_result.id,
            name=db_result.name,
            gender=db_result.gender,
            birth_info={
                "date": db_result.birth_date,
                "time": db_result.birth_time,
                "calendar_type": db_result.calendar_type,
                "month_type": db_result.month_type
            },
            saju_pillars=cached_result["saju_pillars"],
            lunar_info=cached_result["lunar_info"],
            five_elements=cached_result["five_elements"],
            interpretation=cached_result["interpretation"],
            created_at=db_result.created_at
        )
        
        return response
    
    # 데이터베이스에서 조회
    result = await db.execute(
        select(ManseiResult)
        .where(ManseiResult.id == mansei_id, ManseiResult.user_id == current_user.id)
    )
    
    mansei_result = result.scalar_one_or_none()
    
    if not mansei_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="만세력 결과를 찾을 수 없습니다"
        )
    
    response = ManseiResponse(
        id=mansei_result.id,
        name=mansei_result.name,
        gender=mansei_result.gender,
        birth_info={
            "date": mansei_result.birth_date,
            "time": mansei_result.birth_time,
            "calendar_type": mansei_result.calendar_type,
            "month_type": mansei_result.month_type
        },
        saju_pillars=mansei_result.saju_data["saju_pillars"],
        lunar_info=mansei_result.saju_data["lunar_info"],
        five_elements=mansei_result.saju_data["five_elements"],
        interpretation=mansei_result.saju_data["interpretation"],
        created_at=mansei_result.created_at
    )
    
    return response
