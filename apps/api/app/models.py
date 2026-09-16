from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_role: Mapped[str] = mapped_column(String(200), nullable=False)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    plan_summary: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    current_question_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=utcnow, default=utcnow
    )

    __table_args__ = (
        CheckConstraint("language IN ('id','en')", name="ck_session_language"),
        CheckConstraint(
            "status IN ('draft','ready','in_progress','completed','abandoned')",
            name="ck_session_status",
        ),
        Index("idx_session_status", "status"),
        Index("idx_session_created_at", "created_at"),
    )


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    pages: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list, server_default="[]")
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=utcnow, default=utcnow
    )

    __table_args__ = (
        CheckConstraint("file_size_bytes > 0", name="ck_document_file_size"),
        CheckConstraint("status IN ('uploaded','processing','ready','failed')", name="ck_document_status"),
        CheckConstraint("mime_type = 'application/pdf'", name="ck_document_mime"),
    )


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    competency: Mapped[str] = mapped_column(String(100), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    expected_evidence: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    parent_question_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )

    __table_args__ = (
        CheckConstraint("difficulty IN ('easy','medium','hard')", name="ck_question_difficulty"),
        CheckConstraint("kind IN ('main','follow_up')", name="ck_question_kind"),
        CheckConstraint("order_index >= 0 AND order_index <= 4", name="ck_question_order"),
        UniqueConstraint("session_id", "order_index", name="uq_question_session_order"),
    )


class CandidateAnswer(Base):
    __tablename__ = "candidate_answers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=False
    )
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )

    __table_args__ = (
        CheckConstraint("char_length(answer_text) > 0", name="ck_answer_text_not_empty"),
        UniqueConstraint("session_id", "question_id", name="uq_answer_session_question"),
    )


class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidate_answers.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=False
    )
    relevance: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    technical_accuracy: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    clarity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    evidence_specificity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    structure: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    overall: Mapped[Decimal] = mapped_column(Numeric(3, 2), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_quote: Mapped[str] = mapped_column(Text, nullable=False)
    strengths: Mapped[Any] = mapped_column(JSONB, nullable=False)
    improvements: Mapped[Any] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[Decimal] = mapped_column(Numeric(3, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    rubric_version: Mapped[str] = mapped_column(String(20), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=utcnow, default=utcnow
    )

    __table_args__ = (
        CheckConstraint("relevance >= 0 AND relevance <= 5", name="ck_eval_relevance"),
        CheckConstraint("technical_accuracy >= 0 AND technical_accuracy <= 5", name="ck_eval_accuracy"),
        CheckConstraint("clarity >= 0 AND clarity <= 5", name="ck_eval_clarity"),
        CheckConstraint("evidence_specificity >= 0 AND evidence_specificity <= 5", name="ck_eval_evidence"),
        CheckConstraint("structure >= 0 AND structure <= 5", name="ck_eval_structure"),
        CheckConstraint("overall >= 0 AND overall <= 5", name="ck_eval_overall"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_eval_confidence"),
        CheckConstraint(
            "status IN ('evaluated','needs_review','insufficient_answer')", name="ck_eval_status"
        ),
    )


class FinalReport(Base):
    __tablename__ = "final_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    scores_per_competency: Mapped[Any] = mapped_column(JSONB, nullable=False)
    overall_score: Mapped[Decimal] = mapped_column(Numeric(3, 2), nullable=False)
    strengths: Mapped[Any] = mapped_column(JSONB, nullable=False)
    improvements: Mapped[Any] = mapped_column(JSONB, nullable=False)
    recommendations: Mapped[Any] = mapped_column(JSONB, nullable=False)
    question_evaluations: Mapped[Any] = mapped_column(JSONB, nullable=False)
    provenance: Mapped[Any] = mapped_column(JSONB, nullable=False)
    disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    idempotency_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=utcnow, default=utcnow
    )

    __table_args__ = (
        CheckConstraint("status IN ('complete','incomplete')", name="ck_report_status"),
        UniqueConstraint("session_id", "version", name="uq_report_session_version"),
    )
