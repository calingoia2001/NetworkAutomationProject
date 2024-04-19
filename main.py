# !/usr/bin/env python
import os

from simple_term_menu import TerminalMenu
from colorama import Back, Style
# import subprocess


def menu_gui():
    main_menu_title = 10 * '*' + Back.CYAN + " 'Network automation of a GNS3 topology using Python' " + Style.RESET_ALL+ 10 * '*' + "\n"
    main_menu_exit = False
    options = ["option1", "option2", "option3", "quit"]  # Define menu options
    menu = TerminalMenu(menu_entries=options, title=main_menu_title)  # Create menu object

    op1_menu_title = 10 * '*' + Back.CYAN + " 'Option 1' " + Style.RESET_ALL+ 10 * '*' + "\n"
    op1_menu_items = ["option 1", "back"]
    op1_menu_back = False
    op1_menu = TerminalMenu(menu_entries=op1_menu_items, title=op1_menu_title)

    op2_menu_title = 10 * '*' + Back.CYAN + " 'Option 2' " + Style.RESET_ALL+ 10 * '*' + "\n"
    op2_menu_items = ["option 2", "back"]
    op2_menu_back = False
    op2_menu = TerminalMenu(menu_entries=op2_menu_items, title=op2_menu_title)

    op3_menu_title = 10 * '*' + Back.CYAN + " 'Option 3' " + Style.RESET_ALL+ 10 * '*' + "\n"
    op3_menu_items = ["option 3", "back"]
    op3_menu_back = False
    op3_menu = TerminalMenu(menu_entries=op3_menu_items, title=op3_menu_title)

    while not main_menu_exit:
        os.system('clear')
        main_selector = menu.show()
        if main_selector == 0:
            while not op1_menu_back:
                os.system('clear')
                op1_selector = op1_menu.show()
                if op1_selector == 0:
                    print("\n Option 1 has been selected")
                elif op1_selector == 1:
                    op1_menu_back = True
                    print("\n Back selected")
            op1_menu_back = False
        elif main_selector == 1:
            while not op2_menu_back:
                os.system('clear')
                op2_selector = op2_menu.show()
                if op2_selector == 0:
                    print("\n Option 2 has been selected")
                elif op2_selector == 1:
                    op2_menu_back = True
                    print("\n Back selected")
            op2_menu_back = False
        elif main_selector == 2:
            while not op3_menu_back:
                os.system('clear')
                op3_selector = op3_menu.show()
                if op3_selector == 0:
                    print("\n Option 3 has been selected")
                elif op3_selector == 1:
                    op3_menu_back = True
                    print("\n Back selected")
            op3_menu_back = False
        elif main_selector == 3:
            main_menu_exit = True
            print("\n Quitted")


if __name__ == '__main__':
    menu_gui()
