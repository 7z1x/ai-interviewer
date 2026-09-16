from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InterviewSession


class SessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, *, target_role: str, job_description: str, language: str) -> InterviewSession:
        session = InterviewSession(
            target_role=target_role.strip(),
            job_description=job_description.strip(),
            language=language,
            status="draft",
            current_question_index=0,
        )
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def get_by_id(self, session_id: uuid.UUID) -> InterviewSession | None:
        result = await self.db.execute(
            select(InterviewSession).where(InterviewSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_paginated(
        self, *, page: int, page_size: int, status: str | None = None
    ) -> tuple[Sequence[InterviewSession], int]:
        base = select(InterviewSession)
        count_q = select(func.count()).select_from(InterviewSession)
        if status is not None:
            base = base.where(InterviewSession.status == status)
            count_q = count_q.where(InterviewSession.status == status)
        total = (await self.db.execute(count_q)).scalar_one()
        base = base.order_by(InterviewSession.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        items = (await self.db.execute(base)).scalars().all()
        return items, total

    async def delete(self, session: InterviewSession) -> None:
        await self.db.delete(session)
        await self.db.flush()
