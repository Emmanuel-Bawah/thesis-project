#!/bin/bash
# Virtual Environments Setup Script for ARM64
set -e
echo "=========================================="
echo "Virtual Environments Setup for ARM64"
echo "=========================================="
cd ~/thesis-project
mkdir -p venvs && cd venvs

echo "Step 1/5: Creating Kyber-768 environment..."
python3 -m venv kyber768
source kyber768/bin/activate
pip install --upgrade pip setuptools wheel -q
pip install pycryptodome cryptography requests flask flask-restful psutil memory-profiler numpy pandas pytest -q
pip freeze > ../kyber768-requirements.txt
deactivate
echo "✓ kyber768 done"

echo "Step 2/5: Creating RSA-2048 environment..."
python3 -m venv rsa2048
source rsa2048/bin/activate
pip install --upgrade pip setuptools wheel -q
pip install pycryptodome cryptography requests flask flask-restful psutil memory-profiler numpy pandas pytest -q
pip freeze > ../rsa2048-requirements.txt
deactivate
echo "✓ rsa2048 done"

echo "Step 3/5: Creating ECDH environment..."
python3 -m venv ecdh
source ecdh/bin/activate
pip install --upgrade pip setuptools wheel -q
pip install cryptography ecdsa requests flask flask-restful psutil memory-profiler numpy pandas pytest -q
pip freeze > ../ecdh-requirements.txt
deactivate
echo "✓ ecdh done"

echo "Step 4/5: Creating Kyber-512 environment..."
python3 -m venv kyber512
source kyber512/bin/activate
pip install --upgrade pip setuptools wheel -q
pip install pycryptodome cryptography requests flask flask-restful psutil memory-profiler numpy pandas pytest -q
pip freeze > ../kyber512-requirements.txt
deactivate
echo "✓ kyber512 done"

echo "Step 5/5: Creating Testing environment..."
python3 -m venv testing
source testing/bin/activate
pip install --upgrade pip setuptools wheel -q
pip install numpy pandas matplotlib seaborn plotly scipy statsmodels scikit-learn jupyter notebook pytest requests psutil -q
pip freeze > ../testing-requirements.txt
deactivate
echo "✓ testing done"

cd ~/thesis-project
cat > activate-kyber768.sh << 'INNER_EOF'
#!/bin/bash
source ~/thesis-project/venvs/kyber768/bin/activate
export PROJECT_ROOT=~/thesis-project
echo "✓ Kyber-768 environment activated"
INNER_EOF
chmod +x activate-kyber768.sh

cat > activate-rsa2048.sh << 'INNER_EOF'
#!/bin/bash
source ~/thesis-project/venvs/rsa2048/bin/activate
export PROJECT_ROOT=~/thesis-project
echo "✓ RSA-2048 environment activated"
INNER_EOF
chmod +x activate-rsa2048.sh

cat > activate-ecdh.sh << 'INNER_EOF'
#!/bin/bash
source ~/thesis-project/venvs/ecdh/bin/activate
export PROJECT_ROOT=~/thesis-project
echo "✓ ECDH environment activated"
INNER_EOF
chmod +x activate-ecdh.sh

cat > activate-kyber512.sh << 'INNER_EOF'
#!/bin/bash
source ~/thesis-project/venvs/kyber512/bin/activate
export PROJECT_ROOT=~/thesis-project
echo "✓ Kyber-512 environment activated"
INNER_EOF
chmod +x activate-kyber512.sh

cat > activate-testing.sh << 'INNER_EOF'
#!/bin/bash
source ~/thesis-project/venvs/testing/bin/activate
export PROJECT_ROOT=~/thesis-project
echo "✓ Testing environment activated"
INNER_EOF
chmod +x activate-testing.sh

echo ""
echo "=========================================="
echo "✓ ALL 5 VIRTUAL ENVIRONMENTS CREATED!"
echo "=========================================="
echo "To activate: source activate-<name>.sh"
