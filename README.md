# Projet Flask - Allocation de commandes - Studi live Développement web avec Python

## Comment travailler avec le projet

1. Installer `pyenv` (documentation)[https://github.com/pyenv/pyenv#installation]
2. Installer Python `3.10`avec pyenv: `pyenv install 3.10.x` (choisissez la version la plus récente, `3.10.3`au moins)
3. Utiliser cette version dans le répertoire du projet `pyenv local 3.10.x`
4. Créer un environnement virtuel `python -m venv .venv`et l'activer avec `source .venv/bin/activate`(sur Linux / MacOS, dépend de votre système)
5. Mettre à jour pip `pip install -U pip setuptools`
6.  Installer les dépendances du projet: `pip install -r requirements.txt`
7.  Pour faire tourner l'application en local avec le serveur de dev Flask: `FLASK_ENV=development FLASK_APP=allocation:app flask run --reload`


## L'application

### Règles métier

Un produit est identifié par un SKU, prononcé "skew", qui est l'abréviation d'unité de stockage. Les clients passent des commandes. Une commande est identifiée par une référence de commande et comprend plusieurs lignes de commande, où chaque ligne a un SKU et une quantité. Par exemple : 10 unités de RED-CHAIR, 1 unité de TASTELESS-LAMP

Le service des achats commande de petits lots de stock. Un lot de stock a un identifiant unique appelé référence, un SKU et une quantité.

Nous devons allouer des lignes de commande à des lots. Lorsque nous avons attribué une ligne de commande à un lot, nous envoyons le stock de ce lot spécifique à l'adresse de livraison du client. Lorsque nous affectons x unités de stock à un lot, la quantité disponible est réduite de x. Par exemple:
    Nous avons un lot de 20 SMALL-TABLE, et nous allouons une ligne de commande pour 2 SMALL-TABLE.
    Le lot doit avoir 18 SMALL-TABLE restants.

Nous ne pouvons pas allouer à un lot si la quantité disponible est inférieure à la quantité de la ligne de commande. Par exemple:
    Nous avons un lot de 1 BLUE-CUSHION, et une ligne de commande pour 2 BLUE-CUSHION.
    Nous ne devrions pas être en mesure d'allouer la ligne au lot.

Nous ne pouvons pas allouer deux fois la même ligne. Par exemple:
    Nous avons un lot de 10 BLUE-VASE, et nous allouons une ligne de commande pour 2 BLUE-VASE.
    Si nous attribuons à nouveau la ligne de commande au même lot, le lot devrait toujours avoir une quantité disponible de 8.

Les lots ont un ETA (Estimated Time Arrival) s'ils sont actuellement expédiés, ou ils peuvent être en stock d'entrepôt. Nous attribuons au stock d'entrepôt de préférence aux lots d'expédition. Nous attribuons aux lots d'expédition dans l'ordre de ceux qui ont le premier ETA.

### Fonctionnalités

- Webservices, réponses en JSON:
    - lister les produits
    - ajouter des lots
    - allouer une commande (à un lot)

- Une interface HTML:
    - visualiser les produits, lots et allocations
    - visualiser les commandes
    - allouer une commande



