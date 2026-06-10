# Trigger de réentraînement (cron) — Mini-cours

> Brief associé : M6-B2
> Durée de lecture : ~20 min
> Pré-requis : ligne de commande, notion de job planifié

## Pourquoi cette techno ?

Réentraîner **à chaque feedback** serait absurde (coûteux, instable). On déclenche
**périodiquement et sous condition** : « toutes les 6 h, **si** au moins 200
nouveaux feedbacks, réentraîne ». Le **cron** (planificateur OS) suffit pour ça —
pas besoin d'un orchestrateur lourd (Prefect/Airflow) pour M6.

## Concepts clés

- **cron** : une ligne `* * * * * commande` planifie une exécution. `0 */6 * * *`
  = toutes les 6 h. (Testez votre expression sur crontab.guru.)
- **Garde-seuil** : le script vérifie `len(feedbacks) >= seuil` **avant** d'agir ;
  sinon il **ne fait rien** et sort en succès (exit 0). Ce n'est pas une erreur.
- **Idempotence** : relancer le job ne doit pas casser l'état (pas de double
  réentraînement concurrent ; lock simple si besoin).
- **Déclenchement manuel** : en CI, `workflow_dispatch` permet de lancer le
  réentraînement à la demande (utile pour la démo).
- **Anti-spam** : après un réentraînement, on « consomme » ou marque les
  feedbacks pour ne pas re-déclencher immédiatement.

## Exemple minimal qui tourne

```bash
# crontab.txt — toutes les 6h
0 */6 * * * cd /opt/pyrenex && .venv/bin/python scripts/retrain.py --min-feedback 200 >> logs/retrain.log 2>&1
```

```python
# garde-seuil dans retrain.py
if len(feedbacks) < args.min_feedback:
    print({"action": "skip"}); return 0   # rien à faire, pas une erreur
```

## Exercice guidé

1. Écrivez l'expression cron pour « toutes les 6 h » et vérifiez-la sur
   crontab.guru.
2. Implémentez le garde-seuil dans `retrain.py` : 199 feedbacks → skip (exit 0),
   200 → exécute.
3. Ajoutez `workflow_dispatch` au workflow CI pour le déclenchement manuel.

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| Réentraîner à chaque feedback | Coût + instabilité |
| Garde-seuil qui renvoie une erreur quand < seuil | Le cron « échoue » à tort |
| Chemins relatifs dans le cron | Job qui ne trouve pas les fichiers (cron part de `$HOME`) |
| Pas de log redirigé | Échec silencieux, indébogable |

| Symptôme | Cause probable |
|---|---|
| Le cron « échoue » tout le temps | chemins relatifs / venv non activé |
| Réentraînements en boucle | feedbacks non consommés/marqués |
| Rien ne se passe | expression cron fausse (tester sur crontab.guru) |

## Pour aller plus loin

- crontab.guru : https://crontab.guru/
- GitHub Actions — workflow_dispatch : https://docs.github.com/actions/using-workflows/manually-running-a-workflow

## Vérification (checklist apprenant)

- [ ] Mon expression cron est validée (crontab.guru).
- [ ] Le garde-seuil sort en **succès** (exit 0) sous le seuil.
- [ ] Le job utilise des chemins absolus + venv.
- [ ] `workflow_dispatch` permet le déclenchement manuel.
- [ ] Les logs sont redirigés (pas d'échec silencieux).
