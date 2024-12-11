from file_handler import FileHandler
from data_frame_operations import DataFrameOperations
from file_selector import FileSelector
import sys

class CSVAnalyzer:
    def __init__(self):
        self.file_handler = FileHandler()
        self.data_frame_ops = None  # Will be initialized after loading the CSV
        self.file_selector = FileSelector()

    def run_command_prompt(self):
        """
        Run an interactive command prompt for analyzing CSV data.
        """
        # Print the title of the program
        print("Atlas File Analyzer")
        print("================")
        
        # Select and load CSV file
        if not self.file_selector.select_csv_file(self.file_handler):
            sys.exit()
        
        # Initialize DataFrameOperations with the loaded DataFrame
        self.data_frame_ops = DataFrameOperations(self.file_handler.df)

        # Print the options for the user
        while True:
            print("\nOptions:")
            print("1. Show basic information")
            print("2. Sort by column")
            print("3. Filter by value")
            print("4. Show column categories")
            print("5. Export processed data")
            print("6. Add column")
            print("7. Remove column")
            print("8. Add row")
            print("9. Remove row")
            print("10. Exit")
            
            choice = input("\nEnter your choice (1-10): ")
            # ... existing command handling code ...
