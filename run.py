"""Runs all scripts"""

from src.view import view_main
from src.benchmark import stores_data_for_test
from system_info import system_info_main

if __name__ == "__main__":
    system_info_main()
    stores_data_for_test()    
    view_main()
