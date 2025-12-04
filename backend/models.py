from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Event title")
    description: str = Field(..., min_length=1, max_length=2000, description="Event description")
    date: str = Field(..., description="Event date in ISO format (YYYY-MM-DD)")
    location: str = Field(..., min_length=1, max_length=300, description="Event location")
    capacity: int = Field(..., gt=0, le=100000, description="Event capacity (1-100000)")
    organizer: str = Field(..., min_length=1, max_length=200, description="Event organizer")
    status: str = Field(default="active", description="Event status")

    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Validate date format"""
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status values"""
        allowed_statuses = ['active', 'cancelled', 'completed', 'postponed']
        if v.lower() not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v.lower()


class EventCreate(EventBase):
    eventId: Optional[str] = Field(None, description="Optional custom event ID")


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    date: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    capacity: Optional[int] = Field(None, gt=0, le=100000)
    organizer: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v: Optional[str]) -> Optional[str]:
        """Validate date format if provided"""
        if v is not None:
            try:
                datetime.fromisoformat(v)
                return v
            except ValueError:
                raise ValueError('Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status values if provided"""
        if v is not None:
            allowed_statuses = ['active', 'cancelled', 'completed', 'postponed']
            if v.lower() not in allowed_statuses:
                raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
            return v.lower()
        return v


class Event(EventBase):
    eventId: str

    class Config:
        from_attributes = True
