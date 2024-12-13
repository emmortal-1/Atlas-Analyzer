import data_frame_operations
import file_handler
import file_selector
from csv_analyzer import CSVAnalyzer
import sys

def main():
    # Initialize the CSVAnalyzer class and run the command prompt
    analyzer = CSVAnalyzer()
    analyzer.run_command_prompt()

if __name__ == "__main__":
    main()
