'''
Test information and locations are stored in tests.yaml. This module parses that file and returns the proper
items to find and run test files according to the specified configuration.
'''

'''
This module contains the backend of the testserver cli.... mainly to do with getting the proper
directory/location string, validating test files, and running test subprocesses. Used in conjunction with
appcoonfig, the yaml test configuration parser.
'''

import yaml
import os
import subprocess
import getch


class InvalidOptionException(Exception):
    def __init__(self):
        self.message = "An invalid option was selected."  # TODO: this is the worst error message.
        super().__init__(self.message)

class TooManyYAMLFiles(Exception):
    def __init__(self, count, max_files=1):
        self.message = "Found too many YAML files. Expected {}, found {}.".format(max_files, count)
        super().__init__(self.message)

class TestsParse:
    """
    the options below ending in _str are search terms for locating options in the yaml file.
    they should reflect the desired field in the yaml test configuration.
    """
    def __init__(self, filename, rev_string='revisions', location_str='test_location',
                 basecmd_str='base_cmd', testfile_str='test_file', required_options_str='req_opts'):
        self.cfg = None
        self.cfg_filename = filename
        self.rev_string = rev_string
        self.testloc_str = location_str
        self.base_cmd_str = basecmd_str
        self.testfile_str = testfile_str
        self.req_opt_str = required_options_str
        print("Using config file: {}".format(filename))
        with open(filename) as file:
            self.cfg = yaml.load(file, Loader=yaml.FullLoader)

    @staticmethod
    def find_yaml_files(search_directory):
        ret_list = []
        for item in os.listdir(os.path.abspath(search_directory)):
            full_path = os.path.abspath(item)
            if os.path.isdir(full_path):
                pass
            else:
                filename, file_extension = os.path.splitext(full_path)
                if file_extension == (('.yaml' ) or ('.YAML')):
                    ret_list.append(item)
                else:
                    pass
        return ret_list


    def get_board_list(self):
        ret_list = []
        for item in self.cfg.items():
            ret_list.append(item[0])
        return ret_list

    def get_board_entry(self, board):
        # boards = self.get_board_list()
        if board not in self.cfg:
            raise InvalidOptionException()
        else:
            return self.cfg[board]

    def get_rev_list(self, board):
        ret_list = []
        board_info = self.get_board_entry(board)
        for info_entry in board_info.items():
            if ((info_entry[0] == self.rev_string) and (info_entry[1] is not None)):
                for k, v in self.cfg[board][self.rev_string].items():
                    ret_list.append(k)
                return ret_list
        print("No revision entries found for {}".format(board))
        return None

    def get_rev_entry(self, board, rev):
        if self.rev_string not in self.cfg[board]:
            print("Couldn't find board {} in configuration file: {}.".format(board, self.cfg_filename))
            return None
            # raise invalidOptionException
        elif ((self.cfg[board][self.rev_string] is None) or (rev not in self.cfg[board][self.rev_string])):
            print("Couldn't find revision {} for board {} in current configuration file: {}.".format(rev, board,
                                                                                                     self.cfg_filename))
            return None
            # raise invalidOptionException
        else:
            return self.cfg[board][self.rev_string][rev]

    def get_test_location(self, board):
        board_info = self.get_board_entry(board)
        return os.path.abspath(board_info[self.testloc_str])

    def get_command_string(self, board, rev=None, include_opts=False):
        board_info = self.get_board_entry(board)
        ret_str = board_info[self.base_cmd_str]
        #Some boards may not include a revision number.
        if rev is not None:
            try:
                rev_info = self.get_rev_entry(board, rev)
                if (self.testfile_str in rev_info) and (rev_info[self.testfile_str] is not None):
                    ret_str += (" " + rev_info[self.testfile_str])
            except:
                print("Couldn't find revision {} in entry {}. Running without revision option.".format(rev, board))
        if include_opts:
            # TODO: this is broken and I don't know why.
            if ((self.req_opt_str in rev_info) and (rev_info[self.req_opt_str] is not (None or "None"))):
                ret_str += (" " + rev_info[self.req_opt_str])
        return ret_str.rstrip()


class TestRunner:
    def __init__(self, config_obj: TestsParse):
        self.config = config_obj
        self.config_filname = config_obj.cfg_filename

    def get_info(self, board, rev):
        board_entry = self.config.get_board_entry(board)
        rev_entry = self.config.get_rev_entry(board, rev)
        return board_entry, rev_entry
        # print(self.config.get_board_entry(board))
        # print(self.config.get_rev_entry(board, rev))

    def run_test(self, board, rev=None):
        input_char = ''
        while input_char != ('y' or 'Y'):
            print("Selected test: {}, rev: {}. Continue? (y/n)".format(board, str(rev)))
            # start loop to except invalid inputs from window resizing.
            while True:
                try:
                    input_char = getch.getch()
                    break
                except OverflowError as e:
                    continue
            if input_char == ('n' or 'N'):
                return
            elif input_char != ('y' or 'Y'):
                print("Please enter 'y' or 'n'.")

        og_dir = os.getcwd()
        test_dir = self.config.get_test_location(board)
        test_command_string = self.config.get_command_string(board, rev=rev)

        os.chdir(test_dir)
        while True:
            try:
                subprocess.check_call(test_command_string.split())
                # subprocess.check_call(test_command_string, shell=True) #No reason to run this the insecure way...
            except Exception as e:
                print(e)
            print("Process Finished. Press 'r' to rerun, any key to continue.\n")
            #TODO: These are not safe from window resizing. Look at fixing that.
            # except overflow error to allow window resizing.
            got_char = None
            while got_char is None:
                try:
                    got_char = getch.getch()
                except OverflowError as e:
                    continue
            if got_char == ('r' or 'R'):
                continue
            else:
                break
        os.chdir(og_dir)


if __name__ == "__main__":
    print("testrun.py not meant to be run as main.")
