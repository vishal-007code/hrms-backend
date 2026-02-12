from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class AttendanceStatus(str, enum.Enum):
    Present = "Present"
    Absent = "Absent"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        String(50),
        ForeignKey("employees.employee_id"),
        nullable=False
    )

    attendance_date = Column(Date, nullable=False)

    status = Column(
        Enum(AttendanceStatus),
        nullable=False
    )

    employee = relationship(
        "Employee",
        primaryjoin="Attendance.employee_id == Employee.employee_id",
        backref="attendance_records"
    )
