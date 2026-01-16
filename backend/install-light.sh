#!/bin/bash
# Lightweight installation script that avoids downloading full PyTorch

echo "Installing lightweight dependencies..."

# Install basic requirements first
pip install -r requirements-light.txt

echo "Installing sentence-transformers with CPU-only PyTorch..."
# Install PyTorch CPU-only version explicitly
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install sentence-transformers
pip install sentence-transformers==2.3.1

# Install FAISS CPU
pip install faiss-cpu==1.13.2

echo "Installation complete!"
echo "Total download size: ~300MB (vs 900MB for full PyTorch)"
