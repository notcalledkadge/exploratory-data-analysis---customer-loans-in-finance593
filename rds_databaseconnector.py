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
  
    def ignition_switch(self):
        try:
            connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string)
            print("Engine initialized successfully.")
        except Exception as e:
            print(f"Error initializing engine: {e}")
  
    def extract_data(self, query: str) -> pd.DataFrame:
        if self.engine is None:
            raise ValueError("The engine is not initialized. Call ignition_switch() first.")
        
        try:
            with self.engine.connect() as connection:
                data = pd.read_sql_query(query, connection)
                print("Data extracted successfully.")
                return data
        except Exception as e:
            print(f"Error extracting data: {e}")
            return pd.DataFrame()

    def save_data_to_csv(self, data: pd.DataFrame, file_path: str):
        try:
            data.to_csv(file_path, index=False)
            print(f"Data saved to CSV successfully at {file_path}.")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")


if __name__ == "__main__":
  credentials_path = "/Users/ks/exploratory_data_analysis/credentials.yaml"
  query = "SELECT * FROM loan_payments" 
  output_csv_path = "/Users/ks/exploratory_data_analysis/output_data/original_output_data.csv"

  credentials = load_credentials(credentials_path)
  rds_connector = RDSDatabaseConnector(credentials)
  rds_connector.ignition_switch()
  data = rds_connector.extract_data(query)
  if data is not None:
   rds_connector.save_data_to_csv(data, output_csv_path)


