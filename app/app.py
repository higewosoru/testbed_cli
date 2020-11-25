
import os

from testrun.testrun import TestsParse, TestRunner, TooManyYAMLFiles
from gui.gui import GUI


yaml_file_location = "../"
yaml_list = TestsParse.find_yaml_files(yaml_file_location)
if len(yaml_list) != 1:
    raise TooManyYAMLFiles(len(yaml_list))
else:
    cli_tests_configuration = os.path.abspath(os.path.join(yaml_file_location, yaml_list[0]))
# cli_tests_configuration = os.path.abspath("../testfile.yaml")

class TestbedCLI:
    def __init__(self, config_file):
        tests_info = TestsParse(config_file)
        test = TestRunner(tests_info)
        self.gui = GUI(testrunner=test, testing=False)

    def start_cli(self):
        self.gui.start_gui()


if __name__ == "__main__":
    cli = TestbedCLI(cli_tests_configuration)
    cli.start_cli()