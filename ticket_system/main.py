import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ticket_system.database import engine, Base
#from .database import engine, Base
from .routers import auth, tickets, admin, ai_assistant
# Create all DB tables
Base.metadata.create_all(bind=engine)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ticket Management System",
    description="""
A full-featured ticket management API with:
- 🔐 JWT authentication with role-based access (Admin / User)
- 🎫 Full ticket CRUD with filters, search, sorting, and pagination
- 📊 Admin stats dashboard
- 🤖 AI assistant for natural language ticket queries (Bonus)
    """,
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Register routers
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(admin.router)
app.include_router(ai_assistant.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Ticket Management System API", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
