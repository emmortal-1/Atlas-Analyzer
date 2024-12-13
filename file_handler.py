import data_frame_operations
import csv_analyzer
import file_selector
import pandas as pd

class FileHandler:
    def __init__(self):
        self.df = None
        self.file_path = None

    def load_csv(self, file_path):
        """
        Load a CSV file into a pandas DataFrame.
        
        Args:
            file_path (str): Path to the CSV file to be loaded
            
        Returns:
            bool: True if file loaded successfully, False otherwise
            
        Raises:
            Exception: Prints error message if file loading fails
        """
        try:
            self.file_path = file_path  # Store the file path
            self.df = pd.read_csv(file_path)  # Load the CSV into self.df
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def export_processed_data(self, output_path):
        """
        Export the current DataFrame to a CSV file.
        
        Args:
            output_path (str): Path where the CSV file should be saved
            
        Returns:
            str: Success message with output path or error message if no data to export
        """
        if self.df is None:
            return "No data to export"
        self.df.to_csv(output_path, index=False)
        return f"Data exported to {output_path}"
