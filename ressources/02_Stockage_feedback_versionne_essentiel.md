# Stockage des feedbacks — Mini-cours

> Brief associé : M6-B2
> Durée de lecture : ~20 min
> Pré-requis : SQLite (M3), notion de jointure

## Pourquoi cette techno ?

Les feedbacks collectés doivent être **stockés proprement** pour servir au
réentraînement : sans intégrité (doublons, écrasements) ni traçabilité, la
boucle réentraîne sur de la donnée sale. Deux options : **SQLite** (intégrité,
PK, jointures) ou **CSV versionné** (simple, lisible). Le choix se justifie en
groupe — il y a des arbitrages réels.

## Concepts clés

- **SQLite** : base fichier, PK sur `request_id` (anti-doublon), jointures SQL
  vers `prod_scored`. Robuste à la concurrence d'écriture (utile à 8).
- **CSV versionné** : simple, lisible dans Git, mais **pas de garantie
  d'unicité** ni de gestion de la concurrence — risqué à plusieurs.
- **Schéma minimal** : `request_id (PK)`, `true_label`, `comments`, `created_at`.
- **Jointure** : `feedbacks ⋈ prod_scored ON request_id` récupère les
  **features** du dossier → base d'entraînement enrichie.
- **RGPD** : ne stocker que le nécessaire (`request_id` + label). Pas de PII dans
  la table de feedback ; la jointure vers les features reste interne.
- **Rétention** : décider combien de temps on garde les feedbacks (et pourquoi).

## Exemple minimal qui tourne

```python
import sqlite3
con = sqlite3.connect("feedbacks.db")
con.execute("""CREATE TABLE IF NOT EXISTS feedbacks (
    request_id TEXT PRIMARY KEY, true_label INTEGER NOT NULL,
    comments TEXT, created_at TEXT NOT NULL)""")
con.execute("INSERT OR REPLACE INTO feedbacks VALUES (?,?,?,?)",
            ("REQ-00042", 1, "annotation", "2026-06-10T10:00:00Z"))
con.commit()
n = con.execute("SELECT COUNT(*) FROM feedbacks").fetchone()[0]
print("feedbacks:", n)
```

## Exercice guidé

1. En groupe : SQLite **ou** CSV ? Tranchez et écrivez la raison dans `decisions.md`.
2. Implémentez le stockage + un script de **jointure** feedbacks ⋈ prod_scored.
3. Vérifiez : insérer 2× le même `request_id` ne crée pas de doublon.

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| CSV à 8 sans verrou | écritures concurrentes corrompues |
| Pas de PK | doublons → réentraînement biaisé |
| Stocker des PII dans la table feedback | risque RGPD |
| Pas d'horodatage | impossible de gérer la rétention / l'ordre |

| Symptôme | Cause probable |
|---|---|
| Doublons en base | pas de PK / `INSERT OR REPLACE` |
| Jointure vide | `request_id` non aligné entre feedback et prod |
| Conflits Git sur le CSV | choix CSV inadapté au travail à 8 |

## Pour aller plus loin

- Python sqlite3 : https://docs.python.org/3/library/sqlite3.html
- CNIL — durées de conservation : https://www.cnil.fr/fr/la-gestion-des-ressources-humaines

## Vérification (checklist apprenant)

- [ ] Le choix SQLite/CSV est tranché et justifié dans `decisions.md`.
- [ ] Schéma avec PK `request_id` + horodatage.
- [ ] Jointure feedbacks ⋈ prod_scored fonctionnelle.
- [ ] Pas de doublon à la ré-insertion.
- [ ] Pas de PII stockée.
