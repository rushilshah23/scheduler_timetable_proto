from datetime import datetime, timezone,time,timedelta
from enum import Enum
from abc import ABC,abstractmethod
from typing import Dict, List, Tuple

class Config:
    SLOT_DURATION = 30*60



class DayEnum(Enum):
    MONDAY="MONDAY"
    TUESDAY="TUESDAY"
    WEDNESDAY="WEDNESDAY"
    THURSDAY="THURSDAY"
    FRIDAY="FRIDAY"
    SATURDAY="SATURDAY"
    SUNDAY="SUNDAY"




class University():
    def __init__(self,id:str,university_name:str):
        self.id = id
        self.university_name = university_name

class Department():
    def __init__(self,id:str,department_name:str,university:University):
        self.id = id
        self.department_name = department_name
        self.university = university

class Standard():
    def __init__(self,id:str,standard_name:str,department:Department):
        self.id = id
        self.standard_name = standard_name
        self.department = department

class Division():
    def __init__(self,id:str,division_name:str,standard:Standard,department:Department):
        self.id = id
        self.division_name = division_name
        self.standard = standard
        self.department = department

class Subject():
    def __init__(self,id:str,subject_name:str,division:Division):
        self.id = id
        self.subject_name = subject_name
        self.division = division

class Faculty():
    def __init__(self,id:str,faculty_name:str,subjects:list[Subject]):
        self.id = id
        self.faculty_name = faculty_name
        self.subjects = subjects


class Slot:
    def __init__(self,id:str, start_time:time, end_time:time,is_occupied:bool=False):
        self.id = id
        self.start_time=start_time
        self.end_time=end_time
        self.is_occupied = is_occupied

    def to_dict(self):
        return {
            'start_time': self.start_time.strftime("%H:%M"),
            'end_time': self.end_time.strftime("%H:%M"),
            'is_occupied':self.is_occupied
        }



class Lecture():
    def __init__(self,id:str,name:str,faculty:Faculty,subject:Subject,continous_slot_count:int=1):
        self.id = id
        self.faculty = faculty
        self.subject = subject
        self.continous_slot_count = continous_slot_count
        # self.slot = slot

class Break(Lecture):
    def __init__(self,id:str,name:str, slot:Slot,continuous_slots:int=1):
        super().__init__(id,name,None,None,slot,continuous_slots)


class WorkingDay():
    def __init__(self,id:str,day:DayEnum,workday_slot:Slot,slot_duration:int=Config.SLOT_DURATION,breaks:list[Break]=[]):
        self.id = id
        self.day = day
        self.workday_slot = workday_slot
        self.breaks = breaks
        self.slot_duration = slot_duration

class LectureSlot():
    def __init__(self,slot:Slot, lecture:Lecture):
        self.slot = slot,
        self.lecture = lecture

class TimeTable():

    def __init__(self,working_days:List[WorkingDay]=[],lectures:List[Lecture]=[]):
        self.working_days = working_days
        self.lectures= lectures

    def create_timetable()-> Dict[str, list[Dict[str,Tuple[Slot, Lecture]]]]:
        pass
    





class Validators:
    def is_valid_str_time(time_str: str, time_format: str = "%I:%p") -> bool:
        """
        Validates if the given string is a valid time.

        Supported formats include:
        - 2:PM
        - 02:PM
        - 2:pm
        - 02:pm

        :param time_str: The time string to validate.
        :param time_format: The format against which to validate the time string (default: "%I:%p").
        :return: True if valid, False otherwise.
        """
        try:
            # Parse the string with the given format
            datetime.strptime(time_str, time_format)
            return True
        except ValueError:
            return False

