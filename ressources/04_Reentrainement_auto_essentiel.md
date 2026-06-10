# Réentraînement automatique + garde-fous — Mini-cours

> Brief associé : M6-B2
> Durée de lecture : ~25 min
> Pré-requis : Pipeline scikit-learn (M1), évaluation continue (M5-B2)

## Pourquoi cette techno ?

Le cœur de la boucle : produire un **nouveau modèle** à partir des données
récentes + feedbacks, **automatiquement** — mais **jamais à l'aveugle**. Un
réentraînement non contrôlé peut produire un modèle **pire** et le déployer. Les
garde-fous (contract test + évaluation continue **avant** le tag) garantissent
qu'on ne met en prod qu'une version au moins aussi bonne.

## Concepts clés

- **Réutiliser, pas réinventer** : on reprend la **Pipeline M1** (`preprocess.py`
  + mêmes hyperparams). On change la **donnée** (train + feedbacks), pas la recette.
- **Enrichir le train** : joindre les feedbacks (`request_id → true_label`) à
  leurs features (via `prod_scored`) et les ajouter au train initial.
- **Contract test** : le modèle accepte le schéma attendu et sort une proba ∈
  [0,1]. Garde-fou de **non-régression de schéma**.
- **Évaluation continue** : recalcule F1/ROC-AUC/recall sur le `reference_set`
  et compare aux **seuils** (hérités M5-B2). En dessous → **on ne déploie pas**.
- **Code retour** : `retrain.py` sort **0** si OK (modèle v2.1.0 produit), **1**
  si contract test ou éval échoue (la release est bloquée).
- **Redéploiement** : en succès, tag `v2.1.0` → la CI/CD M5 build/push l'image.

## Exemple minimal qui tourne

```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
model = Pipeline([("prep", build_preprocessor()),
                  ("clf", RandomForestClassifier(n_estimators=200, max_depth=10,
                          min_samples_leaf=10, class_weight="balanced", random_state=42))])
model.fit(X_train_plus_feedback, y_train_plus_feedback)
metrics = evaluate(model)                       # F1, ROC-AUC, recall
if any(metrics[k] < THRESHOLDS[k] for k in THRESHOLDS):
    sys.exit(1)                                 # dégradation → bloque
```

## Exercice guidé

1. Complétez `retrain.py` : build training set (train + feedbacks), fit la Pipeline.
2. Ajoutez **contract test** puis **évaluation** ; renvoyez exit 1 si violation.
3. Prouvez le garde-fou : dégradez volontairement (ex. shuffle des labels) →
   le réentraînement doit **bloquer** (exit 1).

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| Déployer sans éval avant le tag | Un modèle pire part en prod |
| Recoder une nouvelle Pipeline | Incohérence avec le modèle servi |
| `print` au lieu de `sys.exit(1)` | La CI ne bloque pas |
| Oublier la jointure feedback↔features | Feedbacks inutilisables pour l'entraînement |
| Non-déterminisme | Résultats non reproductibles (fixer `random_state`) |

| Symptôme | Cause probable |
|---|---|
| v2.1.0 pire que v2 et déployé | éval pas branchée avant le tag |
| `KeyError` features | jointure `request_id` ratée |
| CI verte malgré dégradation | pas de `exit 1` |

## Pour aller plus loin

- scikit-learn Pipeline : https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
- MLOps principles : https://ml-ops.org/content/mlops-principles

## Vérification (checklist apprenant)

- [ ] Je réutilise la Pipeline M1 (pas une nouvelle).
- [ ] J'enrichis le train avec les feedbacks (jointure features).
- [ ] Contract test + éval **avant** le tag v2.1.0.
- [ ] Une dégradation volontaire fait **exit 1** (testé).
- [ ] Résultats reproductibles (`random_state` fixé).

> 💡 **Récap** : on **réutilise** la Pipeline M1 (on change la donnée, pas la recette),
> on **enrichit** le train avec les feedbacks (jointure features), et on **bloque**
> (exit 1) si le contract test ou l'évaluation continue échoue **avant** le tag v2.1.0.
> Jamais de déploiement à l'aveugle.
