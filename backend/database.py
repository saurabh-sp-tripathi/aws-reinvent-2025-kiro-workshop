import boto3
import os
from typing import List, Optional
from uuid import uuid4
from models import Event, EventCreate, EventUpdate

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'Events')
table = dynamodb.Table(table_name)


def create_event(event: EventCreate) -> Event:
    """Create a new event in DynamoDB"""
    event_data = event.model_dump()
    # Use provided eventId or generate a new one
    event_id = event_data.pop('eventId', None) or str(uuid4())
    item = {
        'eventId': event_id,
        **event_data
    }
    table.put_item(Item=item)
    return Event(**item)


def get_event(event_id: str) -> Optional[Event]:
    """Get an event by ID"""
    response = table.get_item(Key={'eventId': event_id})
    item = response.get('Item')
    return Event(**item) if item else None


def list_events() -> List[Event]:
    """List all events"""
    response = table.scan()
    items = response.get('Items', [])
    return [Event(**item) for item in items]


def update_event(event_id: str, event_update: EventUpdate) -> Optional[Event]:
    """Update an event"""
    # Build update expression
    update_data = {k: v for k, v in event_update.model_dump().items() if v is not None}
    
    if not update_data:
        return get_event(event_id)
    
    update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
    expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
    expression_attribute_values = {f":{k}": v for k, v in update_data.items()}
    
    try:
        table.update_item(
            Key={'eventId': event_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return get_event(event_id)
    except Exception:
        return None


def delete_event(event_id: str) -> bool:
    """Delete an event"""
    try:
        table.delete_item(Key={'eventId': event_id})
        return True
    except Exception:
        return False
