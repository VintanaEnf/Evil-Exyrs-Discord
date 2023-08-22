import os
import sys

#This script will contain important etcetera functions for code readability in the main function.
def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows
    else:
        os.system('clear')

