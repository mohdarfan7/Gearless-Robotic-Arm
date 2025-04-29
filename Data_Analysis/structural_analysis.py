import pandas as pd            # For data manipulation and analysis
import numpy as np             # For numerical operations
import matplotlib.pyplot as plt # For creating visualizations
import seaborn as sns          # For enhanced visualizations
from datetime import datetime  # For timestamp operations

# This script analyzes structural test data from the gearless robotic arm project
# It processes raw test data, analyzes structural integrity, and creates visualizations

def load_test_data(file_path):
    """
    Load structural test data from CSV file
    
    Parameters:
    ----------
    file_path : str
        Path to the CSV file containing test data
        
    Returns:
    -------
    pandas.DataFrame
        DataFrame containing the loaded test data
    """
    print(f"Loading test data from {file_path}...")
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    print(f"Loaded {len(df)} data points.")
    return df

def clean_data(df):
    """
    Clean and preprocess the structural test data
    
    This function:
    1. Removes duplicate entries
    2. Handles missing values
    3. Converts timestamps to proper datetime objects
    4. Calculates additional metrics like stiffness
    
    Parameters:
    ----------
    df : pandas.DataFrame
        Raw test data
        
    Returns:
    -------
    pandas.DataFrame
        Cleaned and preprocessed test data
    """
    # Remove any duplicate rows in the dataset
    df_clean = df.drop_duplicates()
    
    # Fill missing values by carrying forward the last valid observation
    # This is appropriate for time-series structural test data
    df_clean = df_clean.fillna(method='ffill')
    
    # Convert timestamp strings to datetime objects for time-based analysis
    if 'timestamp' in df_clean.columns:
        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
    
    # Calculate stiffness as force divided by displacement
    # This is an important mechanical property for structural analysis
    if all(col in df_clean.columns for col in ['force_applied', 'displacement']):
        df_clean['stiffness'] = df_clean['force_applied'] / df_clean['displacement']
    
    print(f"Data cleaning complete. {len(df) - len(df_clean)} duplicate rows removed.")
    return df_clean

def analyze_structural_integrity(df):
    """
    Analyze structural integrity based on test data
    
    Calculates key metrics including:
    - Maximum and average stress values
    - Maximum and average strain values
    - Number of potential failure points
    - Failure rate percentage
    - Joint performance analysis
    
    Parameters:
    ----------
    df : pandas.DataFrame
        Cleaned test data
        
    Returns:
    -------
    dict
        Dictionary containing analysis results
    """
    # Initialize results dictionary with key structural metrics
    results = {
        'max_stress': df['stress'].max(),        # Maximum stress recorded during testing
        'avg_stress': df['stress'].mean(),       # Average stress across all tests
        'max_strain': df['strain'].max(),        # Maximum strain recorded
        'avg_strain': df['strain'].mean(),       # Average strain across all tests
        
        # Count points where stress exceeds the defined threshold (potential failures)
        'failure_points': len(df[df['stress'] > df['stress_threshold']])
    }
    
    # Calculate overall failure rate if test outcome data is available
    if 'test_outcome' in df.columns:
        # Calculate percentage of tests that resulted in failure
        results['failure_rate'] = (df['test_outcome'] == 'fail').mean() * 100
        
    # Analyze performance of individual joints if data is available
    if all(col in df.columns for col in ['joint_id', 'performance_score']):
        # Group by joint_id and calculate mean performance score for each joint
        joint_performance = df.groupby('joint_id')['performance_score'].mean()
        results['joint_performance'] = joint_performance.to_dict()
    
    return results

