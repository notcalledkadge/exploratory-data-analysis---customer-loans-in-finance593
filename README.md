### Exploratory Data Analysis - Customer Loans in Finance

#### Prerequisites:
> use 'pip install' for:
> - pandas
> - seaborn
> - numpy
> - matplotlib
> - scipy
> 

#### Contents:
- Milestone 2: 'rds_databaseconnector' contains the "RDSDatabaseConnector" class and "load_credentials" function that I created to complete this Milestone. "load_credentials" runs first, and pulls the required credentials from the .yaml that was provided. The "RDSDatabaseConnector" Class uses the loaded credentials to access the Data online and saves it as an accessible DataFrame for further use.
- Milestone 3: 'Milestone_3.ipynb' uses 'rds_databaseconnector', 'data_transform', 'dataframe_info' and 'dataframe_transform' to accomplish its functions. This Jupyter notebook begins by using the forementioned process to produce a DataFrame that is then transformed, cleaned up and then used to produced graphs. Along the way, four different versions of the DataFrame are produced which are at various levels of transformation. These are stored in the 'output_data' directory.
- Milestone 4: 'Milestone_4.ipynb' uses the 'original_output_data' file produced in Milestone 3 to produce some percentages and graphs based on the data pulled from the online directory. The purpose of this is assumedly to break down the data and analyse its characteristics. 