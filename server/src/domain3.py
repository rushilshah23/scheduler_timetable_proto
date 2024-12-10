from dataclasses import dataclass, field
from typing import List, Optional
from datetime import time
from enum import Enum
from abc import  ABC, abstractmethod
from src.genetic_algorithm import Gene, Chromosome


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
    id: str
    day_name: str


    def to_dict(self):
        return {
            "id": self.id,
            "day_name": self.day_name
        }

@dataclass
class WorkingDay:
    id: str
    day_id: str
    start_time: time  # You can use datetime if you need more control
    end_time: time
    slot_duration: int
    day: Day
    division_id:str
    division:'Division'
    

    def to_dict(self):
        return {
            "id": self.id,
            "day_id": self.day_id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "slot_duration": self.slot_duration,
            "day": self.day.to_dict(),
            "division_id":self.division_id,
            "division":self.division.to_dict()
        }

@dataclass
class Slot(Gene):
    id: str
    start_time: time
    end_time: time
    working_day_id: str

    working_day: WorkingDay
    daily_slot_number:int
    weekly_slot_number:int
    slot_alloted_to: "SlotAllotable" = None



    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "working_day_id": self.working_day_id,
            "working_day": self.working_day.to_dict() if self.working_day else None,
            "slot_alloted_to": self.slot_alloted_to.to_dict() if self.slot_alloted_to else None,
            "daily_slot_number":self.daily_slot_number,
            "weekly_slot_number":self.weekly_slot_number
        }

@dataclass
class SlotAllotable:
    id: str
    division_id:str
    name: str 
    division: 'Division'
    continuos_slot:int
    # fixed_slot:bool
    # start_time: Optional[time]
    # end_time: Optional[time]
    # working_day_id: Optional[str]
    # working_day: Optional['WorkingDay']


    def to_dict(self):
        return {
            "id": self.id,
            "division_id": self.division_id,
            "name": self.name,
            "division": self.division.to_dict() if self.division else None,
            "fixed_slot": self.fixed_slot,
            "continuos_slot":self.continuos_slot
            # "start_time": self.start_time.strftime("%H:%M:%S") if self.start_time else None,
            # "end_time": self.end_time.strftime("%H:%M:%S") if self.end_time else None,
            # "working_day_id": self.working_day_id,
            # "working_day": self.working_day.to_dict() if self.working_day else None
        }
        

# @dataclass
# class Lecture(SlotAllotable):
#     faculty_id: str
#     subject_id: str 
#     fixed_slot: bool = False
#     continuos_slot = 1
#     # start_time: Optional[time]
#     # end_time: Optional[time] 
#     # working_day_id: Optional[str] 
#     # working_day: Optional['WorkingDay'] 


#     def to_dict(self):
#         base_dict = super().to_dict()
#         base_dict.update({
#             "faculty_id": self.faculty_id,
#             "subject_id": self.subject_id
#         })
#         return base_dict
@dataclass
class Break(SlotAllotable):
    # Inherits and directly uses the base `to_dict` method.
    start_time: time
    end_time: time
    working_day_id: str
    working_day: 'WorkingDay'
    fixed_slot: bool = field(default=True, init=False)
    continuos_slot  = 1
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'start_time':self.start_time.strftime("%H:%M:%S"),
            'end_time':self.end_time.strftime("%H:%M:%S"),
            "working_day_id":self.working_day_id,
            "working_day":self.working_day.to_dict() if self.working_day else None

        })
        return base_dict



@dataclass
class Faculty:
    id: str
    faculty_name: str
    # subjects: List["Subject"] = None

    # def __post_init__(self):
    #     if self.subjects is None:
    #         self.subjects = []
    def to_dict(self):
        return {
            "id": self.id,
            "faculty_name": self.faculty_name
        }
    


@dataclass
class Subject:
    id: str
    subject_name: str
    # divisions: List["Division"] = None
    # faculties: List["Faculty"] = None

    # def __post_init__(self):
    #     if self.divisions is None:
    #         self.divisions = []
    #     if self.faculties is None:
    #         self.faculties = []
    def to_dict(self):
        return {
            "id": self.id,
            "subject_name": self.subject_name
        }

@dataclass
class Division:
    id: str
    division_name: str
    standard_id: str
    standard: "Standard"
    def to_dict(self):
        return {
            "id": self.id,
            "division_name": self.division_name,
            "standard_id": self.standard_id,
            "standard": self.standard.to_dict() if self.standard else None
        }



@dataclass
class Standard:
    id: str
    standard_name: str
    department_id: str
    department: "Department"
    def to_dict(self):
        return {
            "id": self.id,
            "standard_name": self.standard_name,
            "department_id": self.department_id,
            "department": self.department.to_dict() if self.department else None
        }


@dataclass
class Department:
    id: str
    department_name: str
    university_id: str
    university: "University"

    def to_dict(self):
        return {
            "id": self.id,
            "department_name": self.department_name,
            "university_id": self.university_id,
            "university": self.university.to_dict() if self.university else None
        }
@dataclass
class University:
    id: str
    university_name: str

    def to_dict(self):
        return {
            "id": self.id,
            "university_name": self.university_name
        }


@dataclass
class FacultySubjectDivision(SlotAllotable):
    faculty_id: str
    subject_id: str
    division_id: str

    faculty:Faculty
    subject:Subject
    division:Division

    fixed_slot: bool = False
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    working_day_id: Optional[str] = None
    working_day: Optional['WorkingDay'] = None
    continuos_slot=1
    def to_dict(self):
        return {
            "faculty_id": self.faculty_id,
            "subject_id": self.subject_id,
            "division_id": self.division_id,
            "faculty": self.faculty.to_dict() if self.faculty else None,
            "subject": self.subject.to_dict() if self.subject else None,
            "division": self.division.to_dict() if self.division else None
        }

# ---------------------------------
@dataclass
class Timetable:
    division: Division
    slots: List[Slot]
    constraints:List['Constraint'] = None
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints:List['Constraint'] = []


    def to_dict(self):
        return {
            "division": self.division.to_dict() if self.division else None,
            "slots": [slot.to_dict() for slot in self.slots] if self.slots else []
        }
    
@dataclass
class UniversityTimetables(Chromosome):
    genes:List[Slot] = None

    def __post_init__(self):

        if self.genes is None:
            self.genes:List['Slot'] = []
 

            
    # def apply_constraints(self):
    #     for constraint in self.constraints:
    #         result = constraint.apply()
    #         print(f"Constraint {constraint.__class__.__name__} applied: {result}")

    def to_dict(self):
        return {
            "timetables": [timetable.to_dict() for timetable in self.genes] if self.genes else []
            # "constraints": [constraint.to_dict() for constraint in self.constraints] if self.constraints else []
        }


@dataclass
class Constraint(ABC):
    # timetables: UniversityTimetables
    failed_weightage: float


    @abstractmethod
    def apply(self) -> bool:
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "weightage": self.weightage
        }