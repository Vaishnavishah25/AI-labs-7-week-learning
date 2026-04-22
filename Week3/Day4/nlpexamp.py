# ── 1. Import Libraries ─────────────────────────────
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ── 2. Sample Dataset ───────────────────────────────
data = {
    "text": [
        "Win money now",
        "Limited offer just for you",
        "Call this number immediately",
        "Hi how are you",
        "Let's meet tomorrow",
        "Project meeting at 10am",
        "Congratulations you won a lottery",
        "Free entry in contest"
    ],
    "label": [1,1,1,0,0,0,1,1]   # 1 = spam, 0 = not spam
}

df = pd.DataFrame(data)

# ── 3. Split Data ───────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.25, random_state=42
)

# ── 4. TF-IDF Vectorization ─────────────────────────
vectorizer = TfidfVectorizer(stop_words='english')

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ── 5. Train Model ──────────────────────────────────
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# ── 6. Predict ──────────────────────────────────────
y_pred = model.predict(X_test_vec)

# ── 7. Evaluation ───────────────────────────────────
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ── 8. Test Custom Input ────────────────────────────
new_text = ["Free money offer now"]
new_vec = vectorizer.transform(new_text)
prediction = model.predict(new_vec)

print("\nPrediction for new text:", prediction)