class Utils:

    @staticmethod
    def convert_str_to_time(time_str: str, time_format: str = "%I:%M %p") -> time:
        """
        Converts a time string to a datetime object and returns it in 24-hour format.

        Supported time formats include:
        - 2:PM
        - 02:PM
        - 2:pm
        - 02:pm

        :param time_str: The time string to convert.
        :param time_format: The format to parse the time string (default: "%I:%p").
        :return: A string representing the time in 24-hour format (HH:MM).
        :raises ValueError: If the time string is invalid or doesn't match the format.
        """
        try:
            time_str = time_str.upper().replace("AM", " AM").replace("PM", " PM").strip()

            # Parse the time string into a time object
            time_obj = datetime.strptime(time_str, time_format).time()
            # Format the time into a 24-hour string
            # return time_obj.strftime("%H:%M")
            return time_obj
        
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
    def get_empty_slots_with_timing(start_time_str: str, end_time_str: str, slot_duration: int=Config.SLOT_DURATION)-> list[Slot]:
        # start_time:time = Utils.convert_str_to_time(start_time_str)
        # end_time:time = Utils.convert_str_to_time(end_time_str)
        # Convert time to datetime to perform operations
        start_datetime = datetime.combine(datetime.today(), start_time_str)
        end_datetime = datetime.combine(datetime.today(), end_time_str)
        if start_datetime > end_datetime:
            raise ValueError("Start time cannot be greater than End time")
        slots = []
        current_time = start_datetime
        slot_number = 0

        if slot_duration > 0:
            while current_time + timedelta(seconds=slot_duration) <= end_datetime:
                next_time = current_time
                current_time = next_time + timedelta(seconds=slot_duration)
                
                # Define the slot as a dictionary with start and end times
                new_slot = Slot(slot_number, next_time.time(), current_time.time())
                # new_slot = {
                #     # "start_time": next_time.time().strftime("%H:%M"),
                #     # "end_time": current_time.time().strftime("%H:%M")
                #     "start_time": next_time.time(),
                #     "end_time": current_time.time()
                # }
                slots.append(new_slot)
                slot_number += 1
            
            # Handle the last slot where duration might be less than the usual slot
            if current_time < end_datetime:
                new_slot = Slot(slot_number, current_time.time(), end_datetime.time())
                # new_slot:Slot = {
                #     # "start_time": current_time.time().strftime("%H:%M"),
                #     # "end_time": end_datetime.time().strftime("%H:%M")
                #     "start_time": current_time.time(),
                #     "end_time": end_datetime.time()

                # }
                slots.append(new_slot)

        return slots

    @staticmethod
    def find_slots_for_a_time_range(working_day:WorkingDay,start_time:time,end_time:time )-> list[int]:
        slot_numbers:list[int] = []
        
        empty_slots_for_the_day =  Utils.get_empty_slots_with_timing(working_day.workday_slot.start_time,working_day.workday_slot.end_time)
        start_number = None
        end_number =  None
        for slot_item in empty_slots_for_the_day:
            # print('slot item startTime - ',slot_item.start_time,"   endTime- ",slot_item.end_time )
            if slot_item.start_time == start_time and slot_item.end_time == end_time:
                
                slot_numbers.append(slot_item.id)
                return slot_numbers


            if slot_item.start_time == start_time:
                start_number = slot_item.id
                
            if slot_item.end_time == end_time:
                end_number = slot_item.id

            if start_number is not None and end_number is not None:
                for i in range(start_number,end_number):
                    slot_numbers.append(i)
                slot_numbers.append(end_number)

        if start_number is None or end_number is None:
            raise ValueError("Start Time or End Time goes beyond the working hours - ",start_time," - ",end_time )
        
        return slot_numbers
            



        

def create_weekly_slots_table(working_days:list[WorkingDay])->Dict[str,list[Slot]]:
    empty_time_table:Dict[str, list[Slot]] = {}

    for work_day in working_days:
        day = work_day.day
        
        slots = Utils.get_empty_slots_with_timing(work_day.workday_slot.start_time,work_day.workday_slot.end_time,work_day.slot_duration)
        empty_time_table[day] = slots
        for break_lecture in work_day.breaks:
            break_range:list[int] = Utils.find_slots_for_a_time_range(work_day,break_lecture.slot.start_time, break_lecture.slot.end_time)
            for break_slot_number in break_range:
                for index,slot in enumerate(empty_time_table[day]):
                    if slot.id == break_slot_number:
                        empty_time_table[day][index].is_occupied = True
    return empty_time_table



class Constraint(ABC):

    @abstractmethod
    def perform_check()->bool:
        pass

class SameFacultyLectureDoesntClash(Constraint):
    def perform_check(self, ) -> bool:
        pass


if __name__ =="__main__":
    start_time_str = "10:00am"
    end_time_str = "12:00 pm"
    print(Utils.convert_str_to_time(start_time_str))
    print(Utils.convert_str_to_time(end_time_str))


    # print(Utils.get_slots_with_timing("10:00 pm","12:00 pm",30*60))








# STOPPED AT CHECKING BREAK IN EMPTY TABLE BEACUSE OF TIME ISSUE