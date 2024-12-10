from typing import List, Dict
from datetime import datetime, time, timedelta, timezone
from collections import defaultdict

import uuid

# from src.domain import Slot,WorkingDay,SlotAllotable, Lecture
from  src.domain2 import *
from src.domain_utils import DomainUtils





def get_new_id():
    return str(uuid.uuid4())

class Utils:



    @staticmethod
    def convert_str_to_time(time_str: str, time_format: str = "%I:%M %p") -> time:
        """
        Converts a time string to a datetime object and returns it in 24-hour format.
        :param time_str: The time string to convert.
        :param time_format: The format to parse the time string (default: "%I:%M %p").
        :return: A time object.
        """
        try:
            time_str = time_str.upper().replace("AM", " AM").replace("PM", " PM").strip()
            return datetime.strptime(time_str, time_format).time()
        except ValueError as e:
            raise ValueError(f"Invalid time string '{time_str}' with format '{time_format}': {e}")


    @staticmethod
    def convert_datetime_to_utc_datetime(local_time: datetime) -> datetime:
        """
        Converts a given datetime to UTC.

        :param local_time: A datetime object in local time.
        :return: A datetime object converted to UTC.
        """
        if local_time.tzinfo is None:
            raise ValueError("The provided datetime must be timezone-aware.")
        return local_time.astimezone(timezone.utc)




    @staticmethod
    def get_empty_slots_with_timing(start_time: time, end_time: time,working_day:WorkingDay,weekly_slot_number:int=0, slot_duration: int=30*60) -> List[Slot]:
        """
        Generate a list of empty slots between start_time and end_time.
        :param start_time: The starting time for the day.
        :param end_time: The end time for the day.
        :param slot_duration: The duration of each slot in seconds.
        :return: A list of empty slots.
        """
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)

        if start_datetime > end_datetime:
            raise ValueError("Start time cannot be greater than End time")

        slots = []
        current_time = start_datetime
        daily_slot_number = 0

        while current_time + timedelta(seconds=slot_duration) <= end_datetime:
            next_time = current_time
            current_time = next_time + timedelta(seconds=slot_duration)
            # slots.append(Slot(id=slot_id, start_time=next_time.strftime("%H:%M"), end_time=current_time.strftime("%H:%M"),working_day_id=working_day.id, working_day=working_day))
            slots.append(Slot(id=get_new_id(), start_time=next_time.time(), end_time=current_time.time(),working_day_id=working_day.id, working_day=working_day, daily_slot_number=daily_slot_number, weekly_slot_number=weekly_slot_number))

            daily_slot_number += 1
            weekly_slot_number+=1

        if current_time < end_datetime:
            # slots.append(Slot(id=slot_id, start_time=current_time.strftime("%H:%M"), end_time=end_datetime.strftime("%H:%M"),working_day_id=working_day.id, working_day=working_day))
            slots.append(Slot(id=get_new_id(), start_time=current_time.time(), end_time=end_datetime.time(),working_day_id=working_day.id, working_day=working_day, weekly_slot_number=weekly_slot_number, daily_slot_number=daily_slot_number))


        return slots

    @staticmethod
    def find_slots_for_a_time_range(working_day: WorkingDay, start_time: time, end_time: time) -> List[int]:
        """
        Find slot numbers within a time range.
        :param working_day: The working day that contains the slots.
        :param start_time: The start time for the range.
        :param end_time: The end time for the range.
        :return: A list of slot IDs.
        """
        slot_numbers = []
        empty_slots_for_the_week = Utils.get_empty_slots_with_timing(working_day.start_time, working_day.end_time,slot_duration= working_day.slot_duration, working_day=working_day)


        start_slot = None
        end_slot = None


        for slot in empty_slots_for_the_week:
            if slot.working_day_id == working_day.id:
                if slot.start_time == start_time.strftime("%H:%M") and slot.end_time == end_time.strftime("%H:%M"):
                    slot_numbers.append(slot.id)
                    return slot_numbers

                if slot.start_time == start_time.strftime("%H:%M"):
                    start_slot = slot.weekly_slot_number

                if slot.end_time == end_time.strftime("%H:%M"):
                    end_slot = slot.weekly_slot_number

                if start_slot is not None and end_slot is not None:
                    for i in range(start_slot, end_slot):
                        slot_numbers.append(i)
                    slot_numbers.append(end_slot)

        if start_slot is None or end_slot is None:
            raise ValueError("Start Time or End Time goes beyond the working hours.")

        return slot_numbers

    @staticmethod
    def create_weekly_slots_table(working_days: List[WorkingDay]) -> List[Slot]:
        """
        Create a timetable with empty slots, marking the occupied slots as well.
        :param working_days: The working days list.
        :return: A dictionary with days and their corresponding slots.
        """
        # empty_time_table = defaultdict(list)
        empty_time_table:List[Slot] = []
        
        weekly_slot_number_count = 0

        for work_day in working_days:
            day = work_day.day

            slots = Utils.get_empty_slots_with_timing(work_day.start_time, work_day.end_time,work_day,weekly_slot_number_count, work_day.slot_duration)
            if slots:  # Ensure the list is not empty
                max_weekly_slot_number = max(slots, key=lambda slot: slot.weekly_slot_number).weekly_slot_number
                weekly_slot_number_count = max(weekly_slot_number_count, max_weekly_slot_number)+1
            else:
                max_weekly_slot_number = None  # Handle the case where slots is empty
            # empty_time_table[day.day_name] = slots
            empty_time_table.extend(slots)
            # for break_lecture in work_day.breaks:
            #     break_range = Utils.find_slots_for_a_time_range(work_day, break_lecture.slot.start_time, break_lecture.slot.end_time)
            #     for break_slot_number in break_range:
            #         for slot in empty_time_table[day.day_name]:
            #             if slot.id == break_slot_number:
            #                 slot.slot_alloted_to = None  # Mark slot as occupied by break
        return empty_time_table


