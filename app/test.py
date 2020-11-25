
from testrun.testrun import TestsParse, TestRunner

tests_info = TestsParse("testfile.yaml")
test = TestRunner(tests_info)


print(test.get_info("board1", "rev1"))
print(test.get_info("board3", "rev1"))

print(tests_info.get_test_location("board1"))
print(tests_info.get_command_string("board1", "rev1"))


test.run_test("board1", rev="rev1")
#test.run_test("board1", rev="rev2")
#test.run_test("board2")

#print(tests_info.cfg)
#boards = tests_info.get_board_list()
#print(boards)
#print(boards[0])
#print(tests_info.get_rev_list("board3"))
#print(tests_info.get_board_entry("board1"))
#print(tests_info.get_rev_entry("board1", "rev1"))