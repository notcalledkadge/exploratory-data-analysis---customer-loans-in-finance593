import pandas as pd

class DataTransform:
    
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def convert_to_numeric(self, columns: list):
        """
        Convert specified columns to numeric type.
        
        Parameters:
        - columns (list): List of column names to convert.
        """
        for column in columns:
            if column in self.data.columns:
                self.data[column] = pd.to_numeric(self.data[column], errors='coerce')
                print(f"Converted column '{column}' to numeric type.")
            else:
                print(f"Column '{column}' does not exist in the DataFrame. Available columns: {self.data.columns.tolist()}")

    def convert_to_datetime(self, columns: list, date_format: str = '%Y-%m-%d'):
        """
        Convert specified columns to datetime type.
        
        Parameters:
        - columns (list): List of column names to convert.
        - date_format (str, optional): Format of the date strings. Default is '%Y-%m-%d'.
        """
        for column in columns:
            if column in self.data.columns:
                self.data[column] = pd.to_datetime(self.data[column], format=date_format, errors='coerce')
                print(f"Converted column '{column}' to datetime type.")
            else:
                print(f"Column '{column}' does not exist in the DataFrame. Available columns: {self.data.columns.tolist()}")

    def convert_to_categorical(self, columns: list):
        """
        Convert specified columns to categorical type.
        
        Parameters:
        - columns (list): List of column names to convert.
        """
        for column in columns:
            if column in self.data.columns:
                self.data[column] = self.data[column].astype('category')
                print(f"Converted column '{column}' to categorical type.")
            else:
                print(f"Column '{column}' does not exist in the DataFrame. Available columns: {self.data.columns.tolist()}")

    def clean_symbols(self, columns: list, symbols: list):
        """
        Clean specified columns by removing specified symbols.
        
        Parameters:
        - columns (list): List of column names to clean.
        - symbols (list): List of symbols (strings) to remove from each column.
        """
        for column in columns:
            if column in self.data.columns:
                for symbol in symbols:
                    self.data[column] = self.data[column].str.replace(symbol, '', regex=False)
                print(f"Removed symbols '{symbols}' from column '{column}'.")
            else:
                print(f"Column '{column}' does not exist in the DataFrame. Available columns: {self.data.columns.tolist()}")
    
    def get_transformed_data(self) -> pd.DataFrame:
        """
        Return the transformed DataFrame.
        """
        return self.data

    def list_columns(self):
        """
        Print the list of columns in the DataFrame.
        """
        print("Columns in the DataFrame:")
        print(self.data.columns.tolist())