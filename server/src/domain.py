from dataclasses import dataclass
from typing import List
from datetime import time
from enum import Enum
from abc import  ABC, abstractmethod

class DayEnum(Enum):
    MONDAY="MONDAY"
    TUESDAY="TUESDAY"
    WEDNESDAY="WEDNESDAY"
    THURSDAY="THURSDAY"
    FRIDAY="FRIDAY"
    SATURDAY="SATURDAY"
    SUNDAY="SUNDAY"



@dataclass
class Day:
    id: int
    day_name: str


@dataclass
class WorkingDay:
    id: int
    day_id: int
    start_time: time  # You can use datetime if you need more control
    end_time: time
    slot_duration: int
    day: Day


@dataclass
class Slot:
    id: int
    start_time: str
    end_time: str
    slot_alloted_to: "SlotAllotable" = None

    def allot_to(self, slot_allotable:"SlotAllotable"):
        self.slot_alloted_to = slot_allotable

    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "slot_alloted_to": self.slot_alloted_to.to_dict() if self.slot_alloted_to else None
        }

@dataclass
class SlotAllotable:
    id: int
    name: str = None
    continuos_slot=1


    def to_dict(self):
        """Convert the object to a dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,

        }

@dataclass
class Lecture(SlotAllotable):
    faculty_id: int = None
    subject_id: int = None

    def to_dict(self):
        """Extend the base `to_dict` method with additional fields."""
        base_dict = super().to_dict()  # Use base class method
        base_dict.update({
            "faculty_id": self.faculty_id,
            "subject_id": self.subject_id,
        })
        return base_dict

@dataclass
class Break(SlotAllotable):
    # Inherits and directly uses the base `to_dict` method.
    pass


@dataclass
class Faculty:
    id: int
    faculty_name: str
    subjects: List["Subject"] = None

    def __post_init__(self):
        if self.subjects is None:
            self.subjects = []
    
    


@dataclass
class Subject:
    id: int
    subject_name: str
    divisions: List["Division"] = None
    faculties: List["Faculty"] = None

    def __post_init__(self):
        if self.divisions is None:
            self.divisions = []
        if self.faculties is None:
            self.faculties = []


@dataclass
class Division:
    id: int
    division_name: str
    standard_id: int
    standard: "Standard"
    subjects: List[Subject] = None

    def __post_init__(self):
        if self.subjects is None:
            self.subjects = []


@dataclass
class Standard:
    id: int
    standard_name: str
    department_id: int
    department: "Department"
    divisions: List[Division] = None

    def __post_init__(self):
        if self.divisions is None:
            self.divisions = []


@dataclass
class Department:
    id: int
    department_name: str
    university_id: int
    university: "University"
    standards: List[Standard] = None

    def __post_init__(self):
        if self.standards is None:
            self.standards = []


@dataclass
class University:
    id: int
    university_name: str
    departments: List[Department] = None

    def __post_init__(self):
        if self.departments is None:
            self.departments = []


@dataclass
class FacultySubject:
    faculty_id: int
    subject_id: int

# ---------------------------------
@dataclass
class Timetable:
    division: Division
    slots: List[Slot]

@dataclass
class UniversityTimetables:
    timetables: List[Timetable]
    constraints: List['Constraint'] = None

    def __post_init__(self):
        if self.constraints is None:
            self.constraints:List['Constraint'] = []

    def apply_constraints(self):
        for constraint in self.constraints:
            result = constraint.apply()
            print(f"Constraint {constraint.__class__.__name__} applied: {result}")

@dataclass
class Constraint(ABC):
    timetables: UniversityTimetables
    weightage: float

    @abstractmethod
    def apply(self) -> bool:
        pass

@dataclass
class SameFacultyAtDifferentLectureAtSameTime(Constraint):
    weightage: float = 1.0

    def apply(self) -> bool:
        faculty_schedule = {}

        for timetable in self.timetables.timetables:
            for slot in timetable.slots:
                if slot.faculty not in faculty_schedule:
                    faculty_schedule[slot.faculty] = []
                for scheduled_slot in faculty_schedule[slot.faculty]:
                    if self.is_overlap(scheduled_slot, slot):
                        print(f"Conflict: Faculty {slot.faculty} has overlapping slots.")
                        return False
                faculty_schedule[slot.faculty].append(slot)

        return True

    @staticmethod
    def is_overlap(slot1: Slot, slot2: Slot) -> bool:
        return not (slot1.end_time <= slot2.start_time or slot1.start_time >= slot2.end_time)
