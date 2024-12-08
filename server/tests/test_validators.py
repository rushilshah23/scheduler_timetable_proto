from unittest import TestCase
from src.app import Validators

class TestValidStringTime(TestCase):
    def test_is_valid_str_datetime_valid(self):
        self.assertFalse(Validators.is_valid_str_time("2:pm"))
        self.assertTrue(Validators.is_valid_str_time("2024-11-30", "%Y-%m-%d"))
        

    def test_is_valid_str_datetime_invalid(self):
        self.assertFalse(Validators.is_valid_str_time("30-11-2024 10:30:00"))
        self.assertFalse(Validators.is_valid_str_time("2024-11-30 25:30:00"))
        self.assertFalse(Validators.is_valid_str_time("2024-11-30"))

    def test_is_valid_str_datetime_custom_format(self):
        self.assertTrue(Validators.is_valid_str_time("30/11/2024", "%d/%m/%Y"))
        self.assertFalse(Validators.is_valid_str_time("30-11-2024", "%d/%m/%Y"))
