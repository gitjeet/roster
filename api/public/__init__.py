from fastapi import APIRouter, Depends

from api.auth import authent

from api.public.talent import views as talent 
api = APIRouter()


api.include_router(
    talent.router,
    prefix="/talents",  
    tags=["Talents"],
    dependencies=[Depends(authent)],
)