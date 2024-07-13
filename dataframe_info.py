import pandas as pd
class DataFrameInfo:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def describe_columns(self):
        """Describe all columns in the DataFrame to check their data types and summary statistics."""
        print("Describing columns:")
        description = self.df.describe(include='all')
        print(description)
        return description

    def extract_statistics(self):
        """Extract statistical values: median, standard deviation and mean from the DataFrame."""
        statistics = {
            'mean': self.df.mean(numeric_only=True),
            'median': self.df.median(numeric_only=True),
            'std': self.df.std(numeric_only=True)
        }
        print("Extracting statistics:")
        for stat, values in statistics.items():
            print(f"{stat.capitalize()}:\n{values}\n")
        return statistics

    def count_distinct_values(self):
        """Count distinct values in categorical columns."""
        categorical_columns = self.df.select_dtypes(include=['object', 'category']).columns
        distinct_counts = {col: self.df[col].nunique() for col in categorical_columns}
        print("Counting distinct values in categorical columns:")
        for col, count in distinct_counts.items():
            print(f"{col}: {count}")
        return distinct_counts

    def print_shape(self):
        """Print out the shape of the DataFrame."""
        shape = self.df.shape
        print(f"Shape of DataFrame: {shape}")
        return shape

    def count_null_values(self):
        """Generate a count/percentage count of NULL values in each column."""
        null_counts = self.df.isnull().sum()
        null_percentages = (self.df.isnull().sum() / len(self.df)) * 100
        null_info = pd.DataFrame({'count': null_counts, 'percentage': null_percentages})
        print("Count and percentage of NULL values in each column:")
        print(null_info)
        return null_info

    def summary(self):
        """Print a summary of the DataFrame including shape, null value info, and column descriptions."""
        print("DataFrame Summary:")
        self.print_shape()
        null_info = self.count_null_values()
        description = self.describe_columns()
        return {'shape': self.df.shape, 'null_info': null_info, 'description': description}