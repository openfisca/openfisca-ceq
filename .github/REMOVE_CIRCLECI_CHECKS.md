# Supprimer CircleCI des checks GitHub requis

## Problème
CircleCI apparaît encore dans les checks requis pour les Pull Requests, même si le code CircleCI a été supprimé du dépôt.

## Solution : Supprimer CircleCI des Branch Protection Rules

### Étape 1 : Accéder aux paramètres de protection de branche

1. Aller sur : https://github.com/openfisca/openfisca-ceq/settings/branches
2. Chercher la règle de protection pour la branche `master`
3. Cliquer sur **Edit** ou **Add rule** si aucune règle n'existe

### Étape 2 : Supprimer CircleCI des checks requis

1. Dans la section **"Require status checks to pass before merging"**
2. Chercher dans la liste des checks :
   - `ci/circleci` ou similaire
   - Tout check contenant "circle" ou "CircleCI"
3. **Décocher** ces checks CircleCI
4. **Cocher uniquement** les checks GitHub Actions :
   - `test (Python 3.11)`
   - `lint`
   - Optionnellement : `test (Python 3.12)` et `build`
5. Cliquer sur **Save changes**

### Étape 3 : Vérifier

1. Créer ou modifier une PR
2. Vérifier que seuls les checks GitHub Actions apparaissent
3. CircleCI ne devrait plus apparaître

## Alternative : Via l'API GitHub

Si vous préférez utiliser la ligne de commande :

```bash
# Voir la configuration actuelle
gh api repos/openfisca/openfisca-ceq/branches/master/protection

# Note: La modification via API nécessite des permissions admin
# Il est plus simple de le faire via l'interface web
```

## Checks GitHub Actions à configurer

Selon `.github/REQUIRED_CHECKS.md`, les checks suivants devraient être requis :

### Minimum requis :
- `test (Python 3.11)`
- `lint`

### Optionnels :
- `test (Python 3.12)`
- `build`

## Note importante

Le check `deploy` ne doit **PAS** être requis car il ne s'exécute que sur `master` après merge, pas sur les PRs.
