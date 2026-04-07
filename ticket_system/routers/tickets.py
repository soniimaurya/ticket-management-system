from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..core.dependencies import get_current_user
from ..models import User, Ticket, TicketStatus, TicketPriority, TicketCategory, UserRole
from ..schemas import TicketCreate, TicketUpdate, TicketStatusUpdate, TicketOut, PaginatedTickets
from ..services import ticket_service
from ..models import Ticket, User, TicketStatus, TicketPriority, TicketCategory, UserRole
from ..models import Ticket
router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketOut, status_code=201)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new ticket."""
    return ticket_service.create_ticket(data, current_user, db)


@router.get("/", response_model=PaginatedTickets)
def list_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    category: Optional[TicketCategory] = None,
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="asc or desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List tickets with filters, search, sorting, and pagination."""
    return ticket_service.list_tickets(
        db, current_user, status, priority, category,
        search, sort_by, sort_order, page, page_size
    )


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single ticket by ID."""
    return ticket_service.get_ticket(ticket_id, current_user, db)


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update ticket fields."""
    return ticket_service.update_ticket(ticket_id, data, current_user, db)


@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_status(
    ticket_id: int,
    data: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update only the status of a ticket."""
    return ticket_service.update_ticket_status(ticket_id, data.status, current_user, db)


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a ticket."""
    return ticket_service.delete_ticket(ticket_id, current_user, db)
