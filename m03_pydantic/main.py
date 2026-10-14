# List and Optional provide type hints compatible with Python 3.8.
from typing import List, Optional

# BaseModel defines data schemas.
# EmailStr validates email addresses.
# Field defines validation constraints and default values.
# validator defines custom validation in Pydantic v1.
from pydantic import BaseModel, EmailStr, Field, validator

# FastAPI creates our API application.
from fastapi import FastAPI


# Create the FastAPI application.
app = FastAPI(title="Pydantic Practice")


# REQUEST MODEL
# Defines the structure of the JSON clients must send.
class SubscriberCreate(BaseModel):
    """Shape of the JSON a client must send to create a subscriber."""

    # Require a valid email address.
    email: EmailStr

    # Require a name containing between 1 and 60 characters.
    name: str = Field(min_length=1, max_length=60)

    # Create an independent empty list when tags are not provided.
    tags: List[str] = Field(default_factory=list)

    # Allow a phone number to be provided or left as None.
    phone: Optional[str] = None

    # Run this validator when processing the name.
    @validator("name")
    def clean_name(cls, value):
        """Remove surrounding whitespace and capitalize each word."""
        return value.strip().title()

    # Run this validator when processing the tags.
    @validator("tags")
    def lowercase_tags(cls, value):
        """Remove surrounding whitespace and convert tags to lowercase."""
        return [tag.strip().lower() for tag in value]


# RESPONSE MODEL
# Defines which fields the API returns to its client.
class SubscriberOut(BaseModel):
    """Shape of the JSON the API will return to the client."""

    # The ID assigned to the subscriber.
    id: int

    # The subscriber's validated email address.
    email: EmailStr

    # The subscriber's name.
    name: str

    # The subscriber's tags.
    tags: List[str]


# Register a POST endpoint at /subscribers.
# FastAPI validates the returned data against SubscriberOut.
# HTTP 201 means the resource was created.
@app.post(
    "/subscribers",
    response_model=SubscriberOut,
    status_code=201
)
def create_subscriber(payload: SubscriberCreate):

    # FastAPI validates the request before calling this function.
    # payload is a validated SubscriberCreate object.

    # Convert the Pydantic model into a regular Python dictionary.
    data = payload.dict()

    # Simulate saving the subscriber.
    # A real application would normally save this in a database.
    saved = {
        "id": 1,
        "internal_note": "VIP lead",
        **data
    }

    # Return the saved data.
    # FastAPI filters the response using SubscriberOut.
    return saved