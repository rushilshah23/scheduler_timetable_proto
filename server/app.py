# import sqlite3
# from abc import ABC, abstractmethod

# class Constraint: 
#     @abstractmethod
#     def perform_check():
#         pass

# class LecturesWithinUniversityTime(Constraint):
#     def perform_check(self, university, lecture):
#         pass

# class NoLectureDuringBreaks(Constraint):
#     def perform_check(university,lecture ):
#         pass

# # MORE CONSTARINTS  
# # -------------------------------------------
# class Break:
#     def __init__(self,id, university_working_day, start_from , end_at):
#         self.id = id
#         self.start_from = start_from
#         self.end_at = end_at
#         self.university_working_day = university_working_day

# class UniversityWorkingDay:
#     def __init__(self, day, start_from , end_at, breaks, university):
#         self.day = day
#         self.start_from = start_from
#         self.end_at = end_at
#         self.breaks = breaks
#         self.university = university

# class Teaches:
#     def __init__(self, subject, division):
#         self.subject=subject
#         self.division=division

# class Faculty:
#     def __init__(self, id, name, teaches:list[Teaches] ):
#         self.id = id
#         self.name=name
#         self.teaches= teaches
    
# class Department:
#     def __init__(self,id,name,university):
#         self.id = id
#         self.name=name
#         self.university=university

# class Standard:
#     def __init__(self,id, department):
#         self.id = id
#         self.department = department

# class Lecture:
#     def __init__(self, id, division,start_from,end_at, subject, faculty):
#         self.id = id
#         self.division=division
#         self.start_from=start_from
#         self.end_at=end_at,
#         self.subject=subject
#         self.faculty=faculty


# class Division:
#     def __init__(self, id, department, standard):
#         self.id = id
#         self.department=department
#         self.standard=standard

# class Subject:
#     def __init__(self,id,name, department, standard):
#         self.id=id
#         self.name=name
#         self.department=department
#         self.standard=standard

# class University:
#     def __init__(self, id,faculties, departments, standards, subjects, divisions,university_name, working_days,slot_duration=30*60):
#         self.id = id
#         self.faculties = faculties
#         self.departments=  departments
#         self.standards = standards
#         self.subjects = subjects
#         self.divisions = divisions
#         self.university_name = university_name
#         self.slot_duration = slot_duration
#         self.working_days = working_days
        


import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta




class UniversityWorkingDay:
    def __init__(self, day, start_from, end_at, breaks, university):
        self.day = day
        self.start_from = start_from
        self.end_at = end_at
        self.breaks = breaks
        self.university = university

class Break:
    def __init__(self, id, university_working_day:, start_from, end_at):
        self.id = id
        self.start_from = start_from
        self.end_at = end_at
        self.university_working_day = university_working_day

class Teaches:
    def __init__(self, subject, division):
        self.subject = subject
        self.division = division


class Faculty:
    def __init__(self, id, name, teaches):
        self.id = id
        self.name = name
        self.teaches = teaches


class Department:
    def __init__(self, id, name, university):
        self.id = id
        self.name = name
        self.university = university


class Standard:
    def __init__(self, id, department):
        self.id = id
        self.department = department


class Lecture:
    def __init__(self, id, division, start_from, end_at, subject, faculty):
        self.id = id
        self.division = division
        self.start_from = start_from
        self.end_at = end_at
        self.subject = subject
        self.faculty = faculty


class Division:
    def __init__(self, id, department, standard):
        self.id = id
        self.department = department
        self.standard = standard


class Subject:
    def __init__(self, id, name, department, standard):
        self.id = id
        self.name = name
        self.department = department
        self.standard = standard


class University:
    def __init__(self, id, faculties, departments, standards, subjects, divisions, university_name, working_days, slot_duration=30*60):
        self.id = id
        self.faculties = faculties
        self.departments = departments
        self.standards = standards
        self.subjects = subjects
        self.divisions = divisions
        self.university_name = university_name
        self.slot_duration = slot_duration
        self.working_days = working_days
        self.lectures = []  # To store all scheduled lectures

# ---------------------------------------CONSTRAINTS--------------------
class Constraint(ABC):
    @abstractmethod
    def perform_check(self, university, lecture):
        pass


class NoClashingLecturesInDivision(Constraint):
    def perform_check(self, university:University, lecture:Lecture):
        # Ensure no two lectures clash in the same division at the same time
        for existing_lecture in university.lectures:
            if existing_lecture.division == lecture.division:
                if existing_lecture.start_from == lecture.start_from:
                    return False  # Clash detected
        return True


class NoClashingFacultyAssignments(Constraint):
    def perform_check(self, university, lecture):
        # Ensure the same faculty doesn't have multiple lectures at the same time
        for existing_lecture in university.lectures:
            if existing_lecture.faculty == lecture.faculty:
                if existing_lecture.start_from == lecture.start_from:
                    return False  # Clash detected
        return True


class EvenLectureDistribution(Constraint):
    def perform_check(self, university, lecture):
        # Check if lectures are evenly distributed for the faculty
        faculty_lectures = [l for l in university.lectures if l.faculty == lecture.faculty]
        # Ideally, we want to ensure that a faculty isn't overburdened with lectures back-to-back
        if len(faculty_lectures) > 3:  # Example threshold, adjust as needed
            return False
        return True


