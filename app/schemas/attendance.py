from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"


class AttendanceBase(BaseModel):
    employee_id: str = Field(..., description="Public employee identifier (employee_id field)")
    attendance_date: date = Field(..., description="Date of attendance")
    status: AttendanceStatus


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(BaseModel):
    id: int
    employee_id: str
    full_name: str
    attendance_date: date
    status: AttendanceStatus

    model_config = ConfigDict(from_attributes=True)


class AttendanceListResponse(BaseModel):
    total: int
    items: list[AttendanceRead]


class AttendanceUpdate(BaseModel):
    attendance_date: Optional[date] = None
    status: Optional[AttendanceStatus] = None

class AttendanceResponse(AttendanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
