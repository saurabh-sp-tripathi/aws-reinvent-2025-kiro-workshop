from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from models import Event, EventCreate, EventUpdate
import database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"], redirect_slashes=False)


@router.post("", response_model=Event, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):
    """
    Create a new event
    
    - **title**: Event title (1-200 characters)
    - **description**: Event description (1-2000 characters)
    - **date**: Event date in ISO format (YYYY-MM-DD)
    - **location**: Event location (1-300 characters)
    - **capacity**: Event capacity (1-100000)
    - **organizer**: Event organizer (1-200 characters)
    - **status**: Event status (active, cancelled, completed, postponed)
    """
    try:
        return database.create_event(event)
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event"
        )


@router.get("", response_model=List[Event])
@router.get("/", response_model=List[Event])
def list_events(
    status: str = Query(None, description="Filter by status (active, cancelled, completed, postponed)")
):
    """
    List all events
    
    Optional query parameters:
    - **status**: Filter events by status
    """
    try:
        events = database.list_events()
        if status:
            events = [e for e in events if e.status.lower() == status.lower()]
        return events
    except Exception as e:
        logger.error(f"Error listing events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve events"
        )


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: str):
    """
    Get a specific event by ID
    
    - **event_id**: UUID of the event
    """
    if not event_id or not event_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event ID is required"
        )
    
    try:
        event = database.get_event(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        return event
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving event {event_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve event"
        )


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: str, event_update: EventUpdate):
    """
    Update an event
    
    - **event_id**: UUID of the event
    - All fields are optional, only provided fields will be updated
    """
    if not event_id or not event_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event ID is required"
        )
    
    # Check if at least one field is provided
    if not any(v is not None for v in event_update.model_dump().values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )
    
    try:
        # Check if event exists first
        existing_event = database.get_event(event_id)
        if not existing_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        
        event = database.update_event(event_id, event_update)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update event"
            )
        return event
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating event {event_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update event"
        )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: str):
    """
    Delete an event
    
    - **event_id**: UUID of the event
    """
    if not event_id or not event_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event ID is required"
        )
    
    try:
        # Check if event exists first
        existing_event = database.get_event(event_id)
        if not existing_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        
        success = database.delete_event(event_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete event"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting event {event_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete event"
        )
