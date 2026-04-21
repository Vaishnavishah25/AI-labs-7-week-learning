# ── Decision Tree Classification ─────────────────────────────

import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ── 1. Load dataset ─────────────────────────────────────────
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print(f"Dataset shape: {X.shape}")
print(f"Classes: {data.target_names}")

# ── 2. Train-test split ─────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Train Decision Tree ──────────────────────────────────
tree = DecisionTreeClassifier(
    criterion='gini',   # or 'entropy'
    max_depth=4,        # control overfitting
    random_state=42
)

tree.fit(X_train, y_train)

# ── 4. Predict ──────────────────────────────────────────────
y_pred = tree.predict(X_test)

# ── 5. Evaluation ───────────────────────────────────────────
print("\n── Accuracy ────────────────────────────")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

print("\n── Classification Report ───────────────")
print(classification_report(y_test, y_pred, target_names=data.target_names))

print("\n── Confusion Matrix ────────────────────")
print(confusion_matrix(y_test, y_pred))