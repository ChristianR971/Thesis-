# Create figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
    fig.suptitle('Comparative Analysis: Baseline vs Intervention 1', fontsize=16, fontweight='bold')

    # 1. CO2 Emissions Comparison
    co2_data = [CO2_baseline, CO2_s1]
    co2_labels = ['Baseline', 'Intervention 1']
    ax1.bar(co2_labels, co2_data, color=['blue', 'green'])
    ax1.set_title('CO2 Emissions Comparison', fontsize=14)
    ax1.set_ylabel('Total CO2 Emissions')
    for i, v in enumerate(co2_data):
        ax1.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    # Add percentage change annotation
    pct_change_co2 = ((CO2_s1 - CO2_baseline) / CO2_baseline) * 100
    ax1.text(0.5, max(co2_data)*1.1, 
             f'Percentage Change: {pct_change_co2:.2f}%', 
             ha='center', fontweight='bold')

    # 2. Employment Comparison
    emp_data = [Emp_baseline1, Emp_1]
    emp_labels = ['Baseline', 'Intervention 1']
    ax2.bar(emp_labels, emp_data, color=['blue', 'orange'])
    ax2.set_title('Employment Comparison', fontsize=14)
    ax2.set_ylabel('Total Employment')
    for i, v in enumerate(emp_data):
        ax2.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    # Add percentage change annotation
    pct_change_emp = ((Emp_1 - Emp_baseline1) / Emp_baseline1) * 100
    ax2.text(0.5, max(emp_data)*1.1, 
             f'Percentage Change: {pct_change_emp:.2f}%', 
             ha='center', fontweight='bold')

    # 3. Value Added Comparison
    va_data = [VA_baseline, VA_s1]
    va_labels = ['Baseline', 'Intervention 1']
    ax3.bar(va_labels, va_data, color=['blue', 'red'])
    ax3.set_title('Value Added Comparison', fontsize=14)
    ax3.set_ylabel('Total Value Added')
    for i, v in enumerate(va_data):
        ax3.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    # Add percentage change annotation
    pct_change_va = ((VA_s1 - VA_baseline) / VA_baseline) * 100
    ax3.text(0.5, max(va_data)*1.1, 
             f'Percentage Change: {pct_change_va:.2f}%', 
             ha='center', fontweight='bold')

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('intervention_comparison.png', dpi=300, bbox_inches='tight')

    # Create a detailed breakdown plot
    plt.figure(figsize=(12, 8))
    
    # Prepare data for breakdown
    breakdown_data = {
        'CO2 Emissions': [CO2_baseline, CO2_s1],
        'Employment': [Emp_baseline1, Emp_1],
        'Value Added': [VA_baseline, VA_s1]
    }
    
    # Create a grouped bar plot
    x = np.arange(len(breakdown_data))
    width = 0.35
    
    plt.bar(x - width/2, [v[0] for v in breakdown_data.values()], width, label='Baseline', color='blue')
    plt.bar(x + width/2, [v[1] for v in breakdown_data.values()], width, label='Intervention 1', color='green')
    
    plt.title('Detailed Comparison: Baseline vs Intervention 1', fontsize=16)
    plt.xlabel('Metrics')
    plt.ylabel('Value')
    plt.xticks(x, list(breakdown_data.keys()))
    plt.legend()
    
    # Add percentage change annotations
    for i, (key, values) in enumerate(breakdown_data.items()):
        pct_change = ((values[1] - values[0]) / values[0]) * 100
        plt.text(i, max(values)*1.1, 
                 f'Change: {pct_change:.2f}%', 
                 ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('intervention_breakdown.png', dpi=300, bbox_inches='tight')
    
    # Print out key statistics
    print("Comparative Analysis Results:")
    print(f"CO2 Emissions - Baseline: {CO2_baseline:.2f}, Intervention: {CO2_s1:.2f}, % Change: {pct_change_co2:.2f}%")
    print(f"Employment - Baseline: {Emp_baseline1:.2f}, Intervention: {Emp_1:.2f}, % Change: {pct_change_emp:.2f}%")
    print(f"Value Added - Baseline: {VA_baseline:.2f}, Intervention: {VA_s1:.2f}, % Change: {pct_change_va:.2f}%")
