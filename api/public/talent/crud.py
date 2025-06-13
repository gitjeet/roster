from sqlmodel import Session, select
from fastapi import HTTPException, status
from .model import Talent, TalentCreate, Employer, Video


def create_talent(talent: TalentCreate, db: Session):
    db_talent = Talent.model_validate(talent)
    db.add(db_talent)
    db.commit()
    db.refresh(db_talent)
    return db_talent


def get_talent_by_username(username: str, db: Session):
    statement = select(Talent).where(Talent.username == username)
    talent = db.exec(statement).first()
    if not talent:
        raise HTTPException(status_code=404, detail="Talent not found")
    return talent


def update_talent(username: str, data: dict, db: Session):
    talent = get_talent_by_username(username, db)
    for key, value in data.items():
        setattr(talent, key, value)
    db.commit()
    db.refresh(talent)
    return talent


def delete_talent(username: str, db: Session):
    talent = get_talent_by_username(username, db)
    db.delete(talent)
    db.commit()
