from pathlib import Path

class FileSelector:
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

    def select_csv_file(self, file_handler):
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
            
            if file_handler.load_csv(file_path):
                return True
            print("Please try again with a valid CSV file.")
