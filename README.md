# M6-B2 — Implémenter la boucle de rétroaction complète (Pyrenex, groupe entier)

> **Repo template.** Premier (et dernier) brief en **groupe entier (8)** sur un
> repo collectif. Le binôme propriétaire (voté mercredi) fait **« Use this
> template »** → `M6-B2-pyrenex-boucle-<promo>` et invite les 7 autres.

## 🚀 Démarrage

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v tests                                   # quand vos tests existent
python scripts/retrain.py --min-feedback 200      # une fois retrain.py complété
```

Données fournies : `data/feedbacks_simules.csv` (200 à injecter), `prod_scored.csv`,
`lending_club_train.csv`, `reference_set.csv`. Modèle de base : `models/pyrenex_risk_v2.joblib`.

## 🧭 Ce que vous construisez (4 sous-équipes de 2)

| Sous-équipe | À faire | Fichier | Mini-cours |
|---|---|---|---|
| A — Endpoint | `POST /feedback` (valide, stocke) | `services/feedback/` | `01` |
| B — Stockage | SQLite/CSV + jointure `request_id` | (idem) | `02` |
| C — Réentraînement | `retrain.py` (train+feedbacks → v2.1.0 + garde-fous) | `scripts/retrain_TEMPLATE.py` | `04` |
| D — Trigger + CI | cron/`workflow_dispatch`, seuil | `crontab_TEMPLATE.txt`, `.github/workflows/ci.yml` | `03` |

> Coordination (lead tournant, branches nominatives, synchros) : mini-cours `05`,
> décisions dans `decisions_TEMPLATE.md`.

## ✅ Réussite

- `/feedback` accepte ≥ 200 annotations, rejette un `request_id` inconnu.
- Réentraînement **sur seuil** (199 → rien, 200 → trigger).
- **Contract test + éval avant le tag** v2.1.0 ; dégradation → exit 1.
- Chaîne CI/CD M5 récupère → Grafana voit v2.1.0.
- **8 contributeurs** visibles, lead tournant, **journal de bord**.

## 📚 Ressources

Voir [`./ressources/`](./ressources/) — 5 mini-cours + `liens_officiels.md`.
