from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InterviewSession
from app.repositories.sessions import SessionRepository
from app.schemas import SessionCreate


class SessionService:
    """Business rules for InterviewSession lifecycle.

    Route layer must not query DB directly — all access via this service.
    Status transitions validated here; DB CHECK constraints are safety net only.
    """

    VALID_STATUSES = {"draft", "ready", "in_progress", "completed", "abandoned"}

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = SessionRepository(db)

    async def create(self, payload: SessionCreate) -> InterviewSession:
        return await self.repo.create(
            target_role=payload.target_role,
            job_description=payload.job_description,
            language=payload.language,
        )

    async def get(self, session_id: uuid.UUID) -> InterviewSession | None:
        return await self.repo.get_by_id(session_id)

    async def list(self, *, page: int, page_size: int, status: str | None) -> tuple[list[InterviewSession], int]:
        if status is not None and status not in self.VALID_STATUSES:
            # Let API layer return 422 via query param validation; this is fallback
            raise ValueError(f"Invalid status filter: {status}")
        items, total = await self.repo.list_paginated(page=page, page_size=page_size, status=status)
        return list(items), total

    async def delete_draft(self, session: InterviewSession) -> None:
        if session.status != "draft":
            raise ValueError("Only draft sessions can be deleted.")
        await self.repo.delete(session)
