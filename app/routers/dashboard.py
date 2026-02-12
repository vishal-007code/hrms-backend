from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceStatus
from pydantic import BaseModel

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class DashboardSummary(BaseModel):
    total_employees: int
    present_today: int
    absent_today: int


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    """Return key dashboard metrics for today."""
    today = date.today()

    total_employees = db.query(func.count(Employee.id)).scalar() or 0

    present_today = (
        db.query(func.count(Attendance.id))
        .filter(
            Attendance.attendance_date == today,
            Attendance.status == AttendanceStatus.PRESENT.value,
        )
        .scalar()
        or 0
    )

    absent_today = (
        db.query(func.count(Attendance.id))
        .filter(
            Attendance.attendance_date == today,
            Attendance.status == AttendanceStatus.ABSENT.value,
        )
        .scalar()
        or 0
    )

    return DashboardSummary(
        total_employees=total_employees,
        present_today=present_today,
        absent_today=absent_today,
    )

