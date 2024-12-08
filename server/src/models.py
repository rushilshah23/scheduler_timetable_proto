from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship
# from sqlalchemy import event
from db import Base, engine



class University(Base):
    __tablename__ = 'universities'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    university_name=Column(String, nullable=False)

    departments = relationship("Department", back_populates="university")

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    department_name = Column(String, nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'))

    university = relationship("University", back_populates="departments")
    standards = relationship("Standard", back_populates="department")

class Standard(Base):
    __tablename__ = 'standards'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    standard_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship("Department", back_populates="standards")
    divisions = relationship("Division", back_populates="standard")

class Division(Base):
    __tablename__ = 'divisions'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    division_name = Column(String, nullable=False)
    standard_id = Column(Integer, ForeignKey('standards.id'))

    standard = relationship("Standard", back_populates="divisions")
    subjects = relationship("Subject", secondary="divisions_subjects",back_populates="divisions")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    subject_name = Column(String, nullable=False)
    # division_id = Column(Integer, ForeignKey('divisions.id'))

    divisions = relationship("Division", secondary="divisions_subjects",back_populates="subjects")
    faculties = relationship("Faculty", secondary="faculties_subjects", back_populates="subjects")



class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    faculty_name = Column(String, nullable=False)

    subjects = relationship("Subject", secondary="faculty_subjects", back_populates="faculties")

class DivisionSubjects(Base):
    __tablename__ = 'divisions_subjects'
    division_id = Column(Integer, ForeignKey('divisions.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)

class FacultySubject(Base):
    __tablename__ = 'faculties_subjects'
    faculty_id = Column(Integer, ForeignKey('faculties.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)




class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    day_name = Column(String, nullable=False)



class WorkingDay(Base):
    __tablename__ = "working_days"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id"))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    slot_duration = Column(Integer, nullable=False)

    day = relationship("Day")


class SlotAllotable(Base):
    __tablename__ = "slot_allotables"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=True)
    # faculty_id = Column(Integer, ForeignKey('faculties_subjects.faculty_id'), nullable=True)
    # subject_id = Column(Integer, ForeignKey('faculties_subjects.subject_id'), nullable=True)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=True)
    non_teaching = Column(Boolean, default=False, nullable=False)
    slot_id = Column(Integer, ForeignKey('slots.id'), nullable=True)

    slot = relationship("Slot",back_populates="slot_alloted_to")

class Slot(Base):
    __tablename__ = 'slots'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    slot_alloted_to_id = Column(Integer, ForeignKey('slot_allotables.id'), nullable=True)

    slot_alloted_to = relationship("SlotAllotable", back_populates="slot")


# Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)


# slot = Slot()

# # This event listener will automatically check when an object is being inserted or updated
# @event.listens_for(SlotAllotable, 'before_insert')
# @event.listens_for(SlotAllotable, 'before_update')
# def check_special_slots(mapper, connection, target):
#     if target.non_teaching == True:
#         target.faculty_id = None
#         target.subject_id = None
