# ── 1. Import Libraries ─────────────────────────────
import numpy as np
import matplotlib.pyplot as plt

# ── 2. Sample Data ─────────────────────────────────
# y = 2x + 1 (approx)
X = np.array([1, 2, 3, 4, 5])
y = np.array([3, 5, 7, 9, 11])

# ── 3. Initialize Parameters ───────────────────────
m = 0   # slope
b = 0   # intercept

learning_rate = 0.01
epochs = 1000
n = len(X)

# ── 4. Gradient Descent Loop ───────────────────────
for i in range(epochs):
    
    y_pred = m * X + b   # prediction
    
    # Compute gradients
    dm = (-2/n) * sum(X * (y - y_pred))
    db = (-2/n) * sum(y - y_pred)
    
    # Update parameters
    m = m - learning_rate * dm
    b = b - learning_rate * db
    
    # Print loss occasionally
    if i % 100 == 0:
        loss = np.mean((y - y_pred) ** 2)
        print(f"Epoch {i}, Loss: {loss:.4f}")

# ── 5. Final Output ───────────────────────────────
print("\nFinal parameters:")
print("m =", m)
print("b =", b)

# ── 6. Plot Result ────────────────────────────────
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X, m*X + b, color='red', label='Best Fit Line')
plt.legend()
plt.title("Gradient Descent Linear Regression")
plt.show()