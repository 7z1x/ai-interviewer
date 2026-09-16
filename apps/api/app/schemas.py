from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    target_role: str = Field(min_length=1, max_length=200)
    job_description: str = Field(min_length=1, max_length=10000)
    language: Literal["id", "en"]


class SessionResponse(BaseModel):
    id: uuid.UUID
    target_role: str
    job_description: str
    language: str
    status: str
    plan_summary: dict | None = None
    current_question_index: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionListItem(BaseModel):
    id: uuid.UUID
    target_role: str
    status: str
    language: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionListResponse(BaseModel):
    items: list[SessionListItem]
    total: int
    page: int
    page_size: int


class ErrorDetail(BaseModel):
    field: str
    issue: str


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] | None = None
    request_id: str


class ErrorResponse(BaseModel):
    error: ErrorEnvelope
