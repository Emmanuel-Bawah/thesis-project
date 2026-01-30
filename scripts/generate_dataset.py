#!/usr/bin/env python3
"""
Dataset Generator for MSC Thesis
Generates 100,000 synthetic e-commerce transactions
"""

import random
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

print("=" * 60)
print("E-Commerce Transaction Dataset Generator")
print("=" * 60)
print()

TOTAL_TRANSACTIONS = 100000
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.20
TEST_RATIO = 0.10

MERCHANT_CATEGORIES = ['groceries', 'utilities', 'fashion', 'electronics', 'services']
DEVICE_TYPES = ['low-end', 'mid-range', 'high-end']
NETWORK_CONDITIONS = ['2G', '3G', '4G']

VALUE_DISTRIBUTIONS = {
    'low': (0.10, 10.00, 0.60),
    'medium': (10.01, 100.00, 0.30),
    'high': (100.01, 500.00, 0.10)
}

DEVICE_DISTRIBUTIONS = {
    'low-end': 0.50,
    'mid-range': 0.35,
    'high-end': 0.15
}

def generate_transaction_amount():
    rand = random.random()
    if rand < 0.60:
        return round(random.uniform(0.10, 10.00), 2)
    elif rand < 0.90:
        return round(random.uniform(10.01, 100.00), 2)
    else:
        return round(random.uniform(100.01, 500.00), 2)

def generate_device_type():
    rand = random.random()
    if rand < 0.50:
        return 'low-end'
    elif rand < 0.85:
        return 'mid-range'
    else:
        return 'high-end'

def get_device_specs(device_type):
    specs = {
        'low-end': random.choice([1, 2]),
        'mid-range': random.choice([3, 4]),
        'high-end': random.choice([6, 8, 12])
    }
    return specs[device_type]

def generate_transaction(transaction_id, timestamp):
    amount = generate_transaction_amount()
    merchant_category = random.choice(MERCHANT_CATEGORIES)
    device_type = generate_device_type()
    device_ram = get_device_specs(device_type)
    network_condition = random.choice(NETWORK_CONDITIONS)
    merchant_id = f"{merchant_category[:4].upper()}{random.randint(1000, 9999)}"
    
    return {
        'transaction_id': f'TXN{transaction_id:08d}',
        'timestamp': timestamp.isoformat(),
        'amount_usd': amount,
        'merchant_category': merchant_category,
        'merchant_id': merchant_id,
        'device_type': device_type,
        'device_ram_gb': device_ram,
        'network_condition': network_condition,
        'currency': 'USD',
        'country_code': random.choice(['GH', 'NG', 'KE', 'ZA', 'UG']),
    }

def generate_dataset(num_transactions):
    print(f"Generating {num_transactions:,} transactions...")
    transactions = []
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    
    for i in range(num_transactions):
        timestamp = start_date + timedelta(seconds=i * 5)
        transaction = generate_transaction(i + 1, timestamp)
        transactions.append(transaction)
        
        if (i + 1) % 10000 == 0:
            print(f"  Generated {i + 1:,} / {num_transactions:,}")
    
    print(f"✓ Generated {num_transactions:,} transactions\n")
    return transactions

def split_dataset(transactions, train_ratio, val_ratio, test_ratio):
    total = len(transactions)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)
    
    shuffled = transactions.copy()
    random.shuffle(shuffled)
    
    train_set = shuffled[:train_size]
    val_set = shuffled[train_size:train_size + val_size]
    test_set = shuffled[train_size + val_size:]
    
    print(f"Dataset split:")
    print(f"  Training:   {len(train_set):,} ({len(train_set)/total*100:.1f}%)")
    print(f"  Validation: {len(val_set):,} ({len(val_set)/total*100:.1f}%)")
    print(f"  Testing:    {len(test_set):,} ({len(test_set)/total*100:.1f}%)\n")
    
    return train_set, val_set, test_set

def save_to_csv(transactions, filename):
    if not transactions:
        return
    fieldnames = transactions[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)
    print(f"✓ Saved {len(transactions):,} to {filename}")

def analyze_dataset(transactions, name="Dataset"):
    print(f"\n{name} Statistics:")
    print("-" * 60)
    
    low = sum(1 for t in transactions if t['amount_usd'] < 10)
    med = sum(1 for t in transactions if 10 <= t['amount_usd'] <= 100)
    high = sum(1 for t in transactions if t['amount_usd'] > 100)
    
    print(f"Value: Low {low:,} ({low/len(transactions)*100:.1f}%) | Med {med:,} ({med/len(transactions)*100:.1f}%) | High {high:,} ({high/len(transactions)*100:.1f}%)")
    
    for dt in DEVICE_TYPES:
        count = sum(1 for t in transactions if t['device_type'] == dt)
        print(f"Device {dt}: {count:,} ({count/len(transactions)*100:.1f}%)")

def main():
    data_dir = Path.home() / 'thesis-project' / 'data' / 'raw'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Output: {data_dir}\n")
    
    start_time = datetime.now()
    all_transactions = generate_dataset(TOTAL_TRANSACTIONS)
    
    train_set, val_set, test_set = split_dataset(all_transactions, TRAIN_RATIO, VALIDATION_RATIO, TEST_RATIO)
    
    print("Saving datasets...")
    save_to_csv(all_transactions, data_dir / 'transactions_complete.csv')
    save_to_csv(train_set, data_dir / 'transactions_train.csv')
    save_to_csv(val_set, data_dir / 'transactions_validation.csv')
    save_to_csv(test_set, data_dir / 'transactions_test.csv')
    
    analyze_dataset(all_transactions, "Complete")
    analyze_dataset(train_set, "Training")
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("✓ Dataset Generation Complete!")
    print("=" * 60)
    print(f"Total: {TOTAL_TRANSACTIONS:,} | Time: {elapsed:.2f}s")
    print(f"Location: {data_dir}")
    print("=" * 60)

if __name__ == '__main__':
    main()
