import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore, skew,boxcox
from db_utils import RDSDatabaseConnector, load_credentials
from data_transform import DataTransform
from dataframe_info import DataFrameInfo


class Plotter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_null_values(self, title):
        """Plot the percentage of NULL values in each column."""
        null_counts = self.df.isnull().sum()
        null_percentages = (null_counts / len(self.df)) * 100

        plt.figure(figsize=(10, 6))
        null_percentages.plot(kind='bar', color='skyblue')
        plt.title(title)
        plt.xlabel('Columns')
        plt.ylabel('Percentage of NULL Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_skewed_columns(self, columns, title):
        """Plot histograms of skewed columns."""
        for col in columns:
            plt.figure(figsize=(10, 6))
            self.df[col].hist(bins=50)
            plt.title(f'{title}: {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()

    def plot_boxplots(self, columns, title):
        """Plot boxplots of specified columns."""
        for col in columns:
            plt.figure(figsize=(10, 6))
            self.df.boxplot(column=[col])
            plt.title(f'{title}: {col}')
            plt.ylabel(col)
            plt.show()

# DataFrameTransform Class Definition
class DataFrameTransform:
    def __init__(self, df):
        self.df = df.copy()  # Make a copy to avoid modifying the original DataFrame
    
    def check_nulls(self):
        """Check and return columns with NULL values and their percentages."""
        null_counts = self.df.isnull().sum()
        null_percentages = (null_counts / len(self.df)) * 100
        null_info = pd.DataFrame({
            'Null Counts': null_counts,
            'Null Percentage': null_percentages
        })
        print("Null Values in DataFrame:")
        print(null_info)
        return null_info
    
    def drop_columns(self, columns):
        """Drop specified columns from the DataFrame."""
        self.df.drop(columns=columns, inplace=True, errors='ignore')
        print(f"Dropped columns: {columns}")
    
    def impute_missing(self, strategy='median'):
        """Impute missing values using specified strategy ('mean' or 'median') for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            if self.df[col].isnull().any():
                if strategy == 'mean':
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif strategy == 'median':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    raise ValueError("Unsupported imputation strategy. Choose 'mean' or 'median'.")
        print(f"Imputed missing values using {strategy}.")
    
    def transform_skewed_columns(self, columns, transformations=['log', 'sqrt', 'boxcox']):
        """Transform skewed columns to reduce skewness."""
        from scipy.special import boxcox1p
        transformed_columns = {}

        for col in columns:
            best_transformation = None
            best_skew = float('inf')

            # Try different transformations
            for transformation in transformations:
                transformed_col = None

                if transformation == 'log':
                    transformed_col = np.log1p(self.df[col].dropna())
                elif transformation == 'sqrt':
                    transformed_col = np.sqrt(self.df[col].dropna())
                elif transformation == 'boxcox':
                    transformed_col, _ = boxcox1p(self.df[col].dropna(), 0.15)

                # Compute skewness of transformed column
                current_skew = skew(transformed_col.dropna())
                if abs(current_skew) < abs(best_skew):
                    best_skew = current_skew
                    best_transformation = transformed_col

            # Apply best transformation
            self.df[col] = best_transformation
            transformed_columns[col] = best_skew

        print("Transformed columns and their skewness after transformation:")
        print(transformed_columns)
        return transformed_columns

    def remove_outliers(self, columns, z_threshold=3):
        """Remove outliers from specified columns using Z-score method."""
        for col in columns:
            z_scores = np.abs(zscore(self.df[col]))
            self.df = self.df[(z_scores < z_threshold)]
        print(f"Removed outliers from columns: {columns}")

    def get_transformed_data(self):
        """Return the transformed DataFrame."""
        return self.df
