from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema, EventCreateSchema
router = APIRouter(
    prefix='/api/events'
)

@router.get('/')
def read_events() -> EventListSchema:
    return {"results": [{"id":6},{"id":7},{"id":8}], "count":3}

@router.post('/')
def create_events(payload:EventCreateSchema):
    return payload


@router.get('/{event_id}')
def get_event(event_id:int) -> EventSchema:
    return {"id": event_id}