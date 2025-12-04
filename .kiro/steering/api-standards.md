---
inclusion: fileMatch
fileMatchPattern: '(routes|api|endpoints|main|handler)\.py$'
---

# API Standards and Conventions

This steering file defines REST API standards and conventions for the Events API project. These guidelines ensure consistency, maintainability, and adherence to best practices across all API endpoints.

## HTTP Methods

Use HTTP methods according to their semantic meaning:

### GET
- **Purpose**: Retrieve resources
- **Idempotent**: Yes
- **Safe**: Yes (no side effects)
- **Request Body**: Not allowed
- **Usage**:
  - `GET /events` - List all events
  - `GET /events/{id}` - Get a specific event
  - `GET /events?status=active` - Filter events

### POST
- **Purpose**: Create new resources
- **Idempotent**: No
- **Safe**: No
- **Request Body**: Required
- **Usage**:
  - `POST /events` - Create a new event
- **Response**: Return the created resource with `201 Created` status

### PUT
- **Purpose**: Update existing resources (full or partial update)
- **Idempotent**: Yes
- **Safe**: No
- **Request Body**: Required
- **Usage**:
  - `PUT /events/{id}` - Update an event
- **Response**: Return the updated resource with `200 OK` status

### DELETE
- **Purpose**: Remove resources
- **Idempotent**: Yes
- **Safe**: No
- **Request Body**: Not allowed
- **Usage**:
  - `DELETE /events/{id}` - Delete an event
- **Response**: `204 No Content` or `200 OK` with confirmation message

### PATCH (Optional)
- **Purpose**: Partial updates (when PUT is used for full replacement)
- **Idempotent**: No
- **Safe**: No
- **Request Body**: Required (only fields to update)

## HTTP Status Codes

Use appropriate status codes to communicate the result of API operations:

### Success Codes (2xx)

- **200 OK**: Successful GET, PUT, or DELETE with response body
- **201 Created**: Successful POST that creates a resource
  - Include `Location` header with the URI of the created resource
- **204 No Content**: Successful DELETE or PUT with no response body

### Client Error Codes (4xx)

- **400 Bad Request**: Invalid request syntax or validation error
  - Use for: Missing required fields, invalid data types, business rule violations
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Authenticated but not authorized to access resource
- **404 Not Found**: Resource does not exist
  - Use for: Invalid resource IDs, non-existent endpoints
- **409 Conflict**: Request conflicts with current state
  - Use for: Duplicate resource creation, concurrent modification conflicts
- **422 Unprocessable Entity**: Validation errors
  - Use for: Pydantic validation failures, schema violations
- **429 Too Many Requests**: Rate limit exceeded

### Server Error Codes (5xx)

- **500 Internal Server Error**: Unexpected server error
  - Use for: Unhandled exceptions, database errors
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Service temporarily unavailable
- **504 Gateway Timeout**: Upstream server timeout

## Error Response Format

All error responses must follow a consistent JSON structure:

### Standard Error Response

```json
{
  "detail": "Human-readable error message",
  "error_code": "OPTIONAL_ERROR_CODE",
  "timestamp": "2024-12-03T10:30:00Z"
}
```

### Validation Error Response (422)

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "capacity",
      "message": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    },
    {
      "field": "date",
      "message": "Date must be in ISO format (YYYY-MM-DD)",
      "type": "value_error"
    }
  ]
}
```

### Not Found Error Response (404)

```json
{
  "detail": "Event with ID abc-123 not found"
}
```

### Internal Server Error Response (500)

```json
{
  "detail": "Internal server error",
  "message": "An unexpected error occurred"
}
```

**Note**: Never expose sensitive information (stack traces, database details) in production error responses.

## JSON Response Format Standards

### Success Response Structure

#### Single Resource
```json
{
  "eventId": "uuid-string",
  "title": "Event Title",
  "description": "Event description",
  "date": "2024-12-15",
  "location": "Event Location",
  "capacity": 200,
  "organizer": "Organizer Name",
  "status": "active"
}
```

#### Collection of Resources
```json
[
  {
    "eventId": "uuid-1",
    "title": "Event 1",
    ...
  },
  {
    "eventId": "uuid-2",
    "title": "Event 2",
    ...
  }
]
```

#### Paginated Collection (Future Enhancement)
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "next": "/events?page=2",
  "previous": null
}
```

### Field Naming Conventions

- Use **camelCase** for JSON field names (e.g., `eventId`, `firstName`)
- Be consistent across all endpoints
- Use descriptive, self-documenting names
- Avoid abbreviations unless widely understood

### Data Types

