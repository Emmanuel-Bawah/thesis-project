# METHODOLOGY

## Experimental Design

### 3.1 System Architecture

This research implemented and evaluated five encryption systems on ARM64 architecture:

1. **Kyber-768 + AES-256-GCM** (Proposed System)
   - NIST Level 3 post-quantum security
   - Hybrid encryption: Kyber KEM + AES symmetric
   - Target: Optimal security/performance balance

2. **RSA-2048 + AES-256-GCM** (Baseline 1)
   - Classical public-key cryptography
   - Industry standard comparison
   - Vulnerable to quantum attacks

3. **ECDH-P256 + AES-256-GCM** (Baseline 2)
   - Elliptic Curve Diffie-Hellman
   - Modern classical alternative
   - Vulnerable to quantum attacks

4. **Kyber-512 + AES-256-GCM** (Baseline 3)
   - NIST Level 1 post-quantum security
   - Lighter variant for comparison
   - Performance vs security trade-off

5. **Adaptive Post-Quantum System** (Novel Contribution)
   - Intelligent selector between Kyber-768 and Kyber-512
   - Context-aware based on device, network, transaction
   - 100% post-quantum secure

### 3.2 Hardware Platform

**AWS EC2 Instance:**
- Instance Type: t4g.micro
- Processor: ARM Graviton2 (64-bit ARM)
- vCPUs: 2
- RAM: 1 GB
- OS: Ubuntu 24.04 LTS
- Architecture: aarch64

**Rationale:** ARM architecture represents mobile devices prevalent in African markets.

### 3.3 Software Implementation

**Programming Language:** Python 3.12

**Key Libraries:**
- liboqs-python 0.14.1 (Post-quantum cryptography)
- pycryptodome 3.20.0 (AES-GCM symmetric encryption)
- cryptography 43.0.3 (ECDH implementation)

**Virtual Environments:**
- Isolated environments for each system
- Prevents dependency conflicts
- Reproducible installations

### 3.4 Dataset

**Synthetic E-Commerce Transactions:**
- Total: 100,000 transactions
- Split: 70% training, 20% validation, 10% test
- Transaction values: $0.50 to $500.00
- Merchant categories: 5 (groceries, utilities, fashion, electronics, services)
- Countries: Ghana, Nigeria, Kenya, South Africa, Uganda
- Payment methods: Mobile wallets, cards, bank transfers

### 3.5 Test Configurations

**Device Types:**
- Low-end: 1,536 MB RAM (budget smartphones)
- Mid-range: 3,584 MB RAM (average smartphones)
- High-end: 7,168 MB RAM (flagship devices)

**Network Conditions:**
- 2G: 50 Kbps bandwidth, 500ms latency, 3% packet loss
- 3G: 384 Kbps bandwidth, 100ms latency, 1.5% packet loss
- 4G: 10 Mbps bandwidth, 50ms latency, 0.5% packet loss

**Transaction Amounts:**
- Low-value: $5 (airtime, street food)
- Medium-value: $25 (utilities, transport)
- High-value: $150 (rent, electronics)

### 3.6 Testing Methodology

**Baseline Testing:**
- 4 fixed systems (Kyber-768, RSA-2048, ECDH-P256, Kyber-512)
- Configuration: Mid-range device, 4G network
- Runs: 30 per system
- Total: 120 tests

**Adaptive Testing:**
- Adaptive post-quantum system
- 3 devices × 3 networks × 3 amounts
- Runs: 10 per configuration
- Total: 270 tests

**Combined Dataset:** 390 total tests

### 3.7 Performance Metrics

**Primary Metrics:**
1. Key Generation Time (milliseconds)
2. Encryption Time (milliseconds)
3. Decryption Time (milliseconds)

**Secondary Metrics:**
1. Key sizes (bytes)
2. Data integrity verification (100% pass rate)
3. Algorithm selection distribution (adaptive system)

### 3.8 Statistical Analysis

**Methods:**
1. **One-way ANOVA:** Compare means across systems
2. **Tukey's HSD:** Pairwise post-hoc comparisons
3. **95% Confidence Intervals:** Precision estimation
4. **Cohen's d:** Effect size calculation

**Significance Level:** α = 0.05

**Software:** Python with scipy.stats, pandas, numpy

### 3.9 Adaptive Selection Logic

**Decision Rules:**
```
Rule 1: High-Value Security
IF transaction_amount ≥ $100
THEN select Kyber-768 (NIST Level 3)

Rule 2: Device Optimization
IF device_ram ≤ 2048 MB
THEN select Kyber-512 (NIST Level 1)

Rule 3: Network Adaptation
IF device_ram ≤ 4096 MB AND network = "2G"
THEN select Kyber-512

Rule 4: Default Optimal
ELSE select Kyber-768
```

### 3.10 Reproducibility

**Version Control:** Git/GitHub
**Repository:** github.com/Emmanuel-Bawah/thesis-project
**Documentation:** Complete code with comments
**Data:** All test results saved as CSV
**Figures:** High-resolution (300 DPI) publication-ready

### 3.11 Ethical Considerations

- No real user data collected
- Synthetic transactions only
- Open-source implementation
- No privacy concerns

### 3.12 Limitations

1. **Simulated Environment:** Real mobile devices not tested
2. **Network Simulation:** Software-based, not actual mobile networks
3. **Dataset:** Synthetic, not real transaction data
4. **Single Platform:** ARM only, x86 not tested
5. **Time Constraint:** 6-day accelerated timeline

---

**End of Methodology**
