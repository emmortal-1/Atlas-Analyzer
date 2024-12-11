import pandas as pd
import numpy as np
from pathlib import Path
import sys  # For sys.exit()

"""
   Class to analyze CSV files using pandas DataFrame.
"""
class CSVAnalyzer:
   # Initialize the class with no data
   def __init__(self):
       self.df = None  # df is the DataFrame, initialized as None
       self.file_path = None  # file_path stores the CSV path
   
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
       
   def get_basic_info(self):
       """
       Retrieve basic information about the loaded dataset.
       
       Returns:
           dict: Dictionary containing:
               - rows: Number of rows in the dataset
               - columns: List of column names
               - data_types: Dictionary of column data types
               - missing_values: Dictionary of null count per column
           str: Error message if no data is loaded
       """
       if self.df is None:
           return "No data loaded"
       info = {
           "rows": len(self.df),
           "columns": list(self.df.columns),
           "data_types": self.df.dtypes.to_dict(),
           "missing_values": self.df.isnull().sum().to_dict()
       }
       return info
   
   def sort_by_column(self, column, ascending=True, num_rows=5):
       """
       Sort the dataset by a specified column.
       
       Args:
           column (str): Name of the column to sort by
           ascending (bool, optional): Sort order. Defaults to True
           num_rows (int, optional): Number of rows to display. Defaults to 5
           
       Returns:
           DataFrame: Sorted DataFrame
           str: Error message if column not found
       """
       if column not in self.df.columns:
           return None
       self.df = self.df.sort_values(by=column, ascending=ascending)
       return self.df.head(num_rows)
   
   def filter_by_value(self, column, value):
       """
       Filter the dataset to rows where the specified column matches the given value.
       
       Args:
           column (str): Name of the column to filter on
           value: Value to filter by (type should match column data type)
           
       Returns:
           DataFrame: Filtered DataFrame containing only matching rows
           str: Error message if column not found
       """
       if column not in self.df.columns:
           return f"Column '{column}' not found"
       return self.df[self.df[column] == value]
   
   def get_column_categories(self, column):
       """
       Get list of unique values in a specified column.
       
       Args:
           column (str): Name of the column to get unique values from
           
       Returns:
           list: List of unique values in the column
           str: Error message if column not found
       """
       if column not in self.df.columns:
           return f"Column '{column}' not found"
       return self.df[column].unique().tolist()
   
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
   
   def get_available_csv_files(self):
       """
       Scan current directory and subdirectories for CSV files.
       
       Returns:
           list: List of strings containing relative paths to all CSV files found
               Returns empty list if no CSV files are found
       """
       current_dir = Path.cwd()  # Get current working directory
       csv_files = list(current_dir.glob('**/*.csv'))  # Recursively find all CSV files
       
       if not csv_files:
           return []
       return [str(f.relative_to(current_dir)) for f in csv_files]
   
   def select_csv_file(self):
       """
       Interactive loop for selecting a CSV file from available files or by path.
       
       Returns:
           bool: True if file was successfully loaded, False if user quits
       """
       csv_files = self.get_available_csv_files()
       
       while True:
           if csv_files:
               print("\nAvailable CSV files:")
               for i, file in enumerate(csv_files, 1):
                   print(f"{i}. {file}")
               print("\nEnter file number or full path to another CSV file")
               file_path = input("(or 'quit' to exit): ")
               
               if file_path.lower() == 'quit':
                   print("================")
                   print("Thank you for using Atlas File Analyzer!")
                   return False
               
               # Check if user entered a number
               try:
                   file_idx = int(file_path) - 1
                   if 0 <= file_idx < len(csv_files):
                       file_path = csv_files[file_idx]
               except ValueError:
                   pass  # User entered a path directly
           else:
               print("\nNo CSV files found in the current directory.")
               file_path = input("Enter the path to your CSV file (or 'quit' to exit): ")
               if file_path.lower() == 'quit':
                   return False
           
           if self.load_csv(file_path):
               return True
           print("Please try again with a valid CSV file.")
   
   def add_column(self, column_name, default_value=None):
       """
       Add a new column to the DataFrame.
       
       Args:
           column_name (str): Name of the new column
           default_value: Default value for the new column (optional)
           
       Returns:
           str: Success or error message
       """
       if self.df is None:
           return "No data loaded"
       if column_name in self.df.columns:
           return f"Column '{column_name}' already exists"
       
       self.df[column_name] = default_value
       return f"Column '{column_name}' added successfully"
   
   def remove_column(self, column_name):
       """
       Remove a column from the DataFrame.
       
       Args:
           column_name (str): Name of the column to remove
           
       Returns:
           str: Success or error message
       """
       if self.df is None:
           return "No data loaded"
       if column_name not in self.df.columns:
           return f"Column '{column_name}' not found"
       
       self.df = self.df.drop(columns=[column_name])
       return f"Column '{column_name}' removed successfully"
   
   def add_row(self, row_data):
       """
       Add a new row to the DataFrame.
       
       Args:
           row_data (dict): Dictionary with column names as keys and values for the new row
           
       Returns:
           str: Success or error message
       """
       if self.df is None:
           return "No data loaded"
       
       try:
           self.df = pd.concat([self.df, pd.DataFrame([row_data])], ignore_index=True)
           return "Row added successfully"
       except Exception as e:
           return f"Error adding row: {e}"
   
   def remove_row(self, index):
       """
       Remove a row from the DataFrame by index.
       
       Args:
           index (int): Index of the row to remove
           
       Returns:
           str: Success or error message
       """
       if self.df is None:
           return "No data loaded"
       
       try:
           if 0 <= index < len(self.df):
               self.df = self.df.drop(index=index).reset_index(drop=True)
               return f"Row at index {index} removed successfully"
           return f"Index {index} out of range"
       except Exception as e:
           return f"Error removing row: {e}"
   
   def run_command_prompt(self):
       """
       Run an interactive command prompt for analyzing CSV data.
       """
       # Print the title of the program
       print("Atlas File Analyzer")
       print("================")
       
       # Select and load CSV file
       if not self.select_csv_file():
           sys.exit()
       
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

           if choice == "1":
               info = self.get_basic_info()
               print("\nDataset Information:")
               for key, value in info.items():
                   print(f"{key}: {value}")
           
           elif choice == "2":
               while True:
                   print("\nAvailable columns:")
                   for i, col in enumerate(self.df.columns, 1):
                       print(f"{i}. {col}")
                       
                   column = input("\nEnter column name or number to sort by (or 'back' to return to menu): ")
                       
                   if column.lower() == 'back':
                       break
                       
                   # Handle column selection by number
                   try:
                       if column.isdigit():
                           col_idx = int(column) - 1
                           if 0 <= col_idx < len(self.df.columns):
                               column = self.df.columns[col_idx]
                           else:
                               print("Invalid column number. Please try again.")
                               continue
                   except ValueError:
                       pass
                       
                   if column not in self.df.columns:
                       print(f"Error: Column '{column}' not found. Please try again.")
                       continue
                       
                   order = input("Sort ascending? (y/n): ").lower() == 'y'
                       
                   try:
                       num_rows = int(input("How many rows to display? "))
                       if num_rows <= 0:
                           print("Number of rows must be positive. Using default (5 rows)")
                           num_rows = 5
                   except ValueError:
                       print("Invalid number of rows. Using default (5 rows)")
                       num_rows = 5
                       
                   result = self.sort_by_column(column, order, num_rows)
                   if result is not None:
                       print(f"\nSorted data (first {num_rows} rows):")
                       print(result)
                       break
                   else:
                       print("An error occurred while sorting. Please try again.")
           
           elif choice == "3":
               while True:
                   print("\nAvailable columns:")
                   for i, col in enumerate(self.df.columns, 1):
                       print(f"{i}. {col}")
                       
                   column = input("\nEnter column name or number to filter by (or 'back' to return to menu): ")
                       
                   if column.lower() == 'back':
                       break
                       
                   # Handle column selection by number
                   try:
                       if column.isdigit():
                           col_idx = int(column) - 1
                           if 0 <= col_idx < len(self.df.columns):
                               column = self.df.columns[col_idx]
                           else:
                               print("Invalid column number. Please try again.")
                               continue
                   except ValueError:
                       pass
                       
                   if column not in self.df.columns:
                       print(f"Error: Column '{column}' not found. Please try again.")
                       continue
                       
                   # Show unique values in the selected column
                   unique_values = self.df[column].unique()
                   print(f"\nUnique values in '{column}':")
                   for i, val in enumerate(unique_values, 1):
                       print(f"{i}. {val}")
                       
                   value = input("\nEnter value to filter for: ")
                   result = self.filter_by_value(column, value)
                       
                   if isinstance(result, str):  # Error message
                       print(f"Error: {result}")
                       continue
                       
                   if len(result) == 0:
                       print(f"No rows found matching '{value}' in column '{column}'")
                       continue
                       
                   print("\nFiltered data (first 5 rows):")
                   print(result.head())
                   break
           
           elif choice == "4":
               while True:
                   print("\nAvailable columns:")
                   for i, col in enumerate(self.df.columns, 1):
                       print(f"{i}. {col}")
                       
                   column = input("\nEnter column name or number (or 'back' to return to menu): ")
                       
                   if column.lower() == 'back':
                       break
                       
                   # Handle column selection by number
                   try:
                       if column.isdigit():
                           col_idx = int(column) - 1
                           if 0 <= col_idx < len(self.df.columns):
                               column = self.df.columns[col_idx]
                           else:
                               print("Invalid column number. Please try again.")
                               continue
                   except ValueError:
                       pass
                       
                   categories = self.get_column_categories(column)
                   if isinstance(categories, str):  # Error message
                       print(f"Error: {categories}")
                       continue
                       
                   print(f"\nCategories in {column}:")
                   for i, cat in enumerate(categories, 1):
                       print(f"{i}. {cat}")
                   break
           
           elif choice == "5":
               output_path = input("Enter name of new CSV file (include .csv): ")
               result = self.export_processed_data(output_path)
               print(result)
           
           elif choice == "6":
               column_name = input("Enter new column name: ")
               default_value = input("Enter default value (press Enter for None): ")
               default_value = None if default_value == "" else default_value
               result = self.add_column(column_name, default_value)
               print(result)
           
           elif choice == "7":
               while True:
                   print("\nAvailable columns:")
                   for i, col in enumerate(self.df.columns, 1):
                       print(f"{i}. {col}")
                       
                   column_name = input("\nEnter column name or number to remove (or 'back' to return to menu): ")
                       
                   if column_name.lower() == 'back':
                       break
                       
                   # Handle column selection by number
                   try:
                       if column_name.isdigit():
                           col_idx = int(column_name) - 1
                           if 0 <= col_idx < len(self.df.columns):
                               column_name = self.df.columns[col_idx]
                           else:
                               print("Invalid column number. Please try again.")
                               continue
                   except ValueError:
                       pass
                       
                   # Confirm deletion
                   confirm = input(f"Are you sure you want to remove column '{column_name}'? (y/n): ")
                   if confirm.lower() != 'y':
                       print("Column removal cancelled.")
                       break
                       
                   result = self.remove_column(column_name)
                   print(result)
                   break
           
           elif choice == "8":
               while True:
                   print("\nEnter values for each column (or 'back' to return to menu):")
                   row_data = {}
                   
                   for column in self.df.columns:
                       value = input(f"{column}: ")
                       if value.lower() == 'back':
                           break
                       row_data[column] = value
                       
                   if 'back' in [v.lower() if isinstance(v, str) else v for v in row_data.values()]:
                       break
                       
                   if len(row_data) == len(self.df.columns):
                       result = self.add_row(row_data)
                       print(result)
                       
                       # Show preview of added row
                       if result == "Row added successfully":
                           print("\nPreview of added row:")
                           print(self.df.iloc[-1:])
                       break
           
           elif choice == "9":
               while True:
                   try:
                       print(f"\nValid row indices: 0 to {len(self.df) - 1}")
                       print("\nPreview of first and last 5 rows:")
                       print("\nFirst 5 rows:")
                       print(self.df.head())
                       print("\nLast 5 rows:")
                       print(self.df.tail())
                       
                       index = input("\nEnter row index to remove (or 'back' to return to menu): ")
                       
                       if index.lower() == 'back':
                           break
                           
                       index = int(index)
                       
                       # Show the row to be deleted and ask for confirmation
                       if 0 <= index < len(self.df):
                           print("\nRow to be deleted:")
                           print(self.df.iloc[index])
                           confirm = input("\nAre you sure you want to delete this row? (y/n): ")
                           if confirm.lower() != 'y':
                               print("Row deletion cancelled.")
                               break
                               
                           result = self.remove_row(index)
                           print(result)
                           break
                       else:
                           print(f"Error: Index must be between 0 and {len(self.df) - 1}")
                   except ValueError:
                        print("Error: Please enter a valid number")
           
           elif choice == "10":
               print("================")
               print("Thank you for using Atlas File Analyzer!")
               break
   