from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    classroom = Column(String, nullable=False)
    attendance_records = relationship(
        "Attendance",
        back_populates="child",  # Reference the back_populate in Attendance
        foreign_keys="Attendance.child_id"  # Explicitly link the foreign key here
    )


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # Relationship to Attendance
    attendance_records = relationship("Attendance", back_populates="staff")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("children.id"))  # Foreign key from Child
    status= Column(String)
    date = Column(Date, nullable=False)
    
    # Relationships
    child = relationship(
        "Child",
        back_populates="attendance_records",  # Reference the back_populate in Child
        foreign_keys=[child_id]  # Explicitly link the foreign key to the child_id
    )

    staff_id = Column(Integer, ForeignKey("staff.id"))  # Foreign key from Staff
    staff = relationship(
        "Staff",
        back_populates="attendance_records",  # Reference the back_populate in Staff
    )
