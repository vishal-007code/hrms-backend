from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    employee_id: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=255)
    email: EmailStr
    department: str = Field(..., max_length=255)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeListResponse(BaseModel):
    total: int
    items: list[EmployeeRead]

