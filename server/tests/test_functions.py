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
from src.domain3 import WorkingDay, Day, DayEnum, Slot, Break, SlotAllotable
from other_utils import save_output_file
from src.app import parse_input_json_to_python,generate_university_timetables_chromosome, generate_gene, get_total_slots_for_university
import  src.genetic_algorithm as ga
# from src.constraints import SameFacultyAtDifferentLectureAtSameTime
import json
import os


class TestEmptyTimetableCreation(TestCase):

    def test_standard_case(self):

    
        with open("./inputs/input_2.json", "r") as f:
            input_data = json.load(f)

        # university,departments,standards,divisions,slots,faculty_subject_division_list,  faculties, subjects = parse_input_json_to_python(input_data)

        output = parse_input_json_to_python(input_data)
        from other_utils import save_output_file

        print("Saving json parsed university input")
        save_output_file('output_2.json', output)
        

        # university_timetables, allotables = generate_university_timetables_chromosome(output)
        chromosome_length = get_total_slots_for_university(output)
        fitness_evaluator = ga.FitnessEvaluator(constraints=[
            # ga.SameFacultyAtDifferentLectureAtSameTime(penalty=1),
            ga.NoLectureAtBreak(penalty=0.5)
        ])
        genetic_algo_university = ga.GeneticAlgorithm(
            data_pool=output,
            chromosome_length=chromosome_length//10,
            fitness_evaluator=fitness_evaluator,
            gene_generator=generate_gene,
            population_size=chromosome_length//10
        )
        university_timetables = genetic_algo_university.run(chromosome_length,0.005)




        print("Saving university timetable ...")
        # print(university_timetables)
        save_output_file('output_utt_1.json', university_timetables)
