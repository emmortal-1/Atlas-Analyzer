import file_handler
import data_frame_operations
import file_selector
import sys

class CSVAnalyzer:
    def __init__(self):
        self.file_handler = file_handler()
        self.data_frame_ops = None  # Will be initialized after loading the CSV
        self.file_selector = file_selector()

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