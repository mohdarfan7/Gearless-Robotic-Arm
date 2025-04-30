"""
Data Processing Module for Gearless Robotic Arm
Helper functions for data cleaning and preprocessing.

This module contains utility functions used by other analysis scripts to clean,
preprocess, and standardize data from robotic arm testing.

"""

import numpy as np
import pandas as pd
import os

def clean_test_data(df):
    """
    Clean and standardize test data
    
    Parameters:
    df (pandas.DataFrame): Raw data from tests
    
    Returns:
    pandas.DataFrame: Cleaned and preprocessed data
    """
    # Make a copy to avoid modifying the original
    data = df.copy()
    
    # Drop any rows with missing values
    data_cleaned = data.dropna()
    
    # Check for and remove outliers (values more than 3 std devs from mean)
    numeric_columns = data_cleaned.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        mean = data_cleaned[col].mean()
        std = data_cleaned[col].std()
        
        # Define outlier range
        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std
        
        # Filter out outliers
        data_cleaned = data_cleaned[(data_cleaned[col] >= lower_bound) & 
                                   (data_cleaned[col] <= upper_bound)]
    
    # Standardize column names (lowercase, replace spaces with underscores)
    data_cleaned.columns = [col.lower().replace(' ', '_') for col in data_cleaned.columns]
    
    # Ensure consistent data types
    type_mapping = {
        'joint_id': 'category',
        'joint_type': 'category',
        'design_type': 'category',
        'load_category': 'category'
    }
    
    for col, dtype in type_mapping.items():
        if col in data_cleaned.columns:
            data_cleaned[col] = data_cleaned[col].astype(dtype)
    
    return data_cleaned

def normalize_data(df, columns=None):
    """
    Normalize numeric data to 0-1 range
    
    Parameters:
    df (pandas.DataFrame): Data to normalize
    columns (list): Specific columns to normalize (None = all numeric)
    
    Returns:
    pandas.DataFrame: DataFrame with normalized columns
    """
    # Make a copy to avoid modifying the original
    data = df.copy()
    
    # If no columns specified, use all numeric columns
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns
    
    # Apply min-max normalization
    for col in columns:
        if col in data.columns:
            min_val = data[col].min()
            max_val = data[col].max()
            
            # Avoid division by zero
            if max_val > min_val:
                data[col] = (data[col] - min_val) / (max_val - min_val)
            else:
                data[col] = 0  # If all values are the same
    
    return data

def add_calculated_metrics(df):
    """
    Add calculated metrics based on raw measurements
    
    Parameters:
    df (pandas.DataFrame): Raw data
    
    Returns:
    pandas.DataFrame: Data with additional calculated metrics
    """
    # Make a copy to avoid modifying the original
    data = df.copy()
    
    # Calculate efficiency (if required columns exist)
    if 'power_consumption' in data.columns and 'load' in data.columns:
        # Avoid division by zero
        data['efficiency'] = np.where(
            data['load'] > 0,
            data['load'] / data['power_consumption'],
            0
        )
    
    # Calculate stress-to-weight ratio (if required columns exist)
    if 'stress' in data.columns and 'weight' in data.columns:
        # Avoid division by zero
        data['stress_to_weight_ratio'] = np.where(
            data['weight'] > 0,
            data['stress'] / data['weight'],
            0
        )
    
    # Calculate safety factor (if required columns exist)
    if 'stress' in data.columns and 'yield_strength' in data.columns:
        # Avoid division by zero
        data['safety_factor'] = np.where(
            data['stress'] > 0,
            data['yield_strength'] / data['stress'],
            np.nan
        )
    
    return data

def split_by_design_type(df):
    """
    Split data into traditional and gearless design datasets
    
    Parameters:
    df (pandas.DataFrame): Combined dataset
    
    Returns:
    tuple: (traditional_data, gearless_data)
    """
    if 'design_type' not in df.columns:
        raise ValueError("DataFrame does not contain 'design_type' column")
    
    traditional = df[df['design_type'] == 'traditional']
    gearless = df[df['design_type'] == 'gearless']
    
    return traditional, gearless

def ensure_directory_structure():
    """
    Ensure required directories exist
    
    Creates the standard directory structure for data analysis
    if it doesn't already exist.
    """
    directories = [
        'raw_data',
        'processed_data',
        'results',
        'results/figures',
        'results/reports'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
    print("Directory structure verified.")
