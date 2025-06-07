from fastapi import APIRouter, Depends, HTTPException, status

from orm import admin_delete, check_admin, new_admin_set
from schemas import CheckAdmin, DeleteAdmin, SetAdmin
from jwt_config import security


router = APIRouter(
    prefix="/admins",
    tags=["admins"]
)

@router.post("/set_new_admin/", dependencies=[Depends(security.access_token_required)])
async def set_new_admin(set_admin: SetAdmin, verify_admin: CheckAdmin):
    if not await check_admin(verify_admin.username, verify_admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have administrator privileges"
        )
    
    return await new_admin_set(set_admin.username)


@router.post("/delete_admin/", dependencies=[Depends(security.access_token_required)])
async def delete_admin(delete_admin: DeleteAdmin, check_admins: CheckAdmin):
    if await check_admin(check_admins.username, check_admins.password):
        try:
            return await admin_delete(delete_admin.username, delete_admin.reason)
        
        except Exception as e:
            print(f"Error: {e}")