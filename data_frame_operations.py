import pandas as pd

class DataFrameOperations:
    def __init__(self, df):
        self.df = df

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
