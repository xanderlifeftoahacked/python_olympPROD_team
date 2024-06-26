from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    name: str
    longitude: float
    latitude: float


class BusinessType(Enum):
    organisation = "ООО"
    individual = "ИП"


class ParticipantSchema(BaseModel):
    name: str
    position: str
    phone_number: str


class AgentSchema(BaseModel):
    id: int
    name: str
    description: str
    phone_number: str  # regex
    photo: str  # link


class MeetingAddSchema(BaseModel):
    date: datetime  # DATEFORMAT: DD.MM.YYYY HH:MM:SS
    agent_id: int | None = None
    place: LocationSchema
    participants: list[ParticipantSchema]


class MeetingUpdateSchema(BaseModel):
    place: LocationSchema | None = None
    participants: list[ParticipantSchema] | None = None
    date: datetime | None = None


class DocumentsSchema(BaseModel):
    id: int
    documents: list[str]


class MeetingSchema(MeetingAddSchema):
    id: int
    agent_id: int | None = Field(exclude=True, default=None)
    documents: DocumentsSchema | None = None
    agent: AgentSchema | None = None
    is_canceled: bool = False
    type: BusinessType