class LecturesWithinUniversityTime(Constraint):
    def perform_check(self, university, lecture):
        # Get the corresponding day of the week from working_days
        weekday = lecture.start_from.weekday()

        # Option 1: Direct indexing if working_days are ordered from Monday to Sunday
        day_schedule = university.working_days[weekday]

        # Option 2: If working_days are unordered, search by day name
        # day_schedule = None
        # for wd in university.working_days:
        #     if wd.day == lecture.start_from.strftime('%A'):
        #         day_schedule = wd
        #         break

        if not day_schedule:
            raise ValueError("No working day found for the given lecture start time")
        # Continue with the rest of your check


class NoLectureDuringBreaks(Constraint):
    def perform_check(self, university, lecture):
        # Check if the lecture overlaps with any scheduled breaks
        day_schedule = university.working_days.get(lecture.start_from.weekday())
        for break_time in day_schedule.breaks:
            if break_time.start_from <= lecture.start_from.time() < break_time.end_at:
                return False
        return True






from datetime import datetime, timedelta

class TimetableGenerator:
    def __init__(self, university):
        self.university = university
        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def generate_timetable(self):
        timetable = []
        for faculty in self.university.faculties:
            for teaching in faculty.teaches:
                lecture = self.schedule_lecture(faculty, teaching.subject, teaching.division)
                if lecture:
                    timetable.append(lecture)
        return timetable

    def schedule_lecture(self, faculty, subject, division):
        start_time = self.select_start_time()
        # Convert start_time to datetime, then add duration
        start_datetime = datetime.combine(datetime.today(), start_time)  # combine with today's date
        end_datetime = start_datetime + timedelta(seconds=self.university.slot_duration)
        
        # Convert back to time if needed
        end_time = end_datetime.time()

        # Create the lecture
        lecture = Lecture(id=random.randint(1, 1000), division=division, start_from=start_time, end_at=end_time, subject=subject, faculty=faculty)
        
        # Check constraints
        for constraint in self.constraints:
            if not constraint.perform_check(self.university, lecture):
                return None  # This time slot doesn't work, try another
        
        # Schedule the lecture
        self.university.lectures.append(lecture)
        return lecture

    def select_start_time(self):
        # Assuming working_days is a list and we are selecting the first working day
        working_day = self.university.working_days[0]  # Accessing the first element directly

        # Continue with the logic to select the start time
        possible_start_times = [
            datetime.strptime("08:00", "%H:%M").time(),
            datetime.strptime("09:00", "%H:%M").time(),
            datetime.strptime("10:00", "%H:%M").time(),
            # Add more times as needed
        ]
        return random.choice(possible_start_times)

# Test Case Example for University with Multiple Departments

# Create departments
it_department = Department(1, "IT", None)
cs_department = Department(2, "CS", None)
extc_department = Department(3, "EXTC", None)
etx_department = Department(4, "ETX", None)
mechanical_department = Department(5, "Mechanical", None)

# Create faculties (example)
faculty_1 = Faculty(1, "Dr. Smith", [Teaches("Data Structures", "CS-1"), Teaches("Algorithms", "IT-1")])
faculty_2 = Faculty(2, "Dr. John", [Teaches("Physics", "ETX-1"), Teaches("Mechanical Design", "MECH-1")])

# Create subjects
data_structures = Subject(1, "Data Structures", it_department, None)
algorithms = Subject(2, "Algorithms", cs_department, None)
physics = Subject(3, "Physics", etx_department, None)
mechanical_design = Subject(4, "Mechanical Design", mechanical_department, None)

# Create divisions (example)
cs_1 = Division(1, cs_department, None)
it_1 = Division(2, it_department, None)
etx_1 = Division(3, etx_department, None)
mech_1 = Division(4, mechanical_department, None)

# University Setup
working_days = [UniversityWorkingDay(day="Monday", start_from=datetime.strptime("08:00", "%H:%M").time(), end_at=datetime.strptime("17:00", "%H:%M").time(), breaks=[], university=None)]
university = University(id=1, faculties=[faculty_1, faculty_2], departments=[it_department, cs_department, etx_department, mechanical_department],
                        standards=[], subjects=[data_structures, algorithms, physics, mechanical_design],
                        divisions=[cs_1, it_1, etx_1, mech_1], university_name="XYZ University", working_days=working_days)

# Add constraints to the generator
generator = TimetableGenerator(university)
generator.add_constraint(NoClashingLecturesInDivision())
generator.add_constraint(NoClashingFacultyAssignments())
generator.add_constraint(EvenLectureDistribution())
generator.add_constraint(LecturesWithinUniversityTime())
generator.add_constraint(NoLectureDuringBreaks())

# Generate timetable
timetable = generator.generate_timetable()

# Display the generated timetable (simplified)
for lecture in timetable:
    print(f"Lecture: {lecture.subject.name} in Division: {lecture.division.id} scheduled at {lecture.start_from} for Faculty: {lecture.faculty.name}")
