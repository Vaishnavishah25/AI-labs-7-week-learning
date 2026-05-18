import numpy as np
import math

# ── 1. Input Text ─────────────────────────────
documents = ["AI is powerful", "AI is future"]

# ── 2. Tokenization (lowercase + split) ──────
docs = [doc.lower().split() for doc in documents]

# ── 3. Build Vocabulary ─────────────────────
vocab = sorted(list(set(word for doc in docs for word in doc)))
print("Vocabulary:", vocab)

# ── 4. Compute IDF ──────────────────────────
N = len(docs)
idf = {}

for word in vocab:
    df = sum(1 for doc in docs if word in doc)
    idf[word] = math.log((1 + N) / (1 + df)) + 1

print("\nIDF values:")
for k, v in idf.items():
    print(f"{k}: {round(v,3)}")

# ── 5. Compute TF-IDF ───────────────────────
tfidf_vectors = []

for doc in docs:
    tfidf = []
    total_words = len(doc)
    
    for word in vocab:
        # TF
        tf = doc.count(word) / total_words
        
        # TF-IDF
        tfidf_value = tf * idf[word]
        tfidf.append(tfidf_value)
    
    # ── 6. Normalize (L2) ───────────────────
    norm = math.sqrt(sum(x**2 for x in tfidf))
    tfidf = [x / norm if norm != 0 else 0 for x in tfidf]
    
    tfidf_vectors.append(tfidf)

# ── 7. Output ───────────────────────────────
print("\nTF-IDF Matrix:")
for vec in tfidf_vectors:
    print([round(v, 3) for v in vec])