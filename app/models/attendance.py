from datetime import date

from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint(
            "employee_id", "attendance_date", name="uq_attendance_employee_date"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    attendance_date = Column(Date, nullable=False, index=True, default=date.today)
    status = Column(
        Enum("Present", "Absent", name="attendance_status"),
        nullable=False,
    )

    employee = relationship("Employee", backref="attendance_records")