class Validators:

    @staticmethod
    def is_valid_str_time(time_str: str, time_format: str = "%I:%M %p") -> bool:
        """
        Validates if the given string is a valid time.
        :param time_str: The time string to validate.
        :param time_format: The format against which to validate the time string (default: "%I:%M %p").
        :return: True if valid, False otherwise.
        """
        try:
            # Parse the string with the given format
            datetime.strptime(time_str, time_format)
            return True
        except ValueError:
            return False


def assign_lectures_to_slots(working_days: List[WorkingDay], lectures: List[SlotAllotable]) -> dict:
    """
    Assign lectures to available slots in the timetable.
    :param working_days: List of working days.
    :param lectures: List of lectures to be assigned to the timetable slots.
    :return: A dictionary with days as keys and list of slots with lectures assigned.
    """
    time_table = Utils.create_weekly_slots_table(working_days)

    for day_name, slots in time_table.items():
        for slot in slots:
            for lecture in lectures:
                if lecture.slot and lecture.slot.id == slot.id:
                    slot.slot_alloted_to = lecture  # Assign the lecture to the slot
    return time_table


    
import random
def allot_allotables_to_slots(slots:List[Slot]=None, lectures:List[FacultySubjectDivision]=None, breaks:List[Break]=None):
    if slots is None:
        slots = []
    if lectures is None:
        lectures = []
    if breaks is None:
        breaks = []

    slots_len = len(slots)
    lectures.extend(breaks)
    lec_len = len(lectures)

    blaclist_slots= []
    blacklist_lec = []


    # for lec in lectures:
    #     for slot in slots:
    #         if lec.faculty_id is None: #That means it is a break
    #             weekly_slots_range = Utils.find_slots_for_a_time_range(slot.working_day, lec.)

        # for slot in slots:
        # if slot.slot_alloted_to is None:
            
        # slot_alloted =False
        # while slot_alloted is not True  and len(blaclist_num) < lec_len:
    while len(blacklist_lec) < lec_len:

        # print("here 1")
        rand_allotable_num  = random.randint(0,lec_len-1)
        rand_slots_num  = random.randint(0,slots_len-1)


        if rand_allotable_num not in blacklist_lec and rand_slots_num not in blaclist_slots:
            slots[rand_slots_num].slot_alloted_to = lectures[rand_allotable_num]
            blacklist_lec.append(rand_allotable_num)
            blaclist_slots.append(rand_slots_num)
            # slot_alloted = True


    return slots






# STEPS
# 1. Prase JSON to Python
# 2. Validate
    # Dates, Time

