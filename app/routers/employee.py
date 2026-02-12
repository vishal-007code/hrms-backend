from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import Response


from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeListResponse, EmployeeRead

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post(
    "",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)) -> Employee:
    """Create a new employee with a unique employee_id."""
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
    """Return all employees, optionally filtered by a simple search query."""
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
    return EmployeeListResponse(total=total, items=items)


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    print("DELETE FUNCTION CALLED:", employee_id)  # 👈 ADD THIS

    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    print("DELETED SUCCESSFULLY")

    return Response(status_code=204)



