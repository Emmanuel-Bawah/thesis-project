#!/usr/bin/env python3
"""
Statistical Analysis of Encryption Systems
Performs ANOVA, Tukey's HSD, confidence intervals, and effect sizes
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class StatisticalAnalyzer:
    """Comprehensive statistical analysis for encryption systems"""
    
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)
        self.data = None
        self.systems = []
        
    def load_data(self):
        """Load baseline and adaptive test results"""
        print("Loading data...")
        
        # Load baseline tests (120 tests)
        baseline_files = list(self.results_dir.glob('standard_test_*.csv'))
        if baseline_files:
            baseline_df = pd.read_csv(baseline_files[0])
            print(f"  ✓ Loaded {len(baseline_df)} baseline tests")
        else:
            print("  ✗ No baseline data found")
            baseline_df = pd.DataFrame()
        
        # Load adaptive tests (270 tests)
        adaptive_files = list(self.results_dir.glob('adaptive_test_*.csv'))
        if adaptive_files:
            adaptive_df = pd.read_csv(adaptive_files[0])
            # Rename for consistency
            adaptive_df['system'] = 'Adaptive-' + adaptive_df['selected_algorithm']
            print(f"  ✓ Loaded {len(adaptive_df)} adaptive tests")
        else:
            print("  ✗ No adaptive data found")
            adaptive_df = pd.DataFrame()
        
        # Combine
        self.data = pd.concat([baseline_df, adaptive_df], ignore_index=True)
        self.systems = sorted(self.data['system'].unique())
        
        print(f"  ✓ Total: {len(self.data)} tests across {len(self.systems)} systems")
        print(f"  Systems: {', '.join(self.systems)}")
        
    def perform_anova(self, metric='keygen_time_ms'):
        """Perform one-way ANOVA"""
        print(f"\n{'='*70}")
        print(f"ANOVA: {metric}")
        print('='*70)
        
        groups = [self.data[self.data['system'] == sys][metric].values 
                  for sys in self.systems]
        
        f_stat, p_value = f_oneway(*groups)
        
        print(f"F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_value:.4e}")
        
        if p_value < 0.05:
            print("✓ SIGNIFICANT: Systems differ significantly (p < 0.05)")
        else:
            print("✗ NOT SIGNIFICANT: No significant difference (p ≥ 0.05)")
        
        return f_stat, p_value
    
    def tukey_hsd(self, metric='keygen_time_ms'):
        """Perform Tukey's HSD pairwise comparisons"""
        print(f"\n{'='*70}")
        print(f"TUKEY'S HSD: {metric}")
        print('='*70)
        
        from scipy.stats import tukey_hsd
        
        # Prepare data for Tukey
        groups = [self.data[self.data['system'] == sys][metric].values 
                  for sys in self.systems]
        
        try:
            result = tukey_hsd(*groups)
            
            print("\nPairwise Comparisons:")
            print(f"{'System 1':<20} {'System 2':<20} {'Mean Diff':>12} {'Significant':>12}")
            print('-'*70)
            
            comparisons = []
            for i, sys1 in enumerate(self.systems):
                for j, sys2 in enumerate(self.systems):
                    if i < j:
                        mean1 = self.data[self.data['system'] == sys1][metric].mean()
                        mean2 = self.data[self.data['system'] == sys2][metric].mean()
                        diff = abs(mean1 - mean2)
                        
                        # Check if significant
                        significant = result.pvalue[i, j] < 0.05
                        sig_str = "YES" if significant else "NO"
                        
                        print(f"{sys1:<20} {sys2:<20} {diff:>12.2f} {sig_str:>12}")
                        
                        comparisons.append({
                            'system1': sys1,
                            'system2': sys2,
                            'mean_diff': diff,
                            'p_value': result.pvalue[i, j],
                            'significant': significant
                        })
            
            return comparisons
            
        except Exception as e:
            print(f"Error in Tukey's HSD: {e}")
            print("Performing manual pairwise comparisons instead...")
            
            # Manual pairwise t-tests
            comparisons = []
            for i, sys1 in enumerate(self.systems):
                for j, sys2 in enumerate(self.systems):
                    if i < j:
                        data1 = self.data[self.data['system'] == sys1][metric].values
                        data2 = self.data[self.data['system'] == sys2][metric].values
                        
                        t_stat, p_value = stats.ttest_ind(data1, data2)
                        mean_diff = abs(data1.mean() - data2.mean())
                        significant = p_value < 0.05
                        
                        print(f"{sys1:<20} {sys2:<20} {mean_diff:>12.2f} {'YES' if significant else 'NO':>12}")
                        
                        comparisons.append({
                            'system1': sys1,
                            'system2': sys2,
                            'mean_diff': mean_diff,
                            'p_value': p_value,
                            'significant': significant
                        })
            
            return comparisons
    
    def confidence_intervals(self, metric='keygen_time_ms', confidence=0.95):
        """Calculate 95% confidence intervals"""
        print(f"\n{'='*70}")
        print(f"95% CONFIDENCE INTERVALS: {metric}")
        print('='*70)
        
        print(f"{'System':<25} {'Mean':>10} {'95% CI':>25}")
        print('-'*70)
        
        results = {}
        for system in self.systems:
            data = self.data[self.data['system'] == system][metric].values
            mean = data.mean()
            sem = stats.sem(data)
            ci = stats.t.interval(confidence, len(data)-1, loc=mean, scale=sem)
            
            print(f"{system:<25} {mean:>10.2f} [{ci[0]:>8.2f}, {ci[1]:>8.2f}]")
            
            results[system] = {
                'mean': mean,
                'ci_lower': ci[0],
                'ci_upper': ci[1]
            }
        
        return results
    
    def cohen_d(self, metric='keygen_time_ms'):
        """Calculate Cohen's d effect sizes"""
        print(f"\n{'='*70}")
        print(f"COHEN'S D EFFECT SIZES: {metric}")
        print('='*70)
        
        # Compare Adaptive systems to baselines
        adaptive_systems = [s for s in self.systems if 'Adaptive' in s]
        baseline_systems = [s for s in self.systems if 'Adaptive' not in s]
        
        print(f"{'Adaptive System':<25} {'vs':<5} {'Baseline':<15} {'Cohen\'s d':>12} {'Effect':>12}")
        print('-'*70)
        
        for adap in adaptive_systems:
            data1 = self.data[self.data['system'] == adap][metric].values
            
            for baseline in baseline_systems:
                data2 = self.data[self.data['system'] == baseline][metric].values
                
                # Calculate Cohen's d
                mean1, mean2 = data1.mean(), data2.mean()
                std1, std2 = data1.std(), data2.std()
                pooled_std = np.sqrt((std1**2 + std2**2) / 2)
                
                d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0
                
                # Interpret effect size
                if abs(d) < 0.2:
                    effect = "Small"
                elif abs(d) < 0.8:
                    effect = "Medium"
                else:
                    effect = "Large"
                
                print(f"{adap:<25} vs  {baseline:<15} {d:>12.4f} {effect:>12}")
    
    def summary_statistics(self):
        """Generate summary statistics table"""
        print(f"\n{'='*70}")
        print("SUMMARY STATISTICS")
        print('='*70)
        
        metrics = ['keygen_time_ms', 'encryption_time_ms', 'decryption_time_ms']
        
        for metric in metrics:
            print(f"\n{metric.replace('_', ' ').title()}:")
            print(f"{'System':<25} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10} {'n':>6}")
            print('-'*70)
            
            for system in self.systems:
                data = self.data[self.data['system'] == system][metric]
                print(f"{system:<25} {data.mean():>10.2f} {data.std():>10.2f} "
                      f"{data.min():>10.2f} {data.max():>10.2f} {len(data):>6}")
    
    def run_full_analysis(self):
        """Run complete statistical analysis"""
        print("\n" + "="*70)
        print("COMPREHENSIVE STATISTICAL ANALYSIS")
        print("="*70)
        
        self.load_data()
        
        metrics = ['keygen_time_ms', 'encryption_time_ms', 'decryption_time_ms']
        
        for metric in metrics:
            print(f"\n\n{'#'*70}")
            print(f"# METRIC: {metric.replace('_', ' ').upper()}")
            print('#'*70)
            
            self.perform_anova(metric)
            self.tukey_hsd(metric)
            self.confidence_intervals(metric)
            self.cohen_d(metric)
        
        self.summary_statistics()
        
        print("\n" + "="*70)
        print("✓ Statistical analysis complete!")
        print("="*70)


def main():
    results_dir = Path.home() / 'thesis-project' / 'data' / 'results'
    
    analyzer = StatisticalAnalyzer(results_dir)
    analyzer.run_full_analysis()


if __name__ == '__main__':
    main()
