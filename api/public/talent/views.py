from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from api.database import get_session
from .model import TalentCreate, TalentRead
from .crud import create_talent, get_talent_by_username, update_talent, delete_talent
from api.utils.scraper import process_website

router = APIRouter(prefix="/talent", tags=["Talent"])


@router.post("/scrape", response_model=TalentRead)
def create_from_website(url: str, db: Session = Depends(get_session)):
    structured_data = process_website(url)
    return create_talent(TalentCreate(**structured_data), db)


@router.get("/{username}", response_model=TalentRead)
def get_profile(username: str, db: Session = Depends(get_session)):
    return get_talent_by_username(username, db)


@router.patch("/{username}", response_model=TalentRead)
def edit_profile(username: str, updates: dict, db: Session = Depends(get_session)):
    return update_talent(username, updates, db)


@router.delete("/{username}")
def delete_profile(username: str, db: Session = Depends(get_session)):
    delete_talent(username, db)
    return {"detail": "Profile deleted"}