def parse_input_json_to_python(input_data: Dict):
    slots: List[Slot] = []
    faculty_subject_division_list: List[FacultySubjectDivision] = []
    subjects_list: List[Subject] = []
    faculties_list:List[Faculty] = []

    departments_list = []
    standards_list = []
    divisions_list=[]
    working_days_list=[]
    universities = []

    breaks_list = []
    # Create university
    university = University(
        id=get_new_id(),
        university_name=input_data["university"],
    )

    universities.append(university)


    # Parse departments
    for dept_data in input_data["departments"]:
        department = Department(
            id=get_new_id(),
            department_name=dept_data["departmentName"],
            university_id=university.id,
            university=university
        )
        departments_list.append(department)

    # Parse standards
    for std_data in input_data["standards"]:
        department = next((dept for dept in departments_list if dept.department_name == std_data['departmentName']), None)
        standard = Standard(
            id=get_new_id(),
            standard_name=std_data["standardName"],
            department_id=department.id,
            department=department
        )
        standards_list.append(standard)

    # Parse divisions
    for div_data in input_data["divisions"]:
        standard = next((std for std in standards_list if std.standard_name == div_data['standardName']), None)
    
        division = Division(
            id=get_new_id(),
            division_name=div_data["divisionName"],
            standard_id=standard.id,
            standard=standard
        )
        divisions_list.append(division)

    # Parse working days
    for working_day in input_data["workingDays"]:
        division = next((div for div in divisions_list if div.division_name == working_day['divisionName']), None)
        if division is None:
            raise Exception("Invalid division in working days section - ",working_day['divisionName'])
        schedule = working_day['schedule']
        for day_data in schedule:
            day_enum = DayEnum[day_data["dayName"]]
            day = Day(
                id=get_new_id(),
                day_name=day_enum.value
            )
            working_day = WorkingDay(
                id=get_new_id(),
                day_id=day.id,
                # start_time=datetime.strptime(day_data["startTime"], "%I:%M%p").time(),
                # end_time=datetime.strptime(day_data["endTime"], "%I:%M%p").time(),
                start_time=Utils.convert_str_to_time(day_data["startTime"]),
                end_time=Utils.convert_str_to_time(day_data["endTime"]),
                slot_duration=day_data["slotSize"],
                day=day,
                division_id=division.id,
                division=division
            )

            working_days_list.append(working_day)

            # Parse breaks
            for break_data in day_data.get("breaks", []):
                breaks_list.append(Break(
                    id=get_new_id(),
                    division_id=division.id,
                    division=division,
                    name=break_data["breakName"],
                    start_time=Utils.convert_str_to_time(break_data["startTime"]),
                    end_time=Utils.convert_str_to_time(break_data["endTime"]),
                    working_day_id=working_day.id,
                    working_day=working_day,
                    continuos_slot=1

                ))
                # slot = Slot(
                #     id=get_new_id(),
                #     start_time=Utils.convert_str_to_time(break_data["startTime"]),
                #     end_time=Utils.convert_str_to_time(break_data["endTime"]),
                #     working_day_id=working_day.id,
                #     working_day=working_day,
                #     slot_alloted_to=Break(
                #         id=get_new_id(),
                #         name=break_data["breakName"],
                #         division_id=division.id,
                #         division=division
                #     )
                # )
                # slots.append(slot)
    for subject in input_data['subjects']:
        subject_instance = Subject(get_new_id(),subject['subjectName'])
        subjects_list.append(subject_instance)

    for faculty in input_data['faculties']:
        faculty_instance = Faculty(get_new_id(),faculty['facultyName'])
        faculties_list.append(faculty_instance)

    # # Parse subjects and faculties
    # subjects = {sub["subjectName"]: Subject(id=get_new_id(), subject_name=sub["subjectName"]) for sub in input_data["subjects"]}
    # faculties = {fac["facultyName"]: Faculty(id=get_new_id(), faculty_name=fac["facultyName"]) for fac in input_data["faculties"]}

    # Parse subject-faculty-division relationships
    for rel_data in input_data["subjectFacultyDivision"]:
        division = next((div for div in divisions_list if div.division_name == rel_data['divisionName']), None)
        faculty = next((fac for fac in faculties_list if fac.faculty_name == rel_data['facultyName']), None)
        subject = next((sub for sub in subjects_list if sub.subject_name == rel_data['subjectName']), None)


        
        if not (division or subject or faculty):
            raise Exception("Invalid division or subject or faculty")
            # continue  # Skip if division not found

        faculty_subject_division_list.append(FacultySubjectDivision(
            id=get_new_id(),
            name=f"{subject.subject_name} - {faculty.faculty_name}",
            faculty_id=faculty.id,
            subject_id=subject.id,
            division_id=division.id,
            faculty=faculty,
            subject=subject,
            division=division,
            continuos_slot=1
        ))

    return {
        "university": university,
        "departments": departments_list,
        "standards":standards_list,
        "divisions":divisions_list,
        "subjects":subjects_list,
        "faculties":faculties_list,
        "slots": slots,
        "faculty_subject_division_list": faculty_subject_division_list,
        "working_days":working_days_list,
        "breaks_list":breaks_list,
        "universities":universities
    }


