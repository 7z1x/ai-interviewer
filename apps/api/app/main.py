from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routes.sessions import router as sessions_router

app = FastAPI(title="AI Interviewer API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    import uuid

    rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    details = []
    for err in exc.errors():
        loc = err.get("loc", [])
        field = ".".join(str(x) for x in loc) if loc else "body"
        details.append({"field": field, "issue": err.get("msg", "validation error")})
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Validation failed.", "details": details, "request_id": rid}},
    )


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "ai-interviewer-api",
        "version": "0.1.0",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/")
def root() -> dict:
    return {"message": "AI Interviewer API — see /health and /docs"}


app.include_router(sessions_router)
