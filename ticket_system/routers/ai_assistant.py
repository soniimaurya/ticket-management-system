import json
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.dependencies import get_current_user
from ..core.config import settings
from ..models import User, Ticket, UserRole
from ..schemas import AIQuery, AIResponse

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


def _get_tickets_context(user: User, db: Session) -> str:
    """Build a text context of tickets visible to the user."""
    if user.role == UserRole.admin:
        tickets = db.query(Ticket).all()
    else:
        tickets = db.query(Ticket).filter(Ticket.created_by == user.id).all()

    if not tickets:
        return "No tickets found."

    lines = []
    for t in tickets:
        lines.append(
            f"Ticket #{t.id}: '{t.title}' | Status: {t.status} | Priority: {t.priority} "
            f"| Category: {t.category} | Created by user_id={t.created_by} "
            f"| Assigned to: {t.assigned_to or 'unassigned'} | Created: {t.created_at.date()}"
        )
    return "\n".join(lines)


@router.post("/ask", response_model=AIResponse)
async def ask_ai(
    query: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ask a natural language question about tickets.
    Examples:
    - 'What is the status of ticket 5?'
    - 'Show all high priority open tickets'
    - 'How many tickets are unresolved?'
    """
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI assistant is not configured. Set ANTHROPIC_API_KEY in .env"
        )

    tickets_context = _get_tickets_context(current_user, db)
    role_info = f"The user is a {'admin (can see all tickets)' if current_user.role == UserRole.admin else 'regular user (can only see their own tickets)'}."

    system_prompt = f"""You are a helpful ticket management assistant. 
{role_info}
Answer questions about the tickets below clearly and concisely.
If asked about a specific ticket ID, find it in the list. 
If asked for a summary, summarise the key details.

TICKET DATA:
{tickets_context}
"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-opus-4-5",
                "max_tokens": 512,
                "system": system_prompt,
                "messages": [{"role": "user", "content": query.question}]
            },
            timeout=30.0
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="AI service error")

    data = response.json()
    answer = data["content"][0]["text"]
    return AIResponse(answer=answer)
