from pathlib import Path
import numpy as np
import pandas as pd

from src.utils.config_utils import load_config
from src.utils.random_utils import set_global_seed


def generate_transactions(seed: int = 42):
    """
    Generate synthetic e-commerce transactions based on config.yaml
    and save to data/raw/transactions.csv.
    """
    # 1) Load config and set seed
    config = load_config()
    set_global_seed(seed)

    dataset_cfg = config["dataset"]

    n_samples = dataset_cfg["n_samples"]
    amount_ranges = dataset_cfg["amount_ranges"]
    device_dist = dataset_cfg["device_distribution"]
    network_dist = dataset_cfg["network_distribution"]

    # 2) Prepare distributions

    # Device types and probabilities
    device_types = list(device_dist.keys())
    device_probs = np.array(list(device_dist.values()), dtype=float)
    device_probs = device_probs / device_probs.sum()  # just in case they don't sum exactly to 1

    # Network types and probabilities
    network_types = list(network_dist.keys())
    network_probs = np.array(list(network_dist.values()), dtype=float)
    network_probs = network_probs / network_probs.sum()

    # Amount bands (low/medium/high). Here we treat them as equally likely,
    # but you could add a distribution in config.yaml later if needed.
    amount_bands = list(amount_ranges.keys())
    band_probs = np.ones(len(amount_bands), dtype=float) / len(amount_bands)

    # Simple merchant categories (you can refine later or move to config)
    merchant_categories = [
        "airtime",
        "utilities",
        "shopping",
        "transport",
        "food",
        "subscriptions",
    ]
    merchant_probs = np.ones(len(merchant_categories), dtype=float) / len(merchant_categories)

    # 3) Sample each attribute

    # Transaction IDs
    txn_ids = np.arange(1, n_samples + 1)

    # Choose amount band per transaction
    chosen_bands = np.random.choice(amount_bands, size=n_samples, p=band_probs)

    # For each band, draw a continuous amount within its [min, max] range
    amounts = np.empty(n_samples, dtype=float)
    for i, band in enumerate(chosen_bands):
        low, high = amount_ranges[band]
        amounts[i] = np.random.uniform(low, high)

    # Device type per transaction
    device_choices = np.random.choice(device_types, size=n_samples, p=device_probs)

    # Network type per transaction
    network_choices = np.random.choice(network_types, size=n_samples, p=network_probs)

    # Merchant category per transaction
    merchant_choices = np.random.choice(merchant_categories, size=n_samples, p=merchant_probs)

    # 4) Build DataFrame
    df = pd.DataFrame(
        {
            "txn_id": txn_ids,
            "amount": amounts,
            "amount_band": chosen_bands,
            "merchant_category": merchant_choices,
            "device_type": device_choices,
            "network_type": network_choices,
        }
    )

    # 5) Save to data/raw/transactions.csv
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "transactions.csv"

    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} transactions to {out_path}")


if __name__ == "__main__":
    generate_transactions()
