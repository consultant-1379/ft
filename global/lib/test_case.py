'''
This module is aimed at providing the needed test case logic
'''

from base_test_case  import BaseTestCase
from steps.rest_step import RESTStep
from steps.k8s_step  import K8sStep

class TestCase(BaseTestCase):
    '''
    This class is aimed at providing the general test case logic
    '''

    def __init__(self, test_suite_config_file, test_suite_path, test_case_config_file, db, test_case_name, namespace):
        '''
        The constructor of the test case

        @param test_suite_config_file: Test suite configuration file in yaml format
        @type test_suite_config_file: dict
        @param test_suite_path: Test suite path
        @type test_suite_path: str
        @param test_case_config_file: Test case configuration file in yaml format
        @type test_case_config_file: dict
        @param db: Database
        @type db: L{DB}
        @param test_case_name: Test case name
        @type test_case_name: str
        @param namespace: K8s namespace
        @type namespace: str
        '''

        super().__init__(
            test_suite_config_file = test_suite_config_file,
            test_suite_path        = test_suite_path,
            test_case_config_file  = test_case_config_file,
            db                     = db,
            test_case_name         = test_case_name,
            namespace              = namespace,
            )

    ## END METHOD __init__()

    def pre_condition(self):
        '''
        The precondition of the test case

        @return: True if the pre_condition execution was ok and False otherwise
        @rtype: bool
        '''

        if not BaseTestCase.pre_condition(self): return False

        # Additional preconditions here...

        return True

    ## END METHOD pre_condition()

    def start(self):
        '''
        Test case starting
        '''

        test_case_state = {}

        self.result = "PASSED"

        #
        # Steps
        #

        for item in self.test_case_config_file["steps"]:
            step = self._make_step(item)

            success = step.run(
                step            = item,
                test_case_state = test_case_state,
                )

            if not success:
                self.result = "ERROR" if success is None else "FAILED"

                if "stop_on_fail" in item and item["stop_on_fail"] == True:
                    break

        #
        # tearDown
        #

        if "tear_down" in self.test_case_config_file:
            for item in self.test_case_config_file["tear_down"]:
                step = self._make_step(item)

                success = step.run(step=item, test_case_state=test_case_state)

                if "allowed_to_fail" in item and item["allowed_to_fail"]:
                    continue

                else:
                    if not success and self.result == "PASSED":
                        self.result = "ERROR"

    ## END METHOD start()

    def post_condition(self):
        '''
        Actions to be taken after testing the case

        @return: True did all actions success?
        @rtype: bool
        '''

        success = BaseTestCase.post_condition(self)

        # Additional tear downs here...
        # success &= ... # do not short-circuit

        return success

    ## END METHOD post_condition()

    def _make_step(self, item):
        '''
        Make the step

        @param item: Item with the information about the step
        @type item: dict

        @return: Step
        @rtype: L{Step}
        '''

        step = None

        #
        # REST step
        #

        if "request" in item:
            step = RESTStep(
                timeout                = self.test_suite_config_file["request_timeout"],
                test_suite_config_file = self.test_suite_config_file,
                test_suite_path        = self.test_suite_path,
                test_case_name         = self.name,
                db                     = self.db,
                )

        #
        # K8s step
        #

        elif "k8s" in item:
            step = K8sStep(
                test_suite_config_file = self.test_suite_config_file,
                test_suite_path        = self.test_suite_path,
                test_case_name         = self.name,
                db                     = self.db,
                namespace              = self.namespace,
                )

        return step

    ## END METHOD _make_step()

## END CLASS TestCase
