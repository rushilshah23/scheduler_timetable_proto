# from unittest import TestCase
# from app2 import WorkingDay, DayEnum,University,create_weekly_slots_table, Break,Slot,Utils
# import os
# import sys
# from other_utils import save_output_file


# class TestEmptyTimetableCreation(TestCase):

#     def test_standard_case(self):
#         # university_1 = University("U1","University 1")
#         break_1_slot_1 = Slot("bk1s1",Utils.convert_str_to_time("1:00pm"),Utils.convert_str_to_time("2:30pm"))
#         break_1_slot_2 = Slot("bk1s1",Utils.convert_str_to_time("9:00am"),Utils.convert_str_to_time("4:35pm"))

#         break_1 = Break('bk1',"BreakFast",break_1_slot_1)
#         workday_slot_1 = Slot('wdsl1',Utils.convert_str_to_time("9:00am"),Utils.convert_str_to_time("5:00pm"))
#         day_1 = WorkingDay("U1WD1",day=DayEnum.MONDAY.value, workday_slot= workday_slot_1, breaks=[break_1])
#         day_2 = WorkingDay("U1WD2",day=DayEnum.TUESDAY.value, workday_slot= workday_slot_1, )
#         day_3 = WorkingDay("U1WD3",day=DayEnum.WEDNESDAY.value, workday_slot= workday_slot_1, )
#         day_4 = WorkingDay("U1WD4",day=DayEnum.THURSDAY.value, workday_slot=workday_slot_1)
#         day_5 = WorkingDay("U1WD5",day=DayEnum.FRIDAY.value,workday_slot= workday_slot_1,)

#         working_days = [day_1,day_2,day_3,day_4,day_5]

#         weekly_slots=  create_weekly_slots_table(working_days)
#         # print(weekly_slots)
#         save_output_file('output_1.json', weekly_slots)
     



from unittest import TestCase
from datetime import time,datetime,date,timedelta
from src.domain import WorkingDay, Day, DayEnum, Slot, Break, SlotAllotable, Lecture
from other_utils import save_output_file
from src.app import allot_allotables_to_slots,parse_input_json_to_python,create_university_timetables
import json
import os


class TestEmptyTimetableCreation(TestCase):

    def test_standard_case(self):
    #     # Create Day objects
    #     monday = Day(id=1, day_name=DayEnum.MONDAY.value)
    #     tuesday = Day(id=2, day_name=DayEnum.TUESDAY.value)
    #     wednesday = Day(id=3, day_name=DayEnum.WEDNESDAY.value)
    #     thursday = Day(id=4, day_name=DayEnum.THURSDAY.value)
    #     friday = Day(id=5, day_name=DayEnum.FRIDAY.value)

    #     # Define WorkingDay objects
    #     day_1 = WorkingDay(id=1, day_id=1, day=monday, start_time=time(9, 0), end_time=time(17, 0), slot_duration=30*60)
    #     day_2 = WorkingDay(id=2, day_id=2, day=tuesday, start_time=time(9, 0), end_time=time(17, 0), slot_duration=30*60)
    #     day_3 = WorkingDay(id=3, day_id=3, day=wednesday, start_time=time(9, 0), end_time=time(17, 0), slot_duration=30*60)
    #     day_4 = WorkingDay(id=4, day_id=4, day=thursday, start_time=time(9, 0), end_time=time(17, 0), slot_duration=30*60)
    #     day_5 = WorkingDay(id=5, day_id=5, day=friday, start_time=time(9, 0), end_time=time(17, 0), slot_duration=30*60)

    #     # Define slots for break periods
    #     break_slot_1 = Slot(id=1, start_time="13:00", end_time="14:00")
    #     break_slot_2 = Slot(id=2, start_time="15:00", end_time="15:30")

    #     # Assign break slots (optional association for testing purposes)
    #     break_1 = Break(id="bk1", name="Lunch Break", slot=break_slot_1)
    #     break_2 = Break(id="bk2", name="Short Break", slot=break_slot_2)

    #     # Create SlotAllotable for the testing purpose
    #     slot_allotable = SlotAllotable(id=1, name="Faculty A", slot_id=1, slot=break_slot_1)

    #     # Assume some break periods are allocated to the working days
    #     day_1.breaks = [break_1]  # Example of assigning breaks (if such association was intended)

    #     # Put all working days in a list
    #     working_days = [day_1, day_2, day_3, day_4, day_5]

    #     # Generate the weekly timetable using the updated function (which handles the slot logic)
    #     weekly_slots = self.generate_weekly_slots_table(working_days)

    #     # Print the result for viewing in the console
    #     print(weekly_slots)

    #     # Save the result to a file for later inspection
    #     save_output_file('output_1.json', weekly_slots)

    # def generate_weekly_slots_table(self, working_days):
    #     """
    #     Generates a timetable for the whole week, considering working days,
    #     breaks, and slot allocations.
    #     """
    #     weekly_schedule = {}
    #     for day in working_days:
    #         # Accessing the day_name through the day attribute of WorkingDay
    #         day_name = day.day.day_name
    #         slots = self.create_slots_for_day(day)
    #         weekly_schedule[day_name] = slots
    #     return weekly_schedule

    # def create_slots_for_day(self, working_day):
    #     """
    #     Create the slots for a single working day, considering slot durations and breaks.
    #     """
    #     slots = []
    #     start_time = working_day.start_time
    #     end_time = working_day.end_time
    #     duration = working_day.slot_duration

    #     current_time = start_time
    #     while current_time < end_time:
    #         slot_start = current_time.strftime("%H:%M")
    #         slot_end = (datetime.combine(date.today(), current_time) + timedelta(seconds=duration)).strftime("%H:%M")
    #         slot = Slot(id=len(slots) + 1, start_time=slot_start, end_time=slot_end)
    #         slots.append(slot)

    #         # Increment current_time by slot duration
    #         current_time = (datetime.combine(date.today(), current_time) + timedelta(seconds=duration)).time()

    #     return slots



        # slot_1 = Slot(1,"10:00am","10:30am")
        # slot_2 = Slot(2,"10:30am","11:00am")
        # slot_3 = Slot(3,"11:00am","11:30am")
        # slot_4 = Slot(4,"11:30am","12:00pm")
        # slot_5 = Slot(5,"12:00pm","12:30pm")
        # slot_6 = Slot(6,"12:30pm","01:00pm")

        # lec_1 = Lecture(1,"lec 1", 1,1)
        # lec_2 = Lecture(2,"lec 2", 2,1)
        # lec_3 = Lecture(3,"lec 3", 3,1)
        # lec_4 = Lecture(4,"lec 4", 2,2)
        # lec_5 = Lecture(5,"lec 5", 3,2)
        # lec_6 = Lecture(6,"lec 6", 1,3)

        # output = allot_allotables_to_slots([
        #     slot_1,slot_2,slot_3,slot_4,slot_5,slot_6
        # ],[
        #     lec_1,lec_2,lec_3,lec_4,lec_5,lec_6
        # ])

        # save_output_file('slot_lec_map.json',output)


    
        with open("./inputs/input_2.json", "r") as f:
            input_data = json.load(f)

        # university,departments,standards,divisions,slots,faculty_subject_division_list,  faculties, subjects = parse_input_json_to_python(input_data)

        output = parse_input_json_to_python(input_data)
        from other_utils import save_output_file

        print("Saving json parsed university input")
        save_output_file('output_2.json', output)
        
        university_timetables = create_university_timetables(output)

        print("Saving university timetable ...")
        # print(university_timetables)
        save_output_file('output_utt_1.json', university_timetables)
