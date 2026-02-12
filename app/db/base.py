from app.db.session import Base

# Import all models here so Alembic or metadata can detect them
from app.models.employee import Employee
from app.models.attendance import Attendance
