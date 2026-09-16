import uuid

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import SessionCreate, SessionListItem, SessionListResponse, SessionResponse
from app.services.sessions import SessionService

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _request_id(request: Request) -> str:
    return request.headers.get("X-Request-ID") or str(uuid.uuid4())


def _error(status_code: int, code: str, message: str, request_id: str, details=None) -> JSONResponse:  # type: ignore[no-untyped-def]
    body: dict = {"error": {"code": code, "message": message, "request_id": request_id}}
    if details is not None:
        body["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=body)


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(payload: SessionCreate, db: AsyncSession = Depends(get_db)):  # type: ignore[no-untyped-def]
    svc = SessionService(db)
    session = await svc.create(payload)
    return session  # type: ignore[return-value]


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),  # type: ignore[no-untyped-def]
) -> SessionListResponse:
    if status is not None and status not in SessionService.VALID_STATUSES:
        from fastapi import HTTPException

        raise HTTPException(status_code=422, detail=f"Invalid status filter: {status}")
    svc = SessionService(db)
    items, total = await svc.list(page=page, page_size=page_size, status=status)
    return SessionListResponse(
        items=[
            SessionListItem(
                id=s.id,
                target_role=s.target_role,
                status=s.status,
                language=s.language,
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
            for s in items
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{session_id}")
async def get_session(session_id: uuid.UUID, request: Request, db: AsyncSession = Depends(get_db)):  # type: ignore[no-untyped-def]
    svc = SessionService(db)
    session = await svc.get(session_id)
    if session is None:
        return _error(404, "not_found", "Session not found.", _request_id(request))
    return JSONResponse(
        status_code=200,
        content={
            "id": str(session.id),
            "target_role": session.target_role,
            "job_description": session.job_description,
            "language": session.language,
            "status": session.status,
            "plan_summary": session.plan_summary,
            "current_question_index": session.current_question_index,
            "created_at": session.created_at.isoformat().replace("+00:00", "Z"),
            "updated_at": session.updated_at.isoformat().replace("+00:00", "Z"),
        },
    )


@router.delete("/{session_id}")
async def delete_session(session_id: uuid.UUID, request: Request, db: AsyncSession = Depends(get_db)):  # type: ignore[no-untyped-def]
    svc = SessionService(db)
    session = await svc.get(session_id)
    if session is None:
        return _error(404, "not_found", "Session not found.", _request_id(request))
    if session.status != "draft":
        return _error(409, "conflict", "Only draft sessions can be deleted.", _request_id(request))
    await svc.delete_draft(session)
    return Response(status_code=204)
