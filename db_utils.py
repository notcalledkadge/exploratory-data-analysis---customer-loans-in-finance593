"""
In order to be able to work with the database, we need to be able to read it. Hence the import here.
"""
import yaml
import pandas as pd
from sqlalchemy import create_engine


"""
Going back to using Dicts. 
This function will load the credentials found in the YAML file.
"""
def load_credentials(file_path:str)-> dict:
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    print("Credentials loaded successfully")    
    return credentials



"""
The RDS connector needed access to all of the credentials that were provided in the YAML folder for this project. 
The class handles all of the database connections and operations.
"""
class RDSDatabaseConnector:
  
  def __init__(self, credentials: dict):
      self.username = credentials.get('username')
      self.password = credentials.get('password')
      self.host = credentials.get('host')
      self.port = credentials.get('port')
      self.database = credentials.get('database')
      self.engine = None
      print("RDSDatabaseConnector initialized with credentials.")
  """
  The "ignition_switch" method is here to inialise the engine which connects this code to the selected database.
  """
  def ignition_switch(self):
    try:
        connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(connection_string)
        print("Engine initialized successfully.")
    except Exception as exception:
        print(f"Error initializing engine: {exception}")
  """
  Below is the method to extract data from the database.
  """
  def extract_data(self, query: str) -> pd.DataFrame:
        """
        Method to extract data from the database.
        """
        if self.engine is None:
            raise ValueError("The engine is not initialized. Call ignition_switch() first.")
        
        try:
            with self.engine.connect() as connection:
             data = pd.read_sql_query(query, connection)
             print("Data extracted successfully.")
             return data
        except Exception as e:
         print(f"Error extracting data: {e}")
        
  def save_data_as_csv(self,data: pd.DataFrame, file_path: str):
   try:
        data.to_csv(file_path, index=False)
        print(f"Data saved to CSV successfully at {file_path}.")
   except Exception as e:
        print(f"Error saving data to CSV: {e}")

class DataTransform:
    
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def convert_to_numeric(self, columns: list):
        """
        Convert specified columns to numeric types.
        
        Args:
        - columns (list): List of column names to convert.
        """
        for column in columns:
            self.data[column] = pd.to_numeric(self.data[column], errors='coerce')
        print(f"Converted columns {columns} to numeric types.")
    
    def convert_to_datetime(self, columns: list, date_format: str = None):
        """
        Convert specified columns to datetime types.
        
        Args:
        - columns (list): List of column names to convert.
        - date_format (str, optional): Date format to use for conversion. Defaults to None.
        """
        for column in columns:
            self.data[column] = pd.to_datetime(self.data[column], format=date_format, errors='coerce')
        print(f"Converted columns {columns} to datetime types.")
    
    def convert_to_categorical(self, columns: list):
        """
        Convert specified columns to categorical types.
        
        Args:
        - columns (list): List of column names to convert.
        """
        for column in columns:
            self.data[column] = self.data[column].astype('category')
        print(f"Converted columns {columns} to categorical types.")
    
    def clean_symbols(self, columns: list, symbols: str):
        """
        Remove specified symbols from the specified columns.
        
        Args:
        - columns (list): List of column names to clean.
        - symbols (str): String of symbols to remove.
        """
        for column in columns:
            for symbol in symbols:
                self.data[column] = self.data[column].str.replace(symbol, '', regex=False)
        print(f"Removed symbols {symbols} from columns {columns}.")
    
    def get_transformed_data(self) -> pd.DataFrame:
        """
        Return the transformed DataFrame.
        
        Returns:
        - data (pd.DataFrame): The transformed DataFrame.
        """
        return self.data
    
# if __name__ == "__main__":
#   credentials_path = "/Users/ks/exploratory_data_analysis/credentials.yaml"
#   query = "SELECT * FROM loan_payments" 
#   output_csv_path = "/Users/ks/exploratory_data_analysis/output_data.csv"

#   credentials = load_credentials(credentials_path)
#   rds_connector = RDSDatabaseConnector(credentials)
#   rds_connector.ignition_switch()
#   data = rds_connector.extract_data(query)
#   if data is not None:
#    rds_connector.save_data_as_csv(data, output_csv_path)


