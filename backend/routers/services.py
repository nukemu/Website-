from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from jwt_config import security
from schemas import ServiceAdd, CheckAdmin
from orm import check_admin, service_add, service_get


router = APIRouter(
    prefix="/service",
    tags=["services"]
)

@router.get("/get_service/")
async def get_service(
    name: str | None = None,
    service_type: str | None = None,
    price: int | None = None
):
    return await service_get(name, service_type, price)
    

@router.post("/add_service/", dependencies=[Depends(security.access_token_required)])
async def add_service(adding: ServiceAdd, check_admins: CheckAdmin):
    if not await check_admin(check_admins.username, check_admins.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have administrator privileges"
        )
        
    return await service_add(adding.name, adding.service_type, adding.price)