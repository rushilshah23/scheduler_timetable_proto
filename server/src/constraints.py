from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from src.domain2 import Constraint, Slot, Break
from src.app import Utils, get_allotable_timings



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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            # Add any additional details specific to this constraint
        })
        return base_dict
    


@dataclass
class NoLectureAtBreak(Constraint):
    failed_weightage =  1.0
    slots:List[Slot] = None

    def __post_init__(self):

        if self.slots is None:
            self.slots = []
    
    def apply(self):
        for i in range(len(self.slots)):
            slot = self.slots[i]
            if slot.slot_alloted_to is not None:
                if slot.slot_alloted_to.fixed_slot == True and (slot.start_time != slot.slot_alloted_to.start_time or slot.end_time != slot.slot_alloted_to.end_time):
                    print(f"SLot start time - {slot.start_time} SLot end time - {slot.end_time} SLote alloted start time - {slot.slot_alloted_to.start_time} SLot alloted to endtime - {slot.slot_alloted_to.end_time}")
                    return self.failed_weightage

        return 0

# @dataclass
# class CompulsaryContinuosSlot(Constraint):
#     failed_weightage =  1.0
#     slots:List[Slot] = None

#     def __post_init__(self):

#         if self.slots is None:
#             self.slots = []
    
#     def apply(self):
#         for i in range(len(self.slots)):
#             slot = self.slots[i]
#             if slot.slot_alloted_to.continuos_slot > 1:
#                 allotment_start_time = slot.slot_alloted_to.start_time
#                 allotment_end_time = slot.slot_alloted_to.end_time

#                 time_slots = get_allotable_timings(allotment_start_time,allotment_end_time, slot.working_day.slot_duration)

#                 for ts in time_slots:
#                     if ts["start_time"]
#                 if ((slot.start_time == slot.slot_alloted_to.start_time and slot.end_time == slot.slot_alloted_to.end_time) or (slot.start_time == slot.slot_alloted_to.start_time and slot.end_time <= slot.slot_alloted_to.end_time) or (slot.end_time == slot.slot_alloted_to.end_time and slot.start_time >= slot.slot_alloted_to.start_time) ):
#                     return 0
#         return self.failed_weightage