def visualize_stress_distribution(df, output_path=None):
    """
    Create visualization of stress distribution across the structure
    
    Generates two plots:
    1. Bar chart showing average stress by part
    2. Line chart showing stress over time
    
    Parameters:
    ----------
    df : pandas.DataFrame
        Cleaned test data
    output_path : str, optional
        Path to save the visualization image
    """
    # Create a figure with appropriate dimensions
    plt.figure(figsize=(12, 8))
    
    # PLOT 1: Create heatmap of stress across different parts
    if all(col in df.columns for col in ['part_id', 'stress']):
        # Group by part_id and calculate mean stress for each part
        stress_by_part = df.groupby('part_id')['stress'].mean().reset_index()
        
        # Create a bar plot showing stress distribution by part
        plt.subplot(2, 1, 1)  # First subplot in a 2x1 grid
        sns.barplot(x='part_id', y='stress', data=stress_by_part)
        plt.title('Average Stress by Part')
        plt.xlabel('Part ID')
        plt.ylabel('Stress (MPa)')
        
    # PLOT 2: Create a line plot of stress over time
    if all(col in df.columns for col in ['timestamp', 'stress']):
        plt.subplot(2, 1, 2)  # Second subplot in a 2x1 grid
        
        # Group data by hour and calculate mean stress
        time_series = df.groupby(pd.Grouper(key='timestamp', freq='1H'))['stress'].mean()
        
        # Plot the time series data
        plt.plot(time_series.index, time_series.values)
        plt.title('Stress Over Time')
        plt.xlabel('Time')
        plt.ylabel('Stress (MPa)')
        
    # Ensure plots don't overlap
    plt.tight_layout()
    
    # Save the visualization if output path is provided
    if output_path:
        plt.savefig(output_path)
        print(f"Visualization saved to {output_path}")
    else:
        plt.show()  # Display the plot if not saving to file

def compare_design_iterations(df):
    """
    Compare performance metrics across different design iterations
    
    Analyzes how design changes affected key performance metrics and
    calculates improvement percentages between iterations.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        Cleaned test data that includes design iteration information
        
    Returns:
    -------
    pandas.DataFrame
        Table comparing metrics across design iterations
    """
    # Check if design iteration data is available
    if 'design_iteration' not in df.columns:
        print("Design iteration data not available")
        return None
    
    # Group by design iteration and calculate key metrics for each iteration
    design_comparison = df.groupby('design_iteration').agg({
        'stress': ['mean', 'max'],         # Average and maximum stress
        'strain': ['mean', 'max'],         # Average and maximum strain
        'weight': 'mean',                  # Average weight
        'performance_score': 'mean'        # Average performance score
    })
    
    # Calculate improvement percentages between consecutive iterations
    # Positive values indicate improvement, negative values indicate regression
    design_comparison['improvement'] = design_comparison[('performance_score', 'mean')].pct_change() * 100
    
    return design_comparison

def main():
    """
    Main function to run the analysis
    
    This orchestrates the entire analysis workflow:
    1. Loads test data from CSV
    2. Cleans and preprocesses the data
    3. Performs structural integrity analysis
    4. Compares design iterations
    5. Generates visualizations
    6. Saves results to output files
    """
    # Define file paths
    data_file = "data/structural_tests.csv"  # Input data file
    output_dir = "results/"                  # Directory to save results
    
    # Create timestamp for unique output file names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Execute analysis workflow
    try:
        # Step 1: Load data from CSV file
        df = load_test_data(data_file)
        
        # Step 2: Clean and preprocess the data
        df_clean = clean_data(df)
        
        # Step 3: Run structural integrity analysis
        structural_results = analyze_structural_integrity(df_clean)
        
        # Step 4: Compare different design iterations
        design_comparison = compare_design_iterations(df_clean)
        
        # Step 5: Save analysis results to a text file
        with open(f"{output_dir}structural_analysis_{timestamp}.txt", "w") as f:
            f.write("Structural Integrity Analysis Results\n")
            f.write("====================================\n")
            for key, value in structural_results.items():
                f.write(f"{key}: {value}\n")
        
        # Step 6: Save processed data to CSV for future reference
        df_clean.to_csv(f"{output_dir}processed_data_{timestamp}.csv", index=False)
        
        # Step 7: Generate and save visualizations
        visualize_stress_distribution(df_clean, f"{output_dir}stress_distribution_{timestamp}.png")
        
        print("Analysis completed successfully!")
        
    except Exception as e:
        # Handle any errors that occur during analysis
        print(f"Error during analysis: {e}")

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