def get_allotable_timings(start_time:time, end_time:time, slot_duration=30*60):
    # for eg 9 am -10 am with slot duration of 30min
    # return [{"start_time":9 am, end_time: 10am}, {starT-time: 9 30 am, end_time: 10 am}]
    slots = []
    current_time = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    slot_delta = timedelta(seconds=slot_duration)

    while current_time + slot_delta <= end_datetime:
        slot_start = current_time.time()
        slot_end = (current_time + slot_delta).time()
        slots.append({"start_time": slot_start, "end_time": slot_end})
        current_time += slot_delta

    return slots



def generate_slot_objects(obj, start_time, end_time, slot_duration):
    """
    Generates a list of cloned objects with updated start_time and end_time properties.

    Args:
        obj (dict): The object to clone (can be a dictionary or a class instance).
        start_time (time): The start time of the range.
        end_time (time): The end time of the range.
        slot_duration (int): Duration of each slot in seconds.

    Returns:
        list: A list of cloned objects with updated times.
    """
    current_start = start_time
    slots = []
    
    while current_start < end_time:
        current_end = (datetime.combine(datetime.min, current_start) + timedelta(seconds=slot_duration)).time()
        if current_end > end_time:
            break
        
        # Clone the object
        if isinstance(obj, dict):
            cloned_obj = obj.copy()
        else:
            cloned_obj = obj.__class__(**{k: v for k, v in obj.__dict__.items()})
        
        # Update start_time and end_time attributes
        if isinstance(cloned_obj, dict):
            cloned_obj["start_time"] = current_start
            cloned_obj["end_time"] = current_end
        else:
            setattr(cloned_obj, "start_time", current_start)
            setattr(cloned_obj, "end_time", current_end)
        
        slots.append(cloned_obj)
        current_start = current_end
    
    return slots

def find_continuos_slot_count(start_time, end_time, slot_duration)->int:
    # 9 am - 10 30 am ---- slot_duration 30 min ---- output 3
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    
    # Calculate the difference in seconds
    total_duration_seconds = (end_dt - start_dt).total_seconds()
    # Divide by slot duration to find the number of slots
    num_slots = int(total_duration_seconds // slot_duration)
    return num_slots

def create_university_timetables(data:Dict):
    domain_utils = DomainUtils(data)

    university_timetables:UniversityTimetables = UniversityTimetables()
    all_university_slots :List[Slot] = []
    divisions = domain_utils.get_all_divisions()

    tryAttempt = 0
    total_weightage = 100
    while total_weightage >= 1.0:
        tryAttempt+=1
        print(f"Attempt no - {tryAttempt}")
        total_weightage = 0
        all_university_slots = []
        for division in divisions:
            allotables_for_div = [
                lec 
                for lec in domain_utils.get_faculty_subject_division_list() 
                if division.id == lec.division_id 
                for _ in range(lec.continuos_slot)  # Duplicate based on continous_slot
            ]            
            div_weekly_breaks = []
            for brk in domain_utils.get_all_breaks():
                if brk.division_id == division.id:
                    # Generate multiple slots for breaks
                    generated_breaks = generate_slot_objects(
                        obj=brk,
                        start_time=brk.start_time,
                        end_time=brk.end_time,
                        slot_duration=brk.working_day.slot_duration
                    )
                    div_weekly_breaks.extend(generated_breaks)
            
            allotables_for_div.extend(div_weekly_breaks)


            working_days_for_div = [working_day for working_day in domain_utils.get_all_working_days() if division.id == working_day.division_id]
            div_weekly_empty_slots = Utils.create_weekly_slots_table(working_days_for_div)
            

            div_alloted_slots = allot_allotables_to_slots(div_weekly_empty_slots, allotables_for_div, div_weekly_breaks)
            all_university_slots.extend(div_alloted_slots)
            # timetable:Timetable = Timetable(division, div_alloted_slots)
            # university_timetables.timetables.append(timetable)

        from src.constraints import NoLectureAtBreak
        constraints = [NoLectureAtBreak(1.0,all_university_slots )]

        for constarint in constraints:
            constraint_weight = constarint.apply()
            print(f"Attempt -{tryAttempt} - constaint weight -{constraint_weight}")
            total_weightage+=constraint_weight
        # total_weightage =0
    return all_university_slots
    