- **Strings**: Use for text, IDs, enums
- **Numbers**: Use integers for counts, floats for decimals
- **Booleans**: Use `true`/`false` (lowercase)
- **Dates**: Use ISO 8601 format (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`)
- **Arrays**: Use for collections
- **Objects**: Use for nested structures
- **Null**: Use `null` for absent optional values (not empty strings)

## Request Validation

### Required Fields
- Validate all required fields are present
- Return `400 Bad Request` if required fields are missing

### Data Type Validation
- Validate data types match schema
- Return `422 Unprocessable Entity` for type mismatches

### Business Rule Validation
- Validate business constraints (e.g., capacity > 0, valid status values)
- Return `400 Bad Request` or `422 Unprocessable Entity` with clear error messages

### String Length Validation
- Enforce minimum and maximum lengths
- Provide clear error messages indicating the valid range

### Date Validation
- Validate date format (ISO 8601)
- Optionally validate date ranges (e.g., event date must be in the future)

## Query Parameters

### Filtering
- Use query parameters for filtering: `GET /events?status=active`
- Support multiple filters: `GET /events?status=active&location=Vegas`
- Use clear, descriptive parameter names

### Sorting
- Use `sort` parameter: `GET /events?sort=date`
- Support ascending/descending: `GET /events?sort=-date` (minus for descending)

### Pagination (Future Enhancement)
- Use `page` and `page_size` parameters
- Default to reasonable page size (e.g., 20)
- Include pagination metadata in response

### Field Selection (Future Enhancement)
- Use `fields` parameter: `GET /events?fields=title,date,location`
- Return only requested fields to reduce payload size

## CORS Configuration

- Configure appropriate CORS headers for web clients
- In development: Allow all origins (`*`)
- In production: Specify allowed origins explicitly
- Allow necessary HTTP methods: `GET, POST, PUT, DELETE, OPTIONS`
- Allow necessary headers: `Content-Type, Authorization, Accept`

## Security Best Practices

### Input Sanitization
- Sanitize all user input to prevent injection attacks
- Validate against expected patterns (regex for emails, URLs, etc.)

### Authentication & Authorization
- Implement authentication for protected endpoints
- Use JWT tokens or API keys
- Include `Authorization` header in requests
- Return `401 Unauthorized` for missing/invalid credentials
- Return `403 Forbidden` for insufficient permissions

### Rate Limiting
- Implement rate limiting to prevent abuse
- Return `429 Too Many Requests` when limit exceeded
- Include `Retry-After` header with retry time

### HTTPS Only
- Always use HTTPS in production
- Redirect HTTP to HTTPS

## Logging and Monitoring

### Request Logging
- Log all incoming requests with timestamp, method, path, status code
- Include request ID for tracing
- Log response time for performance monitoring

### Error Logging
- Log all errors with full context (stack trace, request details)
- Use appropriate log levels (ERROR, WARNING, INFO, DEBUG)
- Never log sensitive data (passwords, tokens, PII)

### Metrics
- Track request count, error rate, response time
- Monitor by endpoint and status code
- Set up alerts for anomalies

## Versioning (Future Enhancement)

When API versioning is needed:
- Use URL path versioning: `/v1/events`, `/v2/events`
- Or use header versioning: `Accept: application/vnd.api.v1+json`
- Maintain backward compatibility when possible
- Deprecate old versions gracefully with advance notice

## Documentation

### Endpoint Documentation
- Document all endpoints with:
  - HTTP method and path
  - Description of functionality
  - Request parameters (path, query, body)
  - Request body schema with examples
  - Response schema with examples
  - Possible status codes and error responses

### OpenAPI/Swagger
- FastAPI automatically generates OpenAPI documentation
- Access at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- Keep docstrings updated for accurate documentation

## Testing Standards

### Unit Tests
- Test each endpoint independently
- Mock database operations
- Test success and error cases
- Validate response structure and status codes

### Integration Tests
- Test complete request/response cycle
- Use test database
- Test authentication and authorization
- Test error handling

### Test Coverage
- Aim for >80% code coverage
- Cover all error paths
- Test edge cases and boundary conditions

## Code Organization

### Route Handlers
- Keep route handlers thin - delegate to service layer
- Handle only HTTP concerns (request/response)
- Use dependency injection for database connections

### Error Handling
- Use try-except blocks for expected errors
- Let FastAPI handle validation errors automatically
- Implement global exception handlers for unexpected errors
- Return consistent error response format

### Validation
- Use Pydantic models for request/response validation
- Define field validators for complex validation logic
- Use Field() for constraints (min_length, max_length, gt, le, etc.)

## Example Implementation

```python
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from models import Event, EventCreate, EventUpdate
import database

router = APIRouter(prefix="/events", tags=["events"])

@router.post("", response_model=Event, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):
    """
    Create a new event.
    
    - Returns 201 with created event
    - Returns 422 for validation errors
    - Returns 500 for server errors
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
    status: Optional[str] = Query(None, description="Filter by status")
):
    """
    List all events with optional filtering.
    
    - Returns 200 with list of events
    - Returns 500 for server errors
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
```

## Checklist for New Endpoints

When creating a new API endpoint, ensure:

- [ ] HTTP method is semantically correct
- [ ] Appropriate status codes are used
- [ ] Request validation is implemented
- [ ] Error handling is comprehensive
- [ ] Error responses follow standard format
- [ ] Response format is consistent with other endpoints
- [ ] Endpoint is documented with docstring
- [ ] Logging is implemented
- [ ] Unit tests are written
- [ ] Integration tests are written
- [ ] CORS is configured if needed
- [ ] Authentication/authorization is implemented if needed

---

**Remember**: Consistency is key. Follow these standards across all API endpoints to ensure a predictable, maintainable, and developer-friendly API.
