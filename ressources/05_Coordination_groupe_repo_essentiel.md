# Coordination à l'échelle d'un groupe — Mini-cours

> Brief associé : M6-B2
> Durée de lecture : ~20 min
> Pré-requis : Git (branches, PR), pair-coding (M5 `06`)

## Pourquoi cette techno ?

M6-B2 est le **seul brief à 8 sur un même repo**. À cette échelle, l'absence de
convention = chaos (conflits permanents, code écrasé, personne ne sait qui fait
quoi). La coordination devient une **compétence à part entière** (CT2 pilotage,
CT9 collectif), observée par le jury. Le **lead tournant** + les **branches
nominatives** + les **synchros** structurent le travail collectif.

## Concepts clés

- **Branches nominatives** : `<prenom>/<feature>`. Personne ne pousse sur `main`
  directement ; tout passe par des PR. Limite les conflits.
- **Lead tournant** : 1 lead par demi-journée (8 créneaux = chacun lead une
  fois). Le lead valide les PR, tranche les arbitrages, anime la coord. C'est
  l'exercice **CT2** — chacun pilote à son tour.
- **Sous-équipes** : 4 paires sur 4 briques (endpoint / stockage / retrain /
  trigger). Découpage par **interface claire** (qui appelle quoi, quel format).
- **Synchros aux jalons** : 15 min à heures fixes (jeudi 17h, vendredi 9h) pour
  aligner les interfaces et débloquer — pas une réunion permanente.
- **`Co-authored-by:`** : quand deux codent en pair, les 2 sont crédités.
- **Contrat d'interface** : se mettre d'accord **tôt** sur les formats d'échange
  (schéma feedback, nom du modèle v2.1.0) pour bosser en parallèle.

## Exemple minimal qui tourne

```bash
git switch -c lea/feedback-endpoint     # branche nominative
# ... travail ...
git commit -m "feat(feedback): POST /feedback + validation

Co-authored-by: Tom Martin <tom@example.com>"
git push -u origin lea/feedback-endpoint   # puis Pull Request, validée par le lead
```

## Exercice guidé

Avant de coder (en groupe, 30 min) :
1. Répartissez les 4 briques entre les 4 paires.
2. Fixez les **interfaces** : schéma `/feedback`, format de stockage, nom du
   modèle réentraîné.
3. Désignez le **lead** du créneau et planifiez les 2 synchros.
Tracez tout dans `decisions.md`.

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| Tout le monde sur `main` | Conflits permanents, code écrasé |
| Pas d'interfaces fixées | Les briques ne s'emboîtent pas à l'intégration |
| Pas de lead | Personne ne tranche, blocages |
| Synchros permanentes | Personne n'avance |
| 2-3 personnes portent tout | CT9 non validée pour les autres |

| Symptôme | Cause probable |
|---|---|
| Merge hell vendredi matin | pas de PR au fil de l'eau / pull tardif |
| Briques incompatibles | contrat d'interface absent |
| Historique avec 2 contributeurs | coordination en échec |

## Pour aller plus loin

- Co-authored commits : https://docs.github.com/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors
- Async communication (Atlassian) : https://www.atlassian.com/agile/distributed-teams/asynchronous-communication

## Vérification (checklist apprenant)

- [ ] Je travaille sur une **branche nominative** (pas `main`).
- [ ] Les interfaces entre briques sont fixées et tracées.
- [ ] J'ai assuré **mon créneau de lead**.
- [ ] Les synchros jeudi 17h / vendredi 9h ont eu lieu (documentées).
- [ ] **8 contributeurs** visibles dans l'historique.
