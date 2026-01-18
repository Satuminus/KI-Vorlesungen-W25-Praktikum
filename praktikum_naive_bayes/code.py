#!/usr/bin/env python3

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "spam_ham_dataset.csv")



def load_spam_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[["text", "label"]]
    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(str)
    return df


def top_terms_per_class(vectorizer: CountVectorizer, nb: MultinomialNB, class_label: str, k: int = 20):
    feature_names = np.array(vectorizer.get_feature_names_out())
    classes = nb.classes_
    i = np.where(classes == class_label)[0][0]
    logp = nb.feature_log_prob_[i]
    top_idx = np.argsort(logp)[-k:][::-1]
    return feature_names[top_idx]


def most_indicative_terms(vectorizer: CountVectorizer, nb: MultinomialNB, pos_class: str, neg_class: str, k: int = 25):
    feature_names = np.array(vectorizer.get_feature_names_out())
    classes = nb.classes_
    i_pos = np.where(classes == pos_class)[0][0]
    i_neg = np.where(classes == neg_class)[0][0]
    log_odds = nb.feature_log_prob_[i_pos] - nb.feature_log_prob_[i_neg]
    top_pos = np.argsort(log_odds)[-k:][::-1]
    top_neg = np.argsort(log_odds)[:k]
    return feature_names[top_pos], feature_names[top_neg]


def main():
    df = load_spam_dataset(CSV_PATH)

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    clf = Pipeline([
        ("bow", CountVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2
        )),
        ("nb", MultinomialNB(alpha=1.0))
    ])

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
    report = classification_report(y_test, y_pred, digits=4)

    print("=== Evaluation ===")
    print(f"Accuracy: {acc:.4f}")
    print("\nConfusion matrix (rows=true [ham, spam], cols=pred [ham, spam])")
    print(cm)
    print("\nClassification report:\n")
    print(report)

    vectorizer = clf.named_steps["bow"]
    nb = clf.named_steps["nb"]

    print("\n=== Wichtigste Begriffe pro Klasse (nach log P(w | Klasse)) ===")
    for c in nb.classes_:
        terms = top_terms_per_class(vectorizer, nb, c, k=20)
        print(f"\nTop 20 Begriffe für Klasse '{c}':")

        for t in terms:
            print(f"- {t}")

    print("\n=== Am stärksten unterscheidende Begriffe (Log-Odds) ===")
    spam_terms, ham_terms = most_indicative_terms(
        vectorizer, nb,
        pos_class="spam",
        neg_class="ham",
        k=25
    )

    print("\nStark indikativ für spam:")
    for t in spam_terms:
        print(f"- {t}")

    print("\nStark indikativ für ham:")

    for t in ham_terms:
        print(f"- {t}")


if __name__ == "__main__":
    main()
