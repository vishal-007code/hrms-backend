from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeListResponse, EmployeeRead

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post(
    "",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
) -> Employee:
    existing = (
        db.query(Employee)
        .filter(Employee.employee_id == payload.employee_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this employee_id already exists.",
        )

    employee = Employee(
        employee_id=payload.employee_id,
        full_name=payload.full_name,
        email=payload.email,
        department=payload.department,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


@router.get("", response_model=EmployeeListResponse)
def list_employees(
    q: Optional[str] = Query(
        None,
        description="Optional search across employee_id, full_name, email, and department.",
    ),
    db: Session = Depends(get_db),
) -> EmployeeListResponse:
    query = db.query(Employee)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Employee.employee_id.ilike(like),
                Employee.full_name.ilike(like),
                Employee.email.ilike(like),
                Employee.department.ilike(like),
            )
        )

    items = query.order_by(Employee.created_at.desc()).all()
    total = len(items)
    employee_reads = [EmployeeRead.model_validate(item) for item in items]
    return EmployeeListResponse(total=total, items=employee_reads)

@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return Response(status_code=204)
