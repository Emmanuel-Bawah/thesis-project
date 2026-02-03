#!/usr/bin/env python3
"""
Create Publication-Ready Visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set publication style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

results_dir = Path.home() / 'thesis-project' / 'data' / 'results'
output_dir = Path.home() / 'thesis-project' / 'data' / 'results' / 'figures'
output_dir.mkdir(exist_ok=True)

# Load data
baseline_file = list(results_dir.glob('standard_test_*.csv'))[0]
adaptive_file = list(results_dir.glob('adaptive_test_*.csv'))[0]

baseline_df = pd.read_csv(baseline_file)
adaptive_df = pd.read_csv(adaptive_file)
adaptive_df['system'] = 'Adaptive-' + adaptive_df['selected_algorithm']

data = pd.concat([baseline_df, adaptive_df], ignore_index=True)

# Exclude RSA from some plots (too different scale)
data_no_rsa = data[data['system'] != 'RSA-2048']

print("Creating visualizations...")

# Figure 1: Key Generation Time (without RSA)
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=data_no_rsa, x='system', y='keygen_time_ms', ax=ax)
ax.set_xlabel('Encryption System', fontsize=12, fontweight='bold')
ax.set_ylabel('Key Generation Time (ms)', fontsize=12, fontweight='bold')
ax.set_title('Key Generation Performance Comparison\n(Post-Quantum Systems)', 
             fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / 'keygen_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: keygen_comparison.png")
plt.close()

# Figure 2: Encryption Time (without RSA)
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=data_no_rsa, x='system', y='encryption_time_ms', ax=ax)
ax.set_xlabel('Encryption System', fontsize=12, fontweight='bold')
ax.set_ylabel('Encryption Time (ms)', fontsize=12, fontweight='bold')
ax.set_title('Encryption Performance Comparison', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / 'encryption_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: encryption_comparison.png")
plt.close()

# Figure 3: Decryption Time (without RSA)
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=data_no_rsa, x='system', y='decryption_time_ms', ax=ax)
ax.set_xlabel('Encryption System', fontsize=12, fontweight='bold')
ax.set_ylabel('Decryption Time (ms)', fontsize=12, fontweight='bold')
ax.set_title('Decryption Performance Comparison', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / 'decryption_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: decryption_comparison.png")
plt.close()

# Figure 4: All metrics with RSA (log scale)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

metrics = [
    ('keygen_time_ms', 'Key Generation (ms)'),
    ('encryption_time_ms', 'Encryption (ms)'),
    ('decryption_time_ms', 'Decryption (ms)')
]

for idx, (metric, label) in enumerate(metrics):
    sns.boxplot(data=data, x='system', y=metric, ax=axes[idx])
    axes[idx].set_yscale('log')
    axes[idx].set_xlabel('System', fontsize=10, fontweight='bold')
    axes[idx].set_ylabel(label, fontsize=10, fontweight='bold')
    axes[idx].tick_params(axis='x', rotation=45)
    plt.setp(axes[idx].xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.suptitle('Complete Performance Comparison (Log Scale)', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'complete_comparison_log.png', dpi=300, bbox_inches='tight')
print("✓ Saved: complete_comparison_log.png")
plt.close()

# Figure 5: Adaptive system performance by device type
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (metric, label) in enumerate(metrics):
    sns.boxplot(data=adaptive_df, x='device_type', y=metric, 
                hue='selected_algorithm', ax=axes[idx])
    axes[idx].set_xlabel('Device Type', fontsize=10, fontweight='bold')
    axes[idx].set_ylabel(label, fontsize=10, fontweight='bold')
    axes[idx].legend(title='Algorithm', fontsize=8)

plt.suptitle('Adaptive System Performance by Device Type', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'adaptive_by_device.png', dpi=300, bbox_inches='tight')
print("✓ Saved: adaptive_by_device.png")
plt.close()

print(f"\n✓ All figures saved to: {output_dir}")
print("="*70)
