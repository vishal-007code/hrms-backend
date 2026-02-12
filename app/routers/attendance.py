from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceListResponse,
    AttendanceRead,
    AttendanceStatus,
    AttendanceUpdate,
)

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("", response_model=AttendanceRead)
def upsert_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db)
):
    # Find employee by public employee_id
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == payload.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    # Check if attendance exists
    record = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee.employee_id,  # FIXED
            Attendance.attendance_date == payload.attendance_date,
        )
        .first()
    )

    if record:
        record.status = payload.status.value
    else:
        record = Attendance(
            employee_id=employee.employee_id,  # FIXED
            attendance_date=payload.attendance_date,
            status=payload.status.value,
        )
        db.add(record)

    db.commit()
    db.refresh(record)

    return AttendanceRead(
        id=record.id,
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        attendance_date=record.attendance_date,
        status=AttendanceStatus(record.status),
    )


@router.get("", response_model=AttendanceListResponse)
def list_attendance(
    employee_id: Optional[str] = Query(None),
    date_filter: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Attendance)
        .options(joinedload(Attendance.employee))
        .join(Employee, Attendance.employee_id == Employee.employee_id)  # FIXED JOIN
    )

    if employee_id:
        query = query.filter(Employee.employee_id == employee_id)

    if date_filter:
        query = query.filter(Attendance.attendance_date == date_filter)

    records = query.order_by(Attendance.attendance_date.desc()).all()

    items = [
        AttendanceRead(
            id=r.id,
            employee_id=r.employee.employee_id,
            full_name=r.employee.full_name,
            attendance_date=r.attendance_date,
            status=AttendanceStatus(r.status),
        )
        for r in records
    ]

    return AttendanceListResponse(total=len(items), items=items)


@router.put("/{attendance_id}", response_model=AttendanceRead)
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Attendance)
        .options(joinedload(Attendance.employee))
        .filter(Attendance.id == attendance_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )

    if payload.attendance_date is not None:
        record.attendance_date = payload.attendance_date

    if payload.status is not None:
        record.status = payload.status.value

    db.commit()
    db.refresh(record)

    return AttendanceRead(
        id=record.id,
        employee_id=record.employee.employee_id,
        full_name=record.employee.full_name,
        attendance_date=record.attendance_date,
        status=AttendanceStatus(record.status),
    )
