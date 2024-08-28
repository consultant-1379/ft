'''
This module is aimed at providing the needed test suite logic
'''

from base_test_suite import BaseTestSuite
from ext.asyncio     import RunningEventLoop
from ext.contextlib  import NullContext
from test_case       import TestCase

class TestSuite(BaseTestSuite):
    '''
    This class is aimed at providing the general test suite logic
    '''

    def __init__(self, test_suite_config_filename, test_suite_path, test_suite_values, namespace):
        '''
        The constructor of the test suite

        @param test_suite_config_filename: Test suite configuration filename
        @type test_suite_config_filename: str
        @param test_suite_path: Test suite path
        @type test_suite_path: str
        @param test_suite_values: Test Suite configuration file values to be replaced
        @type test_suite_values: list
        @param namespace: K8s namespace
        @type namespace: str
        '''

        super().__init__(
            test_suite_config_filename = test_suite_config_filename,
            test_suite_path            = test_suite_path,
            test_suite_values          = test_suite_values,
            namespace                  = namespace,
            )

    ## END METHOD __init__()

    def pre_condition(self):
        '''
        The precondition of the test suite

        @return: True if the pre_condition execution was ok and False otherwise
        @rtype: bool
        '''

        if not BaseTestSuite.pre_condition(self): return False

        return True

    ## END METHOD pre_condition()

    def start(self):
        '''
        Test suite starting
        '''

        #
        # Instantiate every test case and run its pre, start and post stage
        #

        context = RunningEventLoop if 'servers' in self.test_suite_config_file \
            else NullContext # do nothing
        with context():
            for test_case_name in self.test_suite_config_file["test_cases"]:
                test_case = TestCase(
                    db                     = self.db,
                    namespace              = self.namespace,
                    test_case_config_file  = self.test_cases_config_files[test_case_name],
                    test_case_name         = test_case_name,
                    test_suite_config_file = self.test_suite_config_file,
                    test_suite_path        = self.test_suite_path,
                    )

                if test_case_name in self.test_cases_skipped:
                    test_case.result = "SKIPPED"
                else:
                    if test_case.pre_condition():
                        test_case.start()
                    else:
                        test_case.result = "ERROR"

                    test_case.post_condition()

                self.test_cases.append(test_case)

    ## END METHOD start()

    def post_condition(self):
        '''
        Actions to be taken after testing the suite

        @return: Test suite result
        @rtype: str
        '''

        result = BaseTestSuite.post_condition(self)

        # Additional tear downs here... (do not short-circuit)

        return result

    ## END METHOD post_condition()

## END CLASS TestSuite
