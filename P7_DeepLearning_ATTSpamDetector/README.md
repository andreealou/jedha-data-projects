# P7 – Deep Learning: ATT Spam Detector
*A Deep Learning project using LSTM for real-time spam classification*

---

## 1. Project Overview

This project develops a complete NLP pipeline to classify SMS messages as **HAM (legitimate)** or **SPAM**, using a **Deep Learning LSTM model** implemented in TensorFlow/Keras.

Key features:
- Clean preprocessing pipeline  
- Tokenization and vectorization with `TextVectorization`
- Embedding + LSTM neural architecture
- Early stopping and training curve analysis
- Evaluation with precision, recall, F1-score, confusion matrix, AUC-PR
- Error analysis (false positives & false negatives)
- Real-time prediction tool
- Embedding export for visualization (TensorFlow Projector)

---

## 2. Dataset

Dataset: SMS Spam Collection (UCI ML Repository)

- Total messages: **5,572**
- HAM: **4,825**
- SPAM: **747**

Columns:
- `v1` → label (`ham` / `spam`)
- `v2` → SMS text

Imbalanced dataset → F1-score and AUC-PR crucial.

---

## 3. Preprocessing Steps

- Lowercasing  
- Removing punctuation (keeping apostrophes)  
- Removing extra spaces  
- Keeping digits (important for spam patterns)  
- Removing accents  
- Mapping labels → numeric (`ham=0`, `spam=1`)

Example:

**Before:**  
`"Free entry in 2 a wkly comp to win FA Cup final tkts!"`

**After:**  
`"free entry in 2 a wkly comp to win fa cup final tkts"`

---

## 4. Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_message"], df["label_num"],
    test_size=0.2,
    stratify=df["label_num"],
    random_state=42
)
```

---

## 5. Text Vectorization

```python
vectorizer = TextVectorization(
    max_tokens=10_000,
    output_mode="int",
    output_sequence_length=40,
    standardize="lower_and_strip_punctuation",
    split="whitespace"
)

vectorizer.adapt(X_train.values)
```

The vectorizer transforms SMS text → integer sequences.

---

## 6. Model Architecture (LSTM)

```python
model = Sequential([
    vectorizer,
    Embedding(input_dim=10_000, output_dim=128, mask_zero=True),
    LSTM(64),
    Dropout(0.3),
    Dense(1, activation="sigmoid")
])
```

Why LSTM?

- SMS messages are **short sequences** → word order matters  
- LSTMs capture **context** efficiently  
- Lighter & more interpretable than transformers  
- Excellent performance for this dataset size

---

## 7. Training Configuration

```python
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy", tf.keras.metrics.AUC(curve="PR")]
)

es = EarlyStopping(
    monitor="val_loss",
    patience=2,
    restore_best_weights=True
)

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=10,
    batch_size=64,
    callbacks=[es]
)
```

- Training and validation curves converge → no overfitting  
- EarlyStopping stops at ~epoch 5–6 (optimal point)

---

## 8. Evaluation Metrics

### Classification Report

```python
print(classification_report(y_test, y_pred, target_names=["ham", "spam"]))
```

Results:
- HAM: precision/recall/F1 ≈ **0.99**
- SPAM: precision/recall/F1 ≈ **0.95**
- Accuracy ≈ **0.99**

### Confusion Matrix

False positives and false negatives are minimal.

### Precision–Recall Curve

AUC-PR ≈ **0.98** → excellent for imbalanced datasets.

---

## 9. Error Analysis

Insights:
- **False Positives:** friendly messages containing promo-style words.
- **False Negatives:** soft spam lacking typical spam keywords.

Actionable understanding for future tuning.

---

## 10. Real-Time Prediction Tool

```python
def predict_messages(messages):
    messages = tf.constant(messages, dtype=tf.string)
    proba = model.predict(messages).ravel()
    pred = (proba >= 0.5).astype(int)
    return list(zip(messages.numpy(), pred, proba))
```

Color-coded display:
- Green → HAM  
- Red → SPAM  

Useful for demos and deployment.

---

## 11. Embedding Export (TensorFlow Projector)

```python
embedding_layer = model.get_layer("embedding")
weights = embedding_layer.get_weights()[0]
vocab = vectorizer.get_vocabulary()

with open("meta.tsv", "w") as m, open("vecs.tsv", "w") as v:
    for i in range(1, 1001):
        m.write(vocab[i] + "\n")
        v.write("\t".join([str(x) for x in weights[i]]) + "\n")
```

Explore embeddings at https://projector.tensorflow.org/

Clusters observed:
- promotional words  
- frequent function words  
- numbers  
- names  

---

## 12. Future Work

- Try hybrid **CNN + LSTM** models  
- Fine-tune thresholds depending on business needs  
- Experiment with transformers (BERT, DistilBERT)  
- Deploy as API or Streamlit/Flask web app  

---

## 13. Tech Stack

- Python 3.10  
- TensorFlow / Keras  
- Pandas / NumPy  
- Scikit-Learn  
- Matplotlib / Seaborn  



