from fastapi import APIRouter, Depends, HTTPException
from ...db import get_session
from sqlmodel import Session, select
from typing import List
from ...models import EventModel, EventCreateSchema, EventListSchema, EventUpdateSchema, get_utc_now
#from ...schemas import EventSchema, EventListSchema, EventCreateSchema, EventUpdateSchema
router = APIRouter(
    prefix='/api/events'
)



@router.get('/', response_model=EventListSchema)
def read_events(db: Session = Depends(get_session)):
    result = select(EventModel).order_by(EventModel.updated_at.asc()).limit(10)
    data = db.exec(result).all()
    return {"results": data, "count":len(data)}

@router.post('/', response_model=EventModel)
def create_events(payload:EventCreateSchema, db: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return data 


@router.get('/{event_id}', response_model=EventModel)
def get_event(event_id:int, db: Session = Depends(get_session)):
    result = select(EventModel).where(EventModel.id == event_id)
    data = db.exec(result).first()
    return data

@router.put('/update/{event_id}', response_model=EventModel)
def update_event(event_id:int, payload:EventUpdateSchema, db: Session = Depends(get_session)):
    result = select(EventModel).where(EventModel.id == event_id)
    data = db.exec(result).first()
    if not data:
        raise HTTPException(status=404, detail="Event not Found")
    data.description = payload.description
    data.updated_at = get_utc_now()
    db.commit()
    db.refresh(data)
    return data

@router.delete('/delete/{event_id}')
def delete_event(event_id: int, db: Session = Depends(get_session)):
    result = select(EventModel).where(EventModel.id == event_id)
    data = db.exec(result).first()
    if not data:
        raise HTTPException(status_code=404, detail = "Event not found")
    db.delete(data)
    db.commit()
    return {"msg": "Event Deleted Successfully"}