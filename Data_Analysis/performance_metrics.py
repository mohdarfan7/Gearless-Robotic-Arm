"""
Performance Metrics Analysis for Gearless Robotic Arm
Calculates and visualizes performance metrics compared to traditional designs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Sample metrics for demonstration
def calculate_efficiency_metrics():
    """Calculate key efficiency metrics"""
    
    # Traditional vs Gearless metrics
    metrics = {
        'weight_kg': {'Traditional': 3.2, 'Gearless': 2.1},
        'power_efficiency_pct': {'Traditional': 65, 'Gearless': 82},
        'precision_mm': {'Traditional': 1.2, 'Gearless': 0.6},
        'assembly_time_hrs': {'Traditional': 4.5, 'Gearless': 2.8},
        'maintenance_interval_hrs': {'Traditional': 200, 'Gearless': 500}
    }
    
    # Convert to DataFrame for easier visualization
    df = pd.DataFrame(metrics)
    return df

def visualize_metrics(metrics_df, output_file=None):
    """Visualize performance metrics"""
    
    # Create a figure
    plt.figure(figsize=(14, 8))
    
    # Calculate improvement percentages for labels
    improvements = {}
    for col in metrics_df.columns:
        trad_val = metrics_df.loc['Traditional', col]
        gearless_val = metrics_df.loc['Gearless', col]
        
        # For metrics where lower is better
        if col in ['weight_kg', 'precision_mm', 'assembly_time_hrs']:
            imp_pct = (trad_val - gearless_val) / trad_val * 100
            label_text = f"{imp_pct:.0f}% better"
        else:  # For metrics where higher is better
            imp_pct = (gearless_val - trad_val) / trad_val * 100
            label_text = f"{imp_pct:.0f}% better"
            
        improvements[col] = label_text
    
    # Create subplots for each metric
    for i, col in enumerate(metrics_df.columns):
        plt.subplot(2, 3, i+1)
        
        # Bar plot for this metric
        ax = sns.barplot(x=metrics_df.index, y=metrics_df[col])
        
        # Add improvement percentage
        max_val = metrics_df[col].max()
        y_pos = max_val * 1.1
        plt.text(0.5, y_pos, improvements[col], ha='center', fontweight='bold')
        
        # Formatting
        plt.title(col.replace('_', ' ').title())
        plt.ylabel(col.split('_')[-1].upper())
        
    plt.tight_layout()
    
    # Save if output file specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Performance visualization saved to {output_file}")
    else:
        plt.show()

def main():
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    
    print("Calculating performance metrics...")
    metrics = calculate_efficiency_metrics()
    
    print("Visualizing performance metrics...")
    output_file = "results/performance_comparison.png"
    visualize_metrics(metrics, output_file)
    
    # Save metrics to CSV
    csv_file = "processed_data/performance_metrics.csv"
    metrics.to_csv(csv_file)
    print(f"Performance metrics saved to {csv_file}")
    
    print("Performance analysis completed!")

if __name__ == "__main__":
    main()
