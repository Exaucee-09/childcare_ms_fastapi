from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Child schemas
class ChildBase(BaseModel):
    name: str
    age: int
    classroom: str

class ChildCreate(ChildBase):
    pass

class ChildResponse(ChildBase):
    id: int
    class Config:
        orm_mode = True

# Staff schemas
class StaffBase(BaseModel):
    name: str
    role: str

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    class Config:
        orm_mode = True

# Attendance schemas
class AttendanceBase(BaseModel):
    date: date
    status: Optional[str]  # Allow status to be None
    child_id: int
    staff_id: int

class AttendanceResponse(AttendanceBase):
    id: int
    child: ChildResponse
    staff: StaffResponse

    class Config:
        orm_mode = True

