from unittest import TestCase, TestSuite,TestLoader,TextTestRunner
from app2 import WorkingDay,DayEnum
import tests.test_utils  as test_utils_module
import tests.test_validators as test_validator_module
import tests.test_functions as test_functional_module

def suite():
    suite = TestSuite()

    # suite.addTests(TestLoader().loadTestsFromModule(test_validator_module))
    # suite.addTests(TestLoader().loadTestsFromModule(test_utils_module))     
    suite.addTests(TestLoader().loadTestsFromModule(test_functional_module))                                                      

    return suite

if __name__ == "__main__":
    runner = TextTestRunner(verbosity=3)
    runner.run(suite())