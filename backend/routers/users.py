from fastapi import APIRouter, Depends

from orm import check_admin, user_ban, user_unbann
from schemas import BanUser, CheckAdmin, UnbannUsers
from jwt_config import security


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/ban/", dependencies=[Depends(security.access_token_required)])
async def ban_user(check_admins: CheckAdmin, ban_user: BanUser):
    if await check_admin(check_admins.username, check_admins.password):
        try:
            return await user_ban(ban_user.username, ban_user.reason, ban_user.hours)
        
        except Exception as e:
            print(f"Error: {e}")
            

@router.post("/unbanned/", dependencies=[Depends(security.access_token_required)])
async def unbanned(check_admins: CheckAdmin, unbann: UnbannUsers):
    if await check_admin(check_admins.username, check_admins.password):
        try:
            return await user_unbann(unbann.username)

        except Exception as e:
            print(f"Error: {e}")
            