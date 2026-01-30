# MSC Thesis: Post-Quantum E-Commerce Encryption on ARM

**Student:** Emmanuel Bawah  
**Institution:** [Kwame Nkrumah University of Science and Technology]  
**Architecture:** AWS t4g.micro (ARM64)

## Project Overview
Adaptive Post-Quantum Encryption for Mobile E-Commerce: 
A Performance-Optimized Kyber Implementation for African Payment Systems

## Systems Under Test
1. **Proposed:** Kyber-768 + AES-256-GCM
2. **Baseline 1:** RSA-2048 + AES-256
3. **Baseline 2:** ECDH-P256 + AES-256
4. **Baseline 3:** Kyber-512 + AES-256

## Repository Structure
- `src/` - Implementation code for all systems
- `data/` - Datasets and experimental results
- `venvs/` - Python virtual environments
- `scripts/` - Automation and testing scripts
- `docs/` - Documentation, diagrams, and figures
- `notebooks/` - Jupyter notebooks for analysis

## Environment
- Platform: AWS EC2 t4g.micro
- OS: Ubuntu 24.04 LTS ARM64
- Python: 3.12+
- Architecture: aarch64

Created: $(date)
