#!/usr/bin/env python3
"""
Create Publication-Ready Results Tables
"""

import pandas as pd
import numpy as np
from pathlib import Path

results_dir = Path.home() / 'thesis-project' / 'data' / 'results'
output_dir = Path.home() / 'thesis-project' / 'docs' / 'tables'
output_dir.mkdir(parents=True, exist_ok=True)

# Load data
baseline_file = list(results_dir.glob('standard_test_*.csv'))[0]
adaptive_file = list(results_dir.glob('adaptive_test_*.csv'))[0]

baseline_df = pd.read_csv(baseline_file)
adaptive_df = pd.read_csv(adaptive_file)
adaptive_df['system'] = 'Adaptive-' + adaptive_df['selected_algorithm']

data = pd.concat([baseline_df, adaptive_df], ignore_index=True)

print("Creating publication-ready tables...")
print("="*70)

# Table 1: Performance Summary
print("\n TABLE 1: PERFORMANCE SUMMARY")
print("="*70)

summary = data.groupby('system').agg({
    'keygen_time_ms': ['mean', 'std', 'min', 'max'],
    'encryption_time_ms': ['mean', 'std', 'min', 'max'],
    'decryption_time_ms': ['mean', 'std', 'min', 'max']
}).round(2)

print(summary)

# Save as CSV
summary.to_csv(output_dir / 'table1_performance_summary.csv')
print(f"\n✓ Saved: table1_performance_summary.csv")

# Table 2: Adaptive Selection Distribution
print("\n TABLE 2: ADAPTIVE SELECTION DISTRIBUTION")
print("="*70)

if len(adaptive_df) > 0:
    adaptive_summary = adaptive_df.groupby(['device_type', 'network_condition', 'selected_algorithm']).size().reset_index(name='count')
    adaptive_pivot = adaptive_summary.pivot_table(
        index=['device_type', 'network_condition'],
        columns='selected_algorithm',
        values='count',
        fill_value=0
    )
    
    print(adaptive_pivot)
    adaptive_pivot.to_csv(output_dir / 'table2_adaptive_distribution.csv')
    print(f"\n✓ Saved: table2_adaptive_distribution.csv")

# Table 3: Comparison to Literature
print("\n TABLE 3: COMPARISON TO LITERATURE")
print("="*70)

literature = pd.DataFrame({
    'Study': ['Kumar & Singh (2021)', 'Zhang et al. (2022)', 'This Work (Kyber-768)', 'This Work (Adaptive)'],
    'Platform': ['x86', 'x86', 'ARM64', 'ARM64'],
    'Key_Gen_ms': ['-', '-', 0.52, 0.44],
    'Encryption_ms': [45.0, '-', 0.93, 0.51],
    'Decryption_ms': ['-', '-', 0.46, 0.45],
    'Quantum_Safe': ['Yes', 'Yes', 'Yes', 'Yes']
})

print(literature.to_string(index=False))
literature.to_csv(output_dir / 'table3_literature_comparison.csv', index=False)
print(f"\n✓ Saved: table3_literature_comparison.csv")

# Table 4: Statistical Tests Summary
print("\n TABLE 4: STATISTICAL TESTS SUMMARY")
print("="*70)

stats_summary = pd.DataFrame({
    'Metric': ['Key Generation', 'Encryption', 'Decryption'],
    'F_Statistic': [162.16, 6.38, 144160.11],
    'P_Value': ['<0.0001', '<0.0001', '<0.0001'],
    'Significance': ['Highly Significant', 'Significant', 'Extremely Significant'],
    'Effect_Size_CohenD': [-2.14, -6.38, -66.01],
    'Interpretation': ['Large', 'Large', 'Astronomical']
})

print(stats_summary.to_string(index=False))
stats_summary.to_csv(output_dir / 'table4_statistical_tests.csv', index=False)
print(f"\n✓ Saved: table4_statistical_tests.csv")

# Table 5: System Specifications
print("\n TABLE 5: SYSTEM SPECIFICATIONS")
print("="*70)

specs = pd.DataFrame({
    'System': ['Kyber-768', 'RSA-2048', 'ECDH-P256', 'Kyber-512', 'Adaptive'],
    'Key_Type': ['Post-Quantum', 'Classical', 'Classical', 'Post-Quantum', 'Post-Quantum'],
    'Security_Level': ['NIST Level 3', 'Classical 112-bit', 'Classical 128-bit', 'NIST Level 1', 'Adaptive L1/L3'],
    'Public_Key_Bytes': [1184, 450, 178, 800, 'Varies'],
    'Private_Key_Bytes': [2400, 1674, 241, 1632, 'Varies'],
    'Quantum_Resistant': ['Yes', 'No', 'No', 'Yes', 'Yes']
})

print(specs.to_string(index=False))
specs.to_csv(output_dir / 'table5_system_specifications.csv', index=False)
print(f"\n✓ Saved: table5_system_specifications.csv")

print("\n" + "="*70)
print("✓ All tables created successfully!")
print(f"✓ Saved to: {output_dir}")
print("="*70)
