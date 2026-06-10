"""Réentraînement automatique (SQUELETTE À COMPLÉTER → scripts/retrain.py).

Déclenché sur seuil de feedback. Réutilise la Pipeline M1 (preprocess.py).
Mini-cours : 03 (trigger), 04 (réentraînement + garde-fous).
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import joblib, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).parent))
from preprocess import (CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET_MAPPING,
                        build_preprocessor, load_dataset)

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
# TODO 1 — vos seuils d'éval (hérités M5-B2) : f1_macro, roc_auc, recall_default
THRESHOLDS = {}
RF_PARAMS = dict(n_estimators=200, max_depth=10, min_samples_leaf=10,
                 class_weight="balanced", random_state=42, n_jobs=-1)


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--min-feedback", type=int, default=200)
    args = p.parse_args()
    feedbacks = pd.read_csv(DATA / "feedbacks_simules.csv")
    # TODO 2 — GARDE-SEUIL : si len(feedbacks) < seuil → return 0 (skip, pas une erreur)
    # TODO 3 — build training set : train + lignes prod corrigées (jointure request_id)
    # TODO 4 — fit Pipeline(build_preprocessor(), RandomForestClassifier(**RF_PARAMS))
    # TODO 5 — CONTRACT TEST (proba dans [0,1]) puis ÉVALUATION (seuils) ;
    #          si violation → return 1 (bloque la release)
    # TODO 6 — sauvegarder v2.1.0 + métadonnées ; (en prod : git tag + push)
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
