from dataclasses import dataclass
from typing import List, Optional
from src.domain2 import *

class DomainUtils:
    _instance = None  # This holds the singleton instance

    def __new__(cls, data_source=None):
        if cls._instance is None:
            # Create the singleton instance only once
            cls._instance = super(DomainUtils, cls).__new__(cls)
            cls._instance.data_source = data_source
        return cls._instance
    
    def get_university_by_id(self, id: int):
        """Get a university by ID."""
        for university in self.data_source["universities"]:
            if university.id == id:
                return university
        return None

    def get_department_by_id(self, id: int):
        """Get a department by ID."""
        for department in self.data_source["departments"]:
            if department.id == id:
                return department
        return None

    def get_standard_by_id(self, id: int):
        """Get a standard by ID."""
        for standard in self.data_source["standards"]:
            if standard.id == id:
                return standard
        return None

    def get_division_by_id(self, id: int):
        """Get a division by ID."""
        for division in self.data_source["divisions"]:
            if division.id == id:
                return division
        return None

    def get_subject_by_id(self, id: int):
        """Get a subject by ID."""
        for subject in self.data_source["subjects"]:
            if subject.id == id:
                return subject
        return None

    def get_faculty_by_id(self, id: int):
        """Get a faculty by ID."""
        for faculty in self.data_source["faculties"]:
            if faculty.id == id:
                return faculty
        return None

    def get_faculty_subject_division_list(self):
        """Get the list of all faculty subject divisions."""
        return self.data_source.get("faculty_subject_division_list", [])

    def get_working_day_from_id(self, id: int):
        """Get a working day by ID."""
        for working_day in self.data_source["working_days"]:
            if working_day.id == id:
                return working_day
        return None

    def get_break_by_id(self, id: int):
        """Get a break by ID."""
        for break_item in self.data_source["breaks_list"]:
            if break_item.id == id:
                return break_item
        return None

    def get_all_universities(self) -> List:
        """Get all universities."""
        return self.data_source.get("universities", [])

    def get_all_departments(self) -> List:
        """Get all departments."""
        return self.data_source.get("departments", [])

    def get_all_standards(self) -> List:
        """Get all standards."""
        return self.data_source.get("standards", [])

    def get_all_divisions(self) -> List:
        """Get all divisions."""
        return self.data_source.get("divisions", [])

    def get_all_subjects(self) -> List:
        """Get all subjects."""
        return self.data_source.get("subjects", [])

    def get_all_faculties(self) -> List:
        """Get all faculties."""
        return self.data_source.get("faculties", [])

    def get_all_working_days(self) -> List:
        """Get all working days."""
        return self.data_source.get("working_days", [])

    def get_all_breaks(self) -> List:
        """Get all breaks."""
        return self.data_source.get("breaks_list", [])