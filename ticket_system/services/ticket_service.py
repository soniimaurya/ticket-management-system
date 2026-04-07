from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from typing import Optional
from ..models import Ticket, User, TicketStatus, TicketPriority, TicketCategory, UserRole
from ..schemas import TicketCreate, TicketUpdate, TicketOut, PaginatedTickets, AdminStats


def _enrich(ticket: Ticket) -> TicketOut:
    """Add username fields to ticket output."""
    out = TicketOut.model_validate(ticket)
    out.creator_username = ticket.creator.username if ticket.creator else None
    out.assignee_username = ticket.assignee.username if ticket.assignee else None
    return out


def create_ticket(data: TicketCreate, user: User, db: Session) -> TicketOut:
    if data.assigned_to:
        assignee = db.query(User).filter(User.id == data.assigned_to).first()
        if not assignee:
            raise HTTPException(status_code=404, detail="Assignee user not found")

    ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        category=data.category,
        created_by=user.id,
        assigned_to=data.assigned_to
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return _enrich(ticket)


def list_tickets(
    db: Session,
    user: User,
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    category: Optional[TicketCategory] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 10,
    admin_view: bool = False
) -> PaginatedTickets:
    query = db.query(Ticket)

    # Users can only see their own tickets unless admin
    if not admin_view or user.role != UserRole.admin:
        query = query.filter(Ticket.created_by == user.id)

    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if category:
        query = query.filter(Ticket.category == category)
    if search:
        query = query.filter(
            Ticket.title.ilike(f"%{search}%") | Ticket.description.ilike(f"%{search}%")
        )

    # Sorting
    sort_col = getattr(Ticket, sort_by, Ticket.created_at)
    query = query.order_by(sort_col.desc() if sort_order == "desc" else sort_col.asc())

    total = query.count()
    tickets = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedTickets(
        total=total,
        page=page,
        page_size=page_size,
        tickets=[_enrich(t) for t in tickets]
    )


def get_ticket(ticket_id: int, user: User, db: Session) -> TicketOut:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if user.role != UserRole.admin and ticket.created_by != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return _enrich(ticket)


def update_ticket(ticket_id: int, data: TicketUpdate, user: User, db: Session) -> TicketOut:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if user.role != UserRole.admin and ticket.created_by != user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return _enrich(ticket)


def update_ticket_status(ticket_id: int, new_status: TicketStatus, user: User, db: Session) -> TicketOut:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if user.role != UserRole.admin and ticket.created_by != user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    ticket.status = new_status
    db.commit()
    db.refresh(ticket)
    return _enrich(ticket)


def delete_ticket(ticket_id: int, user: User, db: Session) -> dict:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if user.role != UserRole.admin and ticket.created_by != user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(ticket)
    db.commit()
    return {"message": f"Ticket {ticket_id} deleted"}


def get_admin_stats(db: Session) -> AdminStats:
    total = db.query(Ticket).count()
    by_status = {s.value: db.query(Ticket).filter(Ticket.status == s).count() for s in TicketStatus}
    by_priority = {p.value: db.query(Ticket).filter(Ticket.priority == p).count() for p in TicketPriority}
    by_category = {c.value: db.query(Ticket).filter(Ticket.category == c).count() for c in TicketCategory}
    total_users = db.query(User).count()

    return AdminStats(
        total_tickets=total,
        open_tickets=by_status.get("open", 0),
        in_progress_tickets=by_status.get("in_progress", 0),
        resolved_tickets=by_status.get("resolved", 0),
        closed_tickets=by_status.get("closed", 0),
        total_users=total_users,
        tickets_by_priority=by_priority,
        tickets_by_category=by_category
    )
