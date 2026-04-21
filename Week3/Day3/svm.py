ull working code — copy and run

# ── SVM Classification ─────────────────────────────────────────────
# Dataset: Breast Cancer (569 samples, 30 features, binary labels)
# Goal: Classify tumors as malignant (1) or benign (0)

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (classification_report,
                              confusion_matrix,
                              accuracy_score)

# ── 1. Load dataset ─────────────────────────────────────────────────
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print(f"Dataset shape: {X.shape}")        # (569, 30)
print(f"Classes: {data.target_names}")    # ['malignant' 'benign']
print(y.value_counts())

# ── 2. Train/test split ──────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)# ── 3. Feature scaling (CRITICAL for SVM) ───────────────────────────
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)  # fit on train only
X_test_sc  = scaler.transform(X_test)       # transform test with same scaler

# ── 4. Train SVM with RBF kernel ────────────────────────────────────
svm = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm.fit(X_train_sc, y_train)

# ── 5. Predict and evaluate ──────────────────────────────────────────
y_pred = svm.predict(X_test_sc)

print("\n── Accuracy ────────────────────────────")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

print("\n── Classification Report ───────────────")
print(classification_report(y_test, y_pred,
      target_names=data.target_names))

print("\n── Confusion Matrix ────────────────────")
print(confusion_matrix(y_test, y_pred))

# ── 6. Kernel comparison ─────────────────────────────────────────────
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
print("\n── Kernel Comparison ───────────────────") for k in kernels:
    m = SVC(kernel=k, C=1.0, gamma='scale', random_state=42)
    m.fit(X_train_sc, y_train)
    acc = accuracy_score(y_test, m.predict(X_test_sc))
    print(f"  {k:10} → Accuracy: {acc:.4f}")

# ── 7. Hyperparameter tuning with GridSearchCV ───────────────────────
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C':     [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01],
    'kernel':['rbf', 'linear']
}
grid = GridSearchCV(
    SVC(random_state=42), param_grid,
    cv=5, scoring='accuracy', n_jobs=-1, verbose=0
)
grid.fit(X_train_sc, y_train)

print("\n── GridSearch Best Params ──────────────")
print(f"Best params:   {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.4f}")

best_pred = grid.best_estimator_.predict(X_test_sc)
print(f"Test accuracy: {accuracy_score(y_test, best_pred):.4f}")