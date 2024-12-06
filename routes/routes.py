from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Child, Staff, Attendance
from schemas import ChildCreate, ChildResponse, StaffBase, AttendanceBase, AttendanceResponse
from database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- CRUD Operations for Children --------------------

# Create a child
@router.post("/children/", response_model=ChildResponse)
def create_child(child: ChildCreate, db: Session = Depends(get_db)):
    db_child = Child(**child.dict())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

# Fetch all children
@router.get('/children/', response_model=List[ChildResponse])
def read_children(db: Session = Depends(get_db)):
    return db.query(Child).all()

# Fetch a child by ID, including attendance records
@router.get("/children/{child_id}", response_model=ChildResponse)
def read_child(child_id: int, db: Session = Depends(get_db)):
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child

# Update a child
@router.put("/children/{child_id}", response_model=ChildResponse)
def update_child(child_id: int, child_data: ChildCreate, db: Session = Depends(get_db)):
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    for key, value in child_data.dict().items():
        setattr(child, key, value)
    db.commit()
    db.refresh(child)
    return child

# Delete a child
@router.delete("/children/{child_id}")
def delete_child(child_id: int, db: Session = Depends(get_db)):
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    db.delete(child)
    db.commit()
    return {"message": "Child deleted successfully"}

# -------------------- CRUD Operations for Staff --------------------

# Create a staff member
@router.post("/staff/", response_model=StaffBase)
def create_staff(staff: StaffBase, db: Session = Depends(get_db)):
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

# Fetch all staff
@router.get("/staff/", response_model=List[StaffBase])
def read_staff(db: Session = Depends(get_db)):
    return db.query(Staff).all()

# Fetch a specific staff member by ID
@router.get("/staff/{staff_id}", response_model=StaffBase)
def read_staff_member(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

# Update a staff member
@router.put("/staff/{staff_id}", response_model=StaffBase)
def update_staff(staff_id: int, staff_data: StaffBase, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    for key, value in staff_data.dict().items():
        setattr(staff, key, value)
    db.commit()
    db.refresh(staff)
    return staff

# Delete a staff member
@router.delete("/staff/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    db.delete(staff)
    db.commit()
    return {"message": "Staff member deleted successfully"}

# -------------------- CRUD Operations for Attendance --------------------

# Create an attendance record
@router.post("/attendance/", response_model=AttendanceResponse)
def create_attendance(attendance: AttendanceBase, db: Session = Depends(get_db)):
    # Ensure child and staff exist
    db_child = db.query(Child).filter(Child.id == attendance.child_id).first()
    db_staff = db.query(Staff).filter(Staff.id == attendance.staff_id).first()
    if not db_child or not db_staff:
        raise HTTPException(status_code=400, detail="Child or Staff not found")

    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

# Get all attendance records with linked data
@router.get("/attendance/", response_model=List[AttendanceResponse])
def read_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()

# Get a specific attendance record by ID
@router.get("/attendance/{attendance_id}", response_model=AttendanceResponse)
def read_attendance_record(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance
