# Mapper to convert SQLAlchemy models to domain models
from domain import University,Department,Day,Division,Faculty,Slot,SlotAllotable,Standard,Subject,WorkingDay


def university_model_to_domain(university_model):
    return University(
        id=university_model.id,
        university_name=university_model.university_name,
        departments=[department_model_to_domain(department) for department in university_model.departments]
    )

def department_model_to_domain(department_model):
    return Department(
        id=department_model.id,
        department_name=department_model.department_name,
        university_id=department_model.university_id,
        university=university_model_to_domain(department_model.university),
        standards=[standard_model_to_domain(standard) for standard in department_model.standards]
    )

def standard_model_to_domain(standard_model):
    return Standard(
        id=standard_model.id,
        standard_name=standard_model.standard_name,
        department_id=standard_model.department_id,
        department=department_model_to_domain(standard_model.department),
        divisions=[division_model_to_domain(division) for division in standard_model.divisions]
    )

def division_model_to_domain(division_model):
    return Division(
        id=division_model.id,
        division_name=division_model.division_name,
        standard_id=division_model.standard_id,
        standard=standard_model_to_domain(division_model.standard),
        subjects=[subject_model_to_domain(subject) for subject in division_model.subjects]
    )

def subject_model_to_domain(subject_model):
    return Subject(
        id=subject_model.id,
        subject_name=subject_model.subject_name,
        divisions=[division_model_to_domain(division) for division in subject_model.divisions],
        faculties=[faculty_model_to_domain(faculty) for faculty in subject_model.faculties]
    )

def faculty_model_to_domain(faculty_model):
    return Faculty(
        id=faculty_model.id,
        faculty_name=faculty_model.faculty_name,
        subjects=[subject_model_to_domain(subject) for subject in faculty_model.subjects]
    )

def day_model_to_domain(day_model):
    return Day(id=day_model.id, day_name=day_model.day_name)

def working_day_model_to_domain(working_day_model):
    return WorkingDay(
        id=working_day_model.id,
        day_id=working_day_model.day_id,
        start_time=str(working_day_model.start_time),
        end_time=str(working_day_model.end_time),
        slot_duration=working_day_model.slot_duration,
        day=day_model_to_domain(working_day_model.day)
    )

def slot_allotable_model_to_domain(slot_allotable_model):
    return SlotAllotable(
        id=slot_allotable_model.id,
        name=slot_allotable_model.name,
        faculty_id=slot_allotable_model.faculty_id,
        subject_id=slot_allotable_model.subject_id,
        non_teaching=slot_allotable_model.non_teaching,
        slot_id=slot_allotable_model.slot_id,
        slot=slot_model_to_domain(slot_allotable_model.slot) if slot_allotable_model.slot else None
    )

def slot_model_to_domain(slot_model):
    return Slot(
        id=slot_model.id,
        start_time=str(slot_model.start_time),
        end_time=str(slot_model.end_time),
        slot_alloted_to=slot_allotable_model_to_domain(slot_model.slot_alloted_to) if slot_model.slot_alloted_to else None
    )
