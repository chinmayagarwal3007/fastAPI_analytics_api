from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import DateTime, SQLModel, Field



def get_utc_now():
    return datetime.now(timezone.utc)

class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default = "")

class EventUpdateSchema(SQLModel):
    description: str


class EventModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime = Field(default_factory=get_utc_now, sa_type=DateTime, nullable=False)
    updated_at: datetime = Field(default_factory=get_utc_now, sa_type=DateTime, nullable=False) 

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: Optional[int] = None