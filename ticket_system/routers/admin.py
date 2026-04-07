from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..core.dependencies import require_admin
from ..models import User, TicketStatus, TicketPriority, TicketCategory
from ..schemas import PaginatedTickets, AdminStats
from ..services import ticket_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/tickets", response_model=PaginatedTickets)
def admin_list_all_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    category: Optional[TicketCategory] = None,
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Admin: list ALL tickets across all users."""
    return ticket_service.list_tickets(
        db, current_user, status, priority, category,
        search, sort_by, sort_order, page, page_size,
        admin_view=True
    )


@router.get("/stats", response_model=AdminStats)
def admin_stats(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    """Admin: get ticket and user statistics."""
    return ticket_service.get_admin_stats(db)
