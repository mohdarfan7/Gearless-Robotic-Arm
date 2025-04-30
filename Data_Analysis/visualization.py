"""
Visualization Module for Gearless Robotic Arm
Creates advanced visualizations of test data and performance metrics.

Author: [Your Name]
Created: [Current Date]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from matplotlib.ticker import PercentFormatter
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Set style for all plots
plt.style.use('fivethirtyeight')
sns.set_context("paper", rc={"font.size":12,"axes.titlesize":14,"axes.labelsize":12})

def load_data_for_visualization(data_type='stress', file_path=None):
    """
    Load data for visualization from various sources
    
    Parameters:
    data_type (str): Type of data to load ('stress', 'performance', 'joint')
    file_path (str, optional): Path to specific data file
    
    Returns:
    pandas.DataFrame: Loaded data for visualization
    """
    if file_path and os.path.exists(file_path):
        # If specific file path provided, load it
        return pd.read_csv(file_path)
    
    # Default file paths based on data type
    if data_type == 'stress':
        default_path = 'processed_data/processed_stress_data.csv'
    elif data_type == 'performance':
        default_path = 'processed_data/sample_performance_data.csv'
    elif data_type == 'joint':
        default_path = 'processed_data/joint_performance.csv'
    elif data_type == 'payload':
        default_path = 'processed_data/payload_performance.csv'
    else:
        raise ValueError(f"Unknown data type: {data_type}")
    
    # Check if default file exists
    if os.path.exists(default_path):
        return pd.read_csv(default_path)
    else:
        print(f"Data file not found: {default_path}")
        print("Generating sample data for visualization...")
        
        # Generate sample data based on type
        if data_type == 'stress':
            return generate_sample_stress_data()
        elif data_type == 'performance':
            return generate_sample_performance_data()
        elif data_type == 'joint':
            return generate_sample_joint_data()
        elif data_type == 'payload':
            return generate_sample_payload_data()

def generate_sample_stress_data(n_samples=200):
    """Generate sample stress test data for visualization"""
    np.random.seed(42)
    
    # Create sample data
    joint_ids = np.random.choice(['base', 'shoulder', 'elbow', 'wrist'], n_samples)
    positions = np.random.uniform(0, 100, n_samples)
    loads = np.random.uniform(0, 3, n_samples)
    
    # Create design types with more traditional than gearless (to reflect real testing scenario)
    design_types = np.random.choice(['traditional', 'gearless'], n_samples, p=[0.6, 0.4])
    
    # Calculate stress values (with different parameters for each design)
    stress = np.zeros(n_samples)
    for i in range(n_samples):
        if design_types[i] == 'traditional':
            stress[i] = 120 + 45 * loads[i] + np.random.normal(0, 15)
        else:
            stress[i] = 80 + 30 * loads[i] + np.random.normal(0, 10)
    
    # Calculate deflection (correlated with stress and load)
    deflection = stress * 0.02 + loads * 0.2 + np.random.normal(0, 0.3, n_samples)
    
    # Create dataframe
    df = pd.DataFrame({
        'joint_id': joint_ids,
        'position': positions,
        'load': loads,
        'design_type': design_types,
        'stress': stress,
        'deflection': deflection
    })
    
    # Save to CSV
    os.makedirs('processed_data', exist_ok=True)
    df.to_csv('processed_data/sample_stress_data.csv', index=False)
    
    return df

def generate_sample_performance_data(n_samples=150):
    """Generate sample performance data for visualization"""
    np.random.seed(43)
    
    # Create sample data
    joint_types = np.random.choice(['base', 'shoulder', 'elbow', 'wrist'], n_samples)
    design_types = np.random.choice(['traditional', 'gearless'], n_samples)
    loads = np.random.uniform(0, 3, n_samples)
    
    # Calculate performance metrics with different models for each design
    power_consumption = np.zeros(n_samples)
    positioning_error = np.zeros(n_samples)
    temperature = np.zeros(n_samples)
    noise_level = np.zeros(n_samples)
    response_time = np.zeros(n_samples)
    
    for i in range(n_samples):
        # Power consumption model
        if design_types[i] == 'gearless':
            # Gearless design: more efficient
            power_consumption[i] = 18 + 8 * loads[i] + np.random.normal(0, 2)
        else:
            # Traditional design: less efficient
            power_consumption[i] = 25 + 12 * loads[i] + np.random.normal(0, 3)
            
        # Positioning error model
        if design_types[i] == 'gearless':
            # Gearless design: more precise
            positioning_error[i] = 0.3 + 0.06 * loads[i] + np.random.normal(0, 0.1)
        else:
            # Traditional design: less precise
            positioning_error[i] = 0.8 + 0.15 * loads[i] + np.random.normal(0, 0.2)
            
        # Temperature model
        if design_types[i] == 'gearless':
            # Gearless design: runs cooler
            temperature[i] = 28 + 4 * loads[i] + np.random.normal(0, 2)
        else:
            # Traditional design: runs hotter
            temperature[i] = 35 + 7 * loads[i] + np.random.normal(0, 3)
            
        # Noise level model
        if design_types[i] == 'gearless':
            # Gearless design: quieter
            noise_level[i] = 48 + 4 * loads[i] + np.random.normal(0, 1)
        else:
            # Traditional design: louder
            noise_level[i] = 65 + 3 * loads[i] + np.random.normal(0, 2)
            
        # Response time model
        if design_types[i] == 'gearless':
            # Gearless design: faster response
            response_time[i] = 100 + 20 * loads[i] + np.random.normal(0, 10)
        else:
            # Traditional design: slower response
            response_time[i] = 150 + 40 * loads[i] + np.random.normal(0, 15)
    
    # Create dataframe
    df = pd.DataFrame({
        'joint_type': joint_types,
        'design_type': design_types,
        'load': loads,
        'power_consumption': power_consumption,
        'positioning_error': positioning_error,
        'temperature': temperature,
        'noise_level': noise_level,
        'response_time': response_time
    })
    
    # Save to CSV
    df.to_csv('processed_data/sample_performance_data.csv', index=False)
    
    return df

def generate_sample_joint_data():
    """Generate sample joint performance data for visualization"""
    # Define joint types and design types
    joint_types = ['base', 'shoulder', 'elbow', 'wrist']
    design_types = ['traditional', 'gearless']
    
    # Initialize lists for dataframe
    rows = []
    
    # Create data for each joint and design type
    for joint in joint_types:
        for design in design_types:
            # Base values for each metric
            if design == 'gearless':
                power_base = 20
                error_base = 0.35
                temp_base = 30
                response_base = 110
            else:
                power_base = 28
                error_base = 0.9
                temp_base = 38
                response_base = 160
            
            # Joint-specific modifiers
            if joint == 'base':
                power_mod = 0.9
                error_mod = 0.8
                temp_mod = 0.9
                response_mod = 0.9
            elif joint == 'shoulder':
                power_mod = 1.2
                error_mod = 1.0
                temp_mod = 1.1
                response_mod = 1.0
            elif joint == 'elbow':
                power_mod = 1.0
                error_mod = 1.1
                temp_mod = 1.0
                response_mod = 1.1
            else:  # wrist
                power_mod = 0.8
                error_mod = 1.2
                temp_mod = 0.8
                response_mod = 1.2
            
            # Calculate metrics with some random variation
            power = power_base * power_mod * np.random.uniform(0.95, 1.05)
            error = error_base * error_mod * np.random.uniform(0.95, 1.05)
            temp = temp_base * temp_mod * np.random.uniform(0.97, 1.03)
            response = response_base * response_mod * np.random.uniform(0.95, 1.05)
            
            # Add to rows
            rows.append({
                'joint_type': joint,
                'design_type': design,
                'power_consumption': power,
                'positioning_error': error,
                'temperature': temp,
                'response_time': response
            })
    
    # Create dataframe
    df = pd.DataFrame(rows)
    
    # Save to CSV
    df.to_csv('processed_data/joint_performance.csv', index=False)
    
    return df

def generate_sample_payload_data():
    """Generate sample payload performance data for visualization"""
    # Define load categories and design types
    load_categories = ['0-25%', '25-50%', '50-75%', '75-100%']
    design_types = ['traditional', 'gearless']
    
    # Initialize lists for dataframe
    rows = []
    
    # Create data for each load category and design type
    for load_cat in load_categories:
        for design in design_types:
            # Map load category to numeric load for calculations
            if load_cat == '0-25%':
                load_val = 0.375  # 12.5% average
            elif load_cat == '25-50%':
                load_val = 1.125  # 37.5% average
            elif load_cat == '50-75%':
                load_val = 1.875  # 62.5% average
            else:  # 75-100%
                load_val = 2.625  # 87.5% average
            
            # Calculate metrics based on design type and load
            if design == 'gearless':
                power = 18 + 8 * load_val * np.random.uniform(0.95, 1.05)
                error = 0.3 + 0.06 * load_val * np.random.uniform(0.95, 1.05)
                temp = 28 + 4 * load_val * np.random.uniform(0.97, 1.03)
                noise = 48 + 4 * load_val * np.random.uniform(0.98, 1.02)
                response = 100 + 20 * load_val * np.random.uniform(0.95, 1.05)
            else:
                power = 25 + 12 * load_val * np.random.uniform(0.95, 1.05)
                error = 0.8 + 0.15 * load_val * np.random.uniform(0.95, 1.05)
                temp = 35 + 7 * load_val * np.random.uniform(0.97, 1.03)
                noise = 65 + 3 * load_val * np.random.uniform(0.98, 1.02)
                response = 150 + 40 * load_val * np.random.uniform(0.95, 1.05)
            
            # Add to rows
            rows.append({
                'load_category': load_cat,
                'design_type': design,
                'power_consumption': power,
                'positioning_error': error,
                'temperature': temp,
                'noise_level': noise,
                'response_time': response
            })
    
    # Create dataframe
    df = pd.DataFrame(rows)
    
    # Save to CSV
    df.to_csv('processed_data/payload_performance.csv', index=False)
    
    return df

def create_stress_distribution_plot(data, output_file=None):
    """
    Create visualization of stress distribution across different design types
    
    Parameters:
    data (DataFrame): Stress test data
    output_file (str): Path to save the visualization
    """
    print("Generating stress distribution visualization...")
    
    # Create a figure
    plt.figure(figsize=(16, 12))
    
    # Set color palette
    colors = {'traditional': '#ff6b6b', 'gearless': '#4ecdc4'}
    
    # SUBPLOT 1: Stress Distribution by Design Type
    plt.subplot(2, 2, 1)
    for design in ['traditional', 'gearless']:
        subset = data[data['design_type'] == design]
        sns.kdeplot(subset['stress'], fill=True, label=design.title(), color=colors[design], alpha=0.7)
    
    plt.title('Stress Distribution by Design Type')
    plt.xlabel('Stress (MPa)')
    plt.ylabel('Density')
    plt.legend(title='Design Type')
    
    # SUBPLOT 2: Stress vs. Load Scatterplot
    plt.subplot(2, 2, 2)
    
    # Create scatter plot with regression lines
    for design in ['traditional', 'gearless']:
        subset = data[data['design_type'] == design]
        sns.regplot(x='load', y='stress', data=subset, scatter_kws={'alpha':0.5, 's':50}, 
                   line_kws={'lw':2}, label=design.title(), color=colors[design])
    
    plt.title('Stress vs. Load Relationship')
    plt.xlabel('Load (kg)')
    plt.ylabel('Stress (MPa)')
    plt.legend(title='Design Type')
    
    # SUBPLOT 3: Stress Distribution by Joint
    plt.subplot(2, 2, 3)
    
    # Calculate mean stress by joint and design type
    joint_stress = data.groupby(['joint_id', 'design_type'])['stress'].mean().reset_index()
    
    # Create a barplot
    barplot = sns.barplot(x='joint_id', y='stress', hue='design_type', data=joint_stress, 
                        palette=colors, alpha=0.8)
    
    # Add percentage improvement labels
    for i, joint in enumerate(joint_stress['joint_id'].unique()):
        # Get values for traditional and gearless designs for this joint
        trad_val = joint_stress[(joint_stress['joint_id'] == joint) & 
                                (joint_stress['design_type'] == 'traditional')]['stress'].values[0]
        gear_val = joint_stress[(joint_stress['joint_id'] == joint) & 
                               (joint_stress['design_type'] == 'gearless')]['stress'].values[0]
        
        # Calculate improvement percentage
        imp_pct = (trad_val - gear_val) / trad_val * 100
        
        # Add label
        plt.text(i, max(trad_val, gear_val) + 5, f"{imp_pct:.1f}%", ha='center', fontweight='bold')
    
    plt.title('Average Stress by Joint Type')
    plt.xlabel('Joint')
    plt.ylabel('Average Stress (MPa)')
    plt.legend(title='Design Type')
    
    # SUBPLOT 4: Deflection vs. Stress
    plt.subplot(2, 2, 4)
    
    # Create scatter plot with regression lines for each design type
    for design in ['traditional', 'gearless']:
        subset = data[data['design_type'] == design]
        sns.regplot(x='stress', y='deflection', data=subset, scatter_kws={'alpha':0.5, 's':50}, 
                   line_kws={'lw':2}, label=design.title(), color=colors[design])
    
    plt.title('Deflection vs. Stress Relationship')
    plt.xlabel('Stress (MPa)')
    plt.ylabel('Deflection (mm)')
    plt.legend(title='Design Type')
    
    plt.tight_layout()
    
    # Save or display the figure
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {output_file}")
    else:
        plt.show()

def create_3d_stress_visualization(data, output_file=None):
    """
    Create 3D visualization of stress distribution across load and position
    
    Parameters:
    data (DataFrame): Stress test data
    output_file (str): Path to save the visualization
    """
    print("Generating 3D stress visualization...")
    
    # Create a figure
    fig = plt.figure(figsize=(16, 8))
    
    # Create separate 3D plots for traditional and gearless designs
    for i, design in enumerate(['traditional', 'gearless']):
        # Filter data for this design
        subset = data[data['design_type'] == design]
        
        # Create 3D plot
        ax = fig.add_subplot(1, 2, i+1, projection='3d')
        
        # Create scatter plot
        scatter = ax.scatter(subset['position'], subset['load'], subset['stress'],
                           c=subset['stress'], cmap='inferno', s=50, alpha=0.7)
        
        # Add color bar
        cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label('Stress (MPa)')
        
        # Set labels and title
        ax.set_xlabel('Position (mm)')
        ax.set_ylabel('Load (kg)')
        ax.set_zlabel('Stress (MPa)')
        ax.set_title(f'{design.title()} Design Stress Distribution')
        
        # Add gridlines
        ax.grid(True)
        
        # Set same scale for both plots
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 3)
        ax.set_zlim(0, data['stress'].max() * 1.1)
    
    plt.tight_layout()
    
    # Save or display the figure
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {output_file}")
    else:
        plt.show()

def create_performance_radar_chart(metrics, output_file=None):
    """
    Create radar chart comparing performance metrics between designs
    
    Parameters:
    metrics (dict): Dictionary with performance metrics
    output_file (str): Path to save the visualization
    """
    print("Generating performance radar chart...")
    
    # Extract relevant metrics (exclude improvements)
    plot_metrics = {k: v for k, v in metrics.items() if k != 'improvements'}
    
    # Normalize metrics for radar chart (all metrics should be 0-1 where 1 is better)
    categories = []
    traditional_values = []
    gearless_values = []
    
    for metric, values in plot_metrics.items():
        categories.append(metric.replace('_', ' ').title())
        
        # For metrics where lower is better, we invert the normalization
        if metric in ['weight_kg', 'power_efficiency', 'positioning_error_mm', 
                     'temperature_c', 'noise_level_db', 'response_time_ms']:
            # Find max value for normalization
            max_val = max(values['Traditional'], values['Gearless']) * 1.1  # Add 10% for margin
            
            # Normalize and invert (subtract from 1)
            traditional_values.append(1 - (values['Traditional'] / max_val))
            gearless_values.append(1 - (values['Gearless'] / max_val))
        else:
            # For metrics where higher is better
            max_val = max(values['Traditional'], values['Gearless']) * 1.1  # Add 10% for margin
            
            # Normalize
            traditional_values.append(values['Traditional'] / max_val)
            gearless_values.append(values['Gearless'] / max_val)
    
    # Number of categories
    N = len(categories)
    
    # Compute angle for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Add values for traditional and gearless
    traditional_values += traditional_values[:1]  # Close the loop
    gearless_values += gearless_values[:1]  # Close the loop
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Plot traditional design
    ax.plot(angles, traditional_values, 'o-', linewidth=2, label='Traditional Design', color='#ff6b6b')
    ax.fill(angles, traditional_values, alpha=0.25, color='#ff6b6b')
    
    # Plot gearless design
    ax.plot(angles, gearless_values, 'o-', linewidth=2, label='Gearless Design', color='#4ecdc4')
    ax.fill(angles, gearless_values, alpha=0.25, color='#4ecdc4')
    
    # Set category labels
    plt.xticks(angles[:-1], categories, size=12)
    
    # Set radial ticks
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10)
    plt.ylim(0, 1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title('Performance Metrics Comparison', size=16, y=1.1)
    
    # Save or display the figure
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {output_file}")
    else:
        plt.show()

def create_animated_joint_motion(output_file=None):
    """
    Create animated visualization of joint motion
    
    Parameters:
    output_file (str): Path to save the animation
    """
    print("Generating joint motion animation...")
    
    # Define arm dimensions
    upper_arm_length = 350  # mm
    forearm_length = 300  # mm
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Set limits for both axes
    ax1.set_xlim(-700, 700)
    ax1.set_ylim(-100, 700)
    ax2.set_xlim(-700, 700)
    ax2.set_ylim(-100, 700)
    
    # Set titles and labels
    ax1.set_title('Traditional Geared Design', fontsize=14)
    ax2.set_title('Gearless Design', fontsize=14)
    ax1.set_xlabel('X Position (mm)')
    ax1.set_ylabel('Y Position (mm)')
    ax2.set_xlabel('X Position (mm)')
    ax2.set_ylabel('Y Position (mm)')
    
    # Make axes equal to preserve aspect ratio
    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    
    # Add grid
    ax1.grid(True)
    ax2.grid(True)
    
    # Initialize lines for traditional design (left panel)
    base_point1 = ax1.plot([0], [0], 'ko', markersize=10)[0]
    upper_arm1 = ax1.plot([0, 0], [0, 0], 'r-', linewidth=5)[0]
    elbow_point1 = ax1.plot([0], [0], 'ko', markersize=7)[0]
    forearm1 = ax1.plot([0, 0], [0, 0], 'r-', linewidth=5)[0]
    end_effector1 = ax1.plot([0], [0], 'ko', markersize=7)[0]
    
    # Add "jitter" line for traditional design to represent backlash
    jitter1 = ax1.plot([0, 0], [0, 0], 'r--', linewidth=1, alpha=0.5)[0]
    
    # Initialize lines for gearless design (right panel)
    base_point2 = ax2.plot([0], [0], 'ko', markersize=10)[0]
    upper_arm2 = ax2.plot([0, 0], [0, 0], 'b-', linewidth=5)[0]
    elbow_point2 = ax2.plot([0], [0], 'ko', markersize=7)[0]
    forearm2 = ax2.plot([0, 0], [0, 0], 'b-', linewidth=5)[0]
    end_effector2 = ax2.plot([0], [0], 'ko', markersize=7)[0]
    
    # Add target point
    target1 = ax1.plot([400], [300], 'gX', markersize=10)[0]
    target2 = ax2.plot([400], [300], 'gX', markersize=10)[0]
    
    # Add position error text
    error_text1 = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, fontsize=12, 
                         verticalalignment='top')
    error_text2 = ax2.text(0.05, 0.95, '', transform=ax2.transAxes, fontsize=12, 
                         verticalalignment='top')
    
    # Animation update function
    def update(frame):
        # Set shoulder angle (0 to 90 degrees)
        shoulder_angle = np.radians(frame)
        
        # Set elbow angle (0 to 90 degrees, in opposite direction)
        elbow_angle = np.radians(frame * 0.8)
        
        # Calculate joint positions for traditional design (with error)
        # Add backlash error for traditional design
        if frame < 45:
            shoulder_error = np.radians(1.2)  # Larger error during first half
            elbow_error = np.radians(1.5)
        else:
            shoulder_error = np.radians(0.8)  # Smaller error during second half
            elbow_error = np.radians(1.0)
        
        # Add some random jitter to represent mechanical play
        if frame % 5 == 0:  # Every 5 frames
            shoulder_jitter = np.random.uniform(-0.5, 0.5)
            elbow_jitter = np.random.uniform(-0.7, 0.7)
        else:
            shoulder_jitter = 0
            elbow_jitter = 0
        
        shoulder_angle1 = shoulder_angle + shoulder_error + np.radians(shoulder_jitter)
        elbow_angle1 = elbow_angle + elbow_error + np.radians(elbow_jitter)
        
        # Calculate positions for traditional design
        x_elbow1 = upper_arm_length * np.cos(shoulder_angle1)
        y_elbow1 = upper_arm_length * np.sin(shoulder_angle1)
        
        x_end1 = x_elbow1 + forearm_length * np.cos(shoulder_angle1 + elbow_angle1)
        y_end1 = y_elbow1 + forearm_length * np.sin(shoulder_angle1 + elbow_angle1)
        
        # Calculate positions for gearless design (more precise)
        shoulder_angle2 = shoulder_angle + np.radians(0.2)  # Smaller error
        elbow_angle2 = elbow_angle + np.radians(0.3)  # Smaller error
        
        x_elbow2 = upper_arm_length * np.cos(shoulder_angle2)
        y_elbow2 = upper_arm_length * np.sin(shoulder_angle2)
        
        x_end2 = x_elbow2 + forearm_length * np.cos(shoulder_angle2 + elbow_angle2)
        y_end2 = y_elbow2 + forearm_length * np.sin(shoulder_angle2 + elbow_angle2)
        
        # Calculate jitter line for traditional design (to visualize backlash)
        jitter_x = [x_end1, x_end1 + np.random.uniform(-10, 10)]
        jitter_y = [y_end1, y_end1 + np.random.uniform(-10, 10)]
        
        # Update line data for traditional design
        upper_arm1.set_data([0, x_elbow1], [0, y_elbow1])
        elbow_point1.set_data([x_elbow1], [y_elbow1])
        forearm1.set_data([x_elbow1, x_end1], [y_elbow1, y_end1])
        end_effector1.set_data([x_end1], [y_end1])
        jitter1.set_data(jitter_x, jitter_y)
        
        # Update line data for gearless design
        upper_arm2.set_data([0, x_elbow2], [0, y_elbow2])
        elbow_point2.set_data([x_elbow2], [y_elbow2])
        forearm2.set_data([x_elbow2, x_end2], [y_elbow2, y_end2])
        end_effector2.set_data([x_end2], [y_end2])
        
        # Calculate position error (distance to target)
        target_x, target_y = 400, 300
        error1 = np.sqrt((x_end1 - target_x)**2 + (y_end1 - target_y)**2)
        error2 = np.sqrt((x_end2 - target_x)**2 + (y_end2 - target_y)**2)
        
        # Update error text
        error_text1.set_text(f'Position Error: {error1:.1f} mm')
        error_text2.set_text(f'Position Error: {error2:.1f} mm')
        
        return [upper_arm1, elbow_point1, forearm1, end_effector1, jitter1,
               upper_arm2, elbow_point2, forearm2, end_effector2,
               error_text1, error_text2]
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=90, interval=100, blit=True)
    
    plt.tight_layout()
    
    # Save or display the animation
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        anim.save(output_file, writer='pillow', fps=10)
        print(f"Animation saved to {output_file}")
    else:
        plt.show()

def main():
    """Main function to generate visualizations"""
    
    # Ensure directories exist
    os.makedirs('processed_data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    print("=" * 70)
    print("GEARLESS ROBOTIC ARM - VISUALIZATION GENERATION")
    print("=" * 70)
    
    try:
        # Load efficiency metrics
        if os.path.exists('results/efficiency_metrics.json'):
            with open('results/efficiency_metrics.json', 'r') as f:
                metrics = json.load(f)
        else:
            # If metrics file doesn't exist, generate performance data and calculate metrics
            from performance_metrics import calculate_efficiency_metrics
            performance_data = load_data_for_visualization('performance')
            metrics = calculate_efficiency_metrics(performance_data)
        
        # Load stress data
        stress_data = load_data_for_visualization('stress')
        
        # Generate visualizations
        
        # 1. Create stress distribution visualization
        create_stress_distribution_plot(stress_data, 'results/stress_distribution.png')
        
        # 2. Create 3D stress visualization
        create_3d_stress_visualization(stress_data, 'results/stress_3d_visualization.png')
        
        # 3. Create performance radar chart
        create_performance_radar_chart(metrics, 'results/performance_radar.png')
        
        # 4. Create animated joint motion (GIF file)
        create_animated_joint_motion('results/joint_motion.gif')
        
        print("\nAll visualizations generated successfully!")
        
    except Exception as e:
        print(f"Error during visualization generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
