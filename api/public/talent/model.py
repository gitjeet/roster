from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class VideoBase(SQLModel):
    url: str


class Video(VideoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employer_id: int = Field(foreign_key="employer.id")
    employer: Optional["Employer"] = Relationship(back_populates="videos")


class VideoRead(VideoBase):
    id: int


class EmployerBase(SQLModel):
    name: str


class Employer(EmployerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    talent_id: int = Field(foreign_key="talent.id")
    videos: List[Video] = Relationship(back_populates="employer")
    talent: Optional["Talent"] = Relationship(back_populates="employers")


class EmployerRead(EmployerBase):
    id: int
    videos: List[VideoRead]


class TalentBase(SQLModel):
    username: str
    name: Optional[str]
    bio: Optional[str]
    email: str
    website: str

class Talent(TalentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employers: List[Employer] = Relationship(back_populates="talent")


class TalentCreate(TalentBase):
    pass


class TalentRead(TalentBase):
    id: int
    employers: List[EmployerRead]
