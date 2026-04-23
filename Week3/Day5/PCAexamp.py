# ── 1. Import Libraries ─────────────────────────────
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ── 2. Load Dataset ─────────────────────────────────
data = load_iris()
X = data.data
y = data.target

print("Original Shape:", X.shape)

# ── 3. Standardize Data (VERY IMPORTANT) ────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ── 4. Apply PCA ───────────────────────────────────
pca = PCA(n_components=2)   # reduce to 2 features
X_pca = pca.fit_transform(X_scaled)

# ── 5. Output Results ───────────────────────────────
print("Reduced Shape:", X_pca.shape)

print("\nPCA Data (first 5 rows):")
print(X_pca[:5])

# ── 6. Explained Variance ───────────────────────────
print("\nExplained Variance Ratio:")
print(pca.explained_variance_ratio_)