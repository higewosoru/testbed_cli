'''
The frontend of the testserver gui.
'''

import curses

AUTHOR = "Sol O."
OPT_SELECTED_DELAYMS = 1000


class MenuItem:
    def __init__(self, name: str, x_pos, y_pos, initial_text=" ", final_text="    ->"):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.initial_text = initial_text
        self.final_text = final_text

    def get_title_str(self, uppercase=True):
        ret_val = ""
        if self.initial_text is not None:
            ret_val += self.initial_text

        if uppercase:
            ret_val += self.name.upper()
        else:
            ret_val += self.name

        if self.final_text is not None:
            ret_val += self.final_text
        return ret_val


class GUI:
    def __init__(self, testrunner=None, testing=True):  # modified for our purposes.
        # def __init__(self, testing=True):     #This is the generic one.
        if testing is True:
            print("Starting GUI in testing mode.")
        self.testing = testing
        self.testrunner = testrunner

        self.board_list = []
        self.rev_list = []
        # allow the option to include config file while testing. Should throw an error if no config file specified in normal mode.
        if ((self.testing is True) and (self.testrunner is None)):
            # fake values for easy testing.
            self.config_file = "Testing"
            self.board_list = ['fake1', 'fake2', 'fake3', 'fake4', 'fake5']
            self.rev_list = ['REV1', 'REV2', 'REV3', 'REV4', 'REV5', 'REV6'] # NOTE: This is not how this normally works.... will not be a single, static list but a list per board above.
        else:
            self.config_file = self.testrunner.config.cfg_filename
            self.board_list = self.testrunner.config.get_board_list()

        self.height = 0  # MUST be set with stdscr.getmaxyx() in gui_init()
        self.width = 0  # MUST be set with stdscr.getmaxyx() in gui_init()
        self.page_name = "GUI"

        # These should be adjusted to reflect other GUI elements such as the title bar, etc.
        self.const_maxX = 0
        self.const_maxY = 1
        # Same as above... must also be added to const_min/Y once the maxX/Y is obtained each frame.
        self.const_lowerXoffset = 1
        self.const_lowerYoffset = -2

        self.volatile_minX = self.width  # must also be set on getting max XY
        self.volatile_minY = self.height  # must also be set on getting max XY.

        self.cursor_x = self.const_maxX  # This shoudln't change at all. L/R keystrokes move up and down menus.
        self.cursor_y = self.const_maxY

        self.title = "Should be set by gui_refresh()"
        self.subtitle = "Should be set by gui_refresh()"
        self.statusbarstr = "Should be set by gui_refresh()"

    def load_list_elements(self, element_list: list, initial_text="  ", final_text=None):
        '''takes a list of strings and turns them into a list of MenuItem instances,
        starts at topmost available y value and moves down, aligned '''
        counter = 0
        ret_list = []
        for item in element_list:
            ret_list.append(MenuItem(item, self.const_maxX, (self.const_maxY + counter), initial_text=initial_text, final_text=final_text))
            counter += 1
        return ret_list

    def gui_refresh(self, stdscr):
        # Initialization
        stdscr.clear()
        self.height, self.width = stdscr.getmaxyx()
        self.volatile_minX = self.width + self.const_lowerXoffset
        self.volatile_minY = self.height + self.const_lowerYoffset

        # standard page strings and header text
        self.title = "BSI Testbed {}".format(self.page_name)[:self.width - 1]
        self.subtitle = "Written by {}".format(AUTHOR)[:self.width - 1]
        self.statusbarstr = "Press 'q' to exit | STATUS BAR | Configuration: {}".format(self.config_file)[
                            :self.width - 1]

    """
    Must refresh GUI before drawing common elements to ensure the window size hasn't changed.
    """
    def draw_common_elements(self, stdscr):
        # Centering calculations
        start_x_title = int((self.width // 2) - (len(self.title) // 2) - len(self.title) % 2)
        start_x_subtitle = int((self.width // 2) - (len(self.subtitle) // 2) - len(self.subtitle) % 2)
        # start_y_title = int((self.height // 2) - 2)
        start_y_title = int(0)

        # Render status bar
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(self.height - 1, 0, self.statusbarstr)
        stdscr.addstr(self.height - 1, len(self.statusbarstr), " " * (self.width - len(self.statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(2))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(3))
        stdscr.attron(curses.A_BOLD)
        # Rendering title
        stdscr.addstr(start_y_title, start_x_title, self.title)
        # Render bar before title
        stdscr.addstr(start_y_title, 0, " " * (((self.width - len(self.title)) // 2) - 1))
        # Render bar after title
        stdscr.addstr(start_y_title, (start_x_title + len(self.title)), " " * (((self.width - len(self.title)) // 2) - 0))
        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(3))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        # stdscr.addstr(start_y_title + 1, start_x_subtitle, self.subtitle)
        # stdscr.addstr(start_y_title + 3, (self.width // 2) - 2, '-' * 4)
        # stdscr.addstr(start_y_title + 5, start_x_keystr, keystr)
        # stdscr.addstr(start_y_title + 6, (width // 2), l_r_str)
        stdscr.move(self.cursor_y, self.cursor_x)

    def draw_menu(self, list_of_elements, stdscr):
        """Once an  element list has been parsed by load_menu_items(), use draw_menu_items()
        to draw the menu items from the created MenuItem instances"""
        stdscr.attron(curses.color_pair(1))
        for item in list_of_elements:
            if self.cursor_y == item.y_pos:
                stdscr.attroff(curses.color_pair(1))
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(item.y_pos, item.x_pos, (item.get_title_str() + (" " * (self.width - len(item.get_title_str())))))
                #stdscr.addnstr(item.y_pos, item.x_pos, (item.get_title_str() + (" " * (self.width - len(item.get_title_str())))))
                stdscr.attroff(curses.color_pair(2))
                stdscr.attron(curses.color_pair(1))
            else:
                stdscr.addstr(item.y_pos, item.x_pos, (item.get_title_str() + (" " * (self.width - len(item.get_title_str())))))
        stdscr.attroff(curses.color_pair(1))

    def test_menu_enter_handler(self, stdscr, name):
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(self.volatile_minY, 0, "Selected IteM: {}".format(name))
        stdscr.attroff(curses.color_pair(1))

    def main_menu_enter_handler(self, stdscr, name):
        # only accept no testrunner if testing is set to true.
        if (self.testing is True) and (self.testrunner is None):
            self.sub_menu(stdscr, name, self.rev_list)
        else:
            revs = self.testrunner.config.get_rev_list(name)
            # get_rev_list will return None if there's no revisions in the yaml file.
            if revs is None:
                revs = ["No board revisions found."]
            self.sub_menu(stdscr, name, revs)

    def board_menu_enter_handler(self, stdscr, name):
        if (self.testing is True):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(self.volatile_minY, 0, "Selected IteM: {}".format(name))
            stdscr.attroff(curses.color_pair(1))
        else:
            return name

# TODO: the status messages printed here are not ideal. need to make sure the formatting makes sense.
    def menu_enter(self, stdscr, current_menu_items, enter_handler):
        for item in current_menu_items:
            if item.y_pos == self.cursor_y:
                return item.name, enter_handler(stdscr, item.name)
            else:
                continue
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(self.volatile_minY, 0, "Nothing selected!")
        stdscr.attroff(curses.color_pair(1))

    def sub_menu(self, stdscr, name, menu_element_list):
        self.page_name = name
        parent_item = name
        k = 0
        flag_back = False
        flag_fwd = False
        self.cursor_x = self.const_maxX
        self.cursor_y = self.const_maxY

        self.gui_refresh(stdscr)
        self.draw_common_elements(stdscr)
        self.statusbarstr = "Press the 'back' arrow twice to go back | STATUS BAR | Configuration: {}".format(self.testrunner.config.cfg_filename)[
                            :self.width - 1]

        current_menu_items = self.load_list_elements(menu_element_list, initial_text="  - ", final_text="       | |")

        while (k != curses.KEY_LEFT):

            flag_back = False
            flag_fwd = False

            if k == curses.KEY_LEFT:
                #curses.flash()
                flag_back = True
            elif k == ord('q'):
                quit()
            elif k == curses.KEY_RIGHT:
                flag_fwd = True
                #stdscr.attron(curses.color_pair(1))
                #stdscr.addstr(int((self.height / 2 + 3)), 0, "Right key pressed")
                #stdscr.attroff(curses.color_pair(1))
            elif k == curses.KEY_DOWN:
                self.cursor_y = self.cursor_y + 1
            elif k == curses.KEY_UP:
                self.cursor_y = self.cursor_y - 1

            # check new coordinates against designated max/min values
            self.cursor_x = max(self.const_maxX, self.cursor_x)
            self.cursor_x = min(self.volatile_minX, self.cursor_x)

            self.cursor_y = max(self.const_maxY, self.cursor_y)
            self.cursor_y = min(self.volatile_minY, self.cursor_y)

            self.gui_refresh(stdscr)
            self.statusbarstr = "Press the 'back' arrow to go back | Press 'q' to Quit. | Configuration: {}".format(
                self.config_file)[:self.width - 1]
            self.draw_menu(current_menu_items, stdscr)
            self.draw_common_elements(stdscr)

            if flag_back is True:
                return
            if flag_fwd is True:
                if self.testing is True:
                    self.menu_enter(stdscr, current_menu_items, self.test_menu_enter_handler)
                else:
                    #TODO: this is sus. Make sure it works with boards with no revision.
                    #stdscr.clear()
                    revtup = (self.menu_enter(stdscr, current_menu_items, self.board_menu_enter_handler))
                    try:
                        rev = revtup[0] # have to do this because menu_enter will return a tuple in this case.
                    except:
                        rev = None
                    if rev is not None:
                        stdscr.erase()
                        stdscr.attron(curses.color_pair(1))
                        selected_opt_msg = "Selected board: {}, rev: {}".format(parent_item, str(rev))
                        stdscr.addstr(self.height//2, ((self.width//2) - (len(selected_opt_msg)//2)), selected_opt_msg)
                        stdscr.attroff(curses.color_pair(1))
                        stdscr.refresh()
                        curses.delay_output(OPT_SELECTED_DELAYMS)
                        curses.endwin()
                        #stdscr.clear()
                        #stdscr.refresh()
                        self.testrunner.run_test(parent_item, rev)

                        self.gui_refresh(stdscr)
                        self.statusbarstr = "Press the 'back' arrow to go back | Press 'q' to Quit. | Configuration: {}".format(
                            self.config_file)[:self.width - 1]
                        self.draw_menu(current_menu_items, stdscr)
                        self.draw_common_elements(stdscr)
                """stdscr.attron(curses.color_pair(1))
                stdscr.addstr(int((self.height - 3)), 0, "Right key pressed")
                stdscr.attroff(curses.color_pair(1))"""

            # Refresh the screen
            stdscr.refresh()
            # Wait for next input
            k = stdscr.getch()

    def main_menu(self, stdscr):
        self.page_name = "Main Menu"
        k = 0
        flag_back = False
        flag_fwd = False
        self.cursor_x = self.const_maxX
        self.cursor_y = self.const_maxY

        self.gui_refresh(stdscr)
        self.draw_common_elements(stdscr)

        element_list = self.load_list_elements(self.board_list, final_text="           -->")

        while (k != ord('q')):
            self.page_name = "Main Menu"
            flag_back = False
            flag_fwd = False

            if k == curses.KEY_LEFT:
                #curses.flash()
                flag_back = True
            elif k == curses.KEY_RIGHT:
                flag_fwd = True
                #stdscr.attron(curses.color_pair(1))
                #stdscr.addstr(int((self.height / 2 + 3)), 0, "Right key pressed")
                #stdscr.attroff(curses.color_pair(1))
            elif k == curses.KEY_DOWN:
                self.cursor_y = self.cursor_y + 1
            elif k == curses.KEY_UP:
                self.cursor_y = self.cursor_y - 1

            # check new coordinates against designated max/min values
            self.cursor_x = max(self.const_maxX, self.cursor_x)
            self.cursor_x = min(self.volatile_minX, self.cursor_x)

            self.cursor_y = max(self.const_maxY, self.cursor_y)
            self.cursor_y = min(self.volatile_minY, self.cursor_y)

            self.gui_refresh(stdscr)
            self.draw_menu(element_list, stdscr)
            self.draw_common_elements(stdscr)

            if flag_back is True:
                curses.flash()
            if flag_fwd is True:
                self.menu_enter(stdscr, element_list, self.main_menu_enter_handler)
                """stdscr.attron(curses.color_pair(1))
                stdscr.addstr(int((self.height - 3)), 0, "Right key pressed")
                stdscr.attroff(curses.color_pair(1))"""

            # Refresh the screen
            stdscr.refresh()
            # Wait for next input
            k = stdscr.getch()

    def init_gui(self, stdscr):
        self.width, self.height = stdscr.getmaxyx()

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) # background/list item color
        #curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # old
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE) # Status bar/selected item color
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLUE) # title color

        self.main_menu(stdscr)

    def start_gui(self):
        curses.wrapper(self.init_gui)


if __name__ == "__main__":
    app = GUI()
    app.start_app()
