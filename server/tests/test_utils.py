from unittest import TestCase
from datetime import datetime, timezone,time,timedelta
from src.app import Utils


class TestConvertStringToTime(TestCase):

    def test_convert_str_to_datetime_valid_24_hour(self):
        time_str = "10:30 PM"
        result = Utils.convert_str_to_time(time_str, "%I:%M %p")
        self.assertEqual(result, time(22,30))

        time_str = "02:15 AM"
        result = Utils.convert_str_to_time(time_str, "%I:%M %p")
        self.assertEqual(result, time(2,15))

        time_str = "12:00 PM"
        result = Utils.convert_str_to_time(time_str, "%I:%M %p")
        self.assertEqual(result, time(12,0))

        time_str = "12:00 AM"
        result = Utils.convert_str_to_time(time_str, "%I:%M %p")
        self.assertEqual(result, time(0,0))

    def test_convert_str_to_datetime_invalid(self):
        with self.assertRaises(ValueError):
            Utils.convert_str_to_time("25:00 PM", "%I:%M %p")
        with self.assertRaises(ValueError):
            Utils.convert_str_to_time("10:75 AM", "%I:%M %p")
        with self.assertRaises(ValueError):
            Utils.convert_str_to_time("invalid_time", "%I:%M %p")



class TestDatetimeToUTCDateTime(TestCase):
    def test_convert_time_to_utc_time_valid(self):
        local_time = datetime(2024, 11, 30, 10, 30, tzinfo=timezone(timedelta(hours=5, minutes=30)))  # IST
        utc_time = Utils.convert_datetime_to_utc_datetime(local_time)
        expected_time = local_time.astimezone(timezone.utc)
        self.assertEqual(utc_time, expected_time)

    def test_convert_time_to_utc_time_invalid(self):
        naive_time = datetime(2024, 11, 30, 10, 30)  # No timezone info
        with self.assertRaises(ValueError):
            Utils.convert_datetime_to_utc_datetime(naive_time)


# class TestGetSlotsWithTimings(TestCase):
#     def test_standard_case(self):
#         start_time = "9:00 AM"
#         end_time = "11:00 AM"
#         slot_duration = 30 * 60  # 30 minutes in seconds
        
#         # Expected slots: 9:00-9:30, 9:30-10:00, 10:00-10:30, 10:30-11:00
#         slots = Utils.get_slots_with_timing(start_time, end_time, slot_duration)
#         self.assertEqual(len(slots), 4)  # Expecting 4 slots
#         # Check exact dictionary values
#         self.assertEqual(slots[0], {'start_time': time(9, 0), 'end_time': time(9, 30)})
#         self.assertEqual(slots[1], {'start_time': time(9, 30), 'end_time': time(10, 0)})
#         self.assertEqual(slots[2], {'start_time': time(10, 0), 'end_time': time(10, 30)})
#         self.assertEqual(slots[3], {'start_time': time(10, 30), 'end_time': time(11, 0)})

#     def test_edge_case_last_slot_adjustment(self):
#         start_time = "5:00 PM"
#         end_time = "5:15 PM"
#         slot_duration = 30 * 60  # 30 minutes in seconds
        
#         # Expected slot: 5:00-5:15 (last slot adjusted)
#         slots = Utils.get_slots_with_timing(start_time, end_time, slot_duration)
        
#         self.assertEqual(len(slots), 1)  # Expecting 1 slot
#         # Check exact dictionary values
#         self.assertEqual(slots[0], {'start_time': time(17, 0), 'end_time': time(17, 15)})

#     def test_slot_duration_equal_time(self):
#         start_time = "12:00 PM"
#         end_time =  "12:30 PM"
#         slot_duration = 30 * 60  # 30 minutes in seconds
        
#         # Expected slot: 12:00-12:30 (one slot covering the entire time)
#         slots = Utils.get_slots_with_timing(start_time, end_time, slot_duration)
        
#         self.assertEqual(len(slots), 1)  # Expecting 1 slot
#         # Check exact dictionary values
#         self.assertEqual(slots[0], {'start_time': time(12, 0), 'end_time': time(12, 30)})

#     def test_single_slot_case(self):
#         start_time =  "2:00 AM"
#         end_time = "2:10 AM"
#         slot_duration = 30 * 60  # 30 minutes in seconds
        
#         # Expected slot: 2:00-2:10 (since end_time is less than slot_duration, it should be a single small slot)
#         slots = Utils.get_slots_with_timing(start_time, end_time, slot_duration)
        
#         self.assertEqual(len(slots), 1)  # Expecting 1 slot
#         # Check exact dictionary values
#         self.assertEqual(slots[0], {'start_time': time(2, 0), 'end_time': time(2, 10)})

#     def test_invalid_case(self):
#         start_time = "10:00 AM"
#         end_time = "9:00 AM" 
#         # (start time is later than end time, invalid case)
#         slot_duration = 30 * 60  # 30 minutes in seconds
        
#         # Since start_time is after end_time, there should be no slots
#         with self.assertRaises(ValueError):
#             Utils.get_slots_with_timing(start_time, end_time, slot_duration)

#     def test_zero_duration_case(self):
#         start_time = "8:00 AM"
#         end_time = "8:30 AM"
#         slot_duration = 0  # 0 seconds duration (invalid slot duration)
#         slots = Utils.get_slots_with_timing(start_time, end_time, slot_duration)

#         self.assertEqual(len(slots), 0)  # No slots should be returned

