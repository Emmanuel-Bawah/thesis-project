from src.utils.config_utils import load_config
from src.utils.random_utils import set_global_seed
from src.utils.results_utils import create_run_id, save_run_csv, save_run_summary


def run_experiments():
    config = load_config()
    seed = 42
    set_global_seed(seed)

    run_id = create_run_id(1)
    rows = []

    dataset_cfg = config["dataset"]
    crypto_cfg = config["crypto"]
    exp_cfg = config["experiment"]

    for scheme in crypto_cfg["schemes"]:
        scheme_name = scheme["name"]

        for device_type in dataset_cfg["device_distribution"].keys():
            for network in dataset_cfg["network_distribution"].keys():
                for amount_band in dataset_cfg["amount_ranges"].keys():
                    for i in range(exp_cfg["n_runs"]):

                        # Placeholder metrics (replace with real measurements later)
                        encryption_time_ms = 1.0
                        decryption_time_ms = 0.9
                        keygen_time_ms = 5.0
                        memory_mb = 12.0

                        rows.append({
                            "scheme": scheme_name,
                            "device_type": device_type,
                            "network": network,
                            "transaction_amount_band": amount_band,
                            "run_id": run_id,
                            "seed": seed,
                            "encryption_time_ms": encryption_time_ms,
                            "decryption_time_ms": decryption_time_ms,
                            "keygen_time_ms": keygen_time_ms,
                            "memory_mb": memory_mb,
                        })

    save_run_csv(run_id, rows)
    save_run_summary(run_id, seed, notes="Test run")


if __name__ == "__main__":
    run_experiments()
