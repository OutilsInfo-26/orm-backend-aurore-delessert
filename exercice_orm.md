# Exercice : pratiquer ORM + SQL brut (FastAPI)

Objectif : étendre le mini projet ORM pour manipuler des requêtes SQL et ORM, tout en gardant la validation via schemas Pydantic.

---

## Questions de compréhension

Répondez aux questions suivantes avant de commencer l'implémentation.

### Base de données

1. Qu'est-ce qu'une clé primaire et à quoi sert-elle ?
   - Une clé primaire est un champ dans une table de base de données qui identifie de manière unique chaque enregistrement. Elle sert à garantir l'unicité des données et à faciliter les opérations de recherche, de mise à jour et de suppression. Par exemple, dans la table `Author`, le champ `id` est une clé primaire qui identifie chaque auteur de manière unique.
2. Qu'est-ce qu'une clé étrangère ? Donnez un exemple avec les tables du projet.
   - Une clé étrangère est un champ dans une table qui fait référence à la clé primaire d'une autre table. Elle est utilisée pour établir des relations entre les tables. Par exemple, dans la table `Book`, le champ `author_id` est une clé étrangère qui fait référence à l'`id` de la table `Author`, indiquant quel auteur a écrit chaque livre.
3. Quelle est la différence entre un `INNER JOIN` et un `LEFT JOIN` ? Quand utilise-t-on l'un plutôt que l'autre ?
   - Un `INNER JOIN` retourne uniquement les enregistrements qui ont des correspondances dans les deux tables, tandis qu'un `LEFT JOIN` retourne tous les enregistrements de la table de gauche et les correspondances de la table de droite (ou `NULL` si aucune correspondance n'existe). On utilise un `INNER JOIN` lorsque l'on veut uniquement les données qui ont des correspondances, et un `LEFT JOIN` lorsque l'on veut inclure tous les enregistrements de la table de gauche même s'ils n'ont pas de correspondance.
4. Qu'est-ce qu'une table de jointure (association) ? Pourquoi en utilise-t-on une dans ce projet ?
   - Une table de jointure (association) est une table intermédiaire utilisée pour représenter une relation N:M (many-to-many) entre deux tables. Dans ce projet, la table `BookTag` est une table de jointure qui relie les livres (`Book`) et les tags (`Tag`), car un livre peut avoir plusieurs tags et un tag peut être associé à plusieurs livres.
5. Quelle est la différence entre une relation 1:N et une relation N:M ?
   - Une relation 1:N (one-to-many) signifie qu'un enregistrement dans une table peut être associé à plusieurs enregistrements dans une autre table, mais chaque enregistrement de la seconde table ne peut être associé qu'à un seul enregistrement de la première table. Par exemple, un auteur peut écrire plusieurs livres, mais chaque livre n'a qu'un seul auteur. Une relation N:M (many-to-many) signifie que plusieurs enregistrements dans une table peuvent être associés à plusieurs enregistrements dans une autre table. Par exemple, un livre peut avoir plusieurs tags et un tag peut être associé à plusieurs livres.

### Modèles SQLAlchemy (`models.py`)

6. Pourquoi crée-t-on une classe `Base` qui hérite de `DeclarativeBase` au lieu d'hériter directement de `DeclarativeBase` dans chaque modèle ?
   - Créer une classe `Base` qui hérite de `DeclarativeBase` permet de centraliser la configuration et les fonctionnalités communes à tous les modèles. Cela facilite la maintenance et l'extension du code, car toutes les classes de modèles héritent des mêmes propriétés et méthodes définies dans `Base`. De plus, cela permet d'ajouter des fonctionnalités globales (comme des méthodes utilitaires) à tous les modèles en un seul endroit.
7. Comment sont créées les tables en base de données à partir des modèles Python ?
   - Les tables en base de données sont créées à partir des modèles Python en utilisant la méthode `Base.metadata.create_all(bind=engine)`. Cette méthode lit les classes de modèles définies (qui héritent de `Base`) et génère les instructions SQL nécessaires pour créer les tables correspondantes dans la base de données, en fonction des attributs et des types de données spécifiés dans les modèles.
8. Expliquez cette ligne :
   ```python
   id: Mapped[int] = mapped_column(primary_key=True)
   ```
   - Cette ligne définit un champ `id` dans le modèle SQLAlchemy. `Mapped[int]` indique que ce champ est de type entier et est mappé à une colonne de la base de données. `mapped_column(primary_key=True)` spécifie que cette colonne est une clé primaire, ce qui signifie qu'elle identifiera de manière unique chaque enregistrement dans la table correspondante. En résumé, cette ligne crée un champ `id` qui est un entier et sert de clé primaire pour la table.
9.  Comment indique-t-on qu'un champ peut être `NULL` (optionnel) en base de données avec SQLAlchemy 2.0 ?
    - En SQLAlchemy 2.0, on peut indiquer qu'un champ peut être `NULL` (optionnel) en utilisant `mapped_column(nullable=True)`. Par exemple :
    ```python
    description: Mapped[str | None] = mapped_column(nullable=True)
    ```
    Cela signifie que le champ `description` peut être soit une chaîne de caractères, soit `None`, et que la colonne correspondante dans la base de données autorisera les valeurs `NULL`.
10. Expliquez cette ligne :
    ```python
    book_tags: Mapped[list["BookTag"]] = relationship("BookTag", back_populates="book")
    ```
    Que signifie `back_populates` ? Que se passe-t-il si on l'omet ?
    - Cette ligne définit une relation entre le modèle `Book` et le modèle `BookTag`. `Mapped[list["BookTag"]]` indique que ce champ est une liste d'instances de `BookTag`, ce qui signifie qu'un livre peut être associé à plusieurs tags. La fonction `relationship("BookTag", back_populates="book")` établit la relation ORM entre les deux modèles. Le paramètre `back_populates` indique que la relation est bidirectionnelle, c'est-à-dire que dans le modèle `BookTag`, il doit y avoir un champ qui fait référence à `Book` avec `back_populates="book"`. Si on omet `back_populates`, la relation ne sera pas bidirectionnelle, ce qui signifie que l'accès à la relation depuis l'autre modèle (`BookTag`) ne sera pas automatiquement géré par SQLAlchemy, et cela pourrait entraîner des incohérences ou des difficultés lors de la manipulation des données liées.
11. Dans le modèle `Book`, `publisher_id` est défini comme `ForeignKey` mais il n'y a pas de `relationship` vers `Publisher`. Quelle conséquence cela a-t-il sur les requêtes ?
    - Le fait que `publisher_id` soit défini comme `ForeignKey` sans une `relationship` vers `Publisher` signifie que SQLAlchemy ne gérera pas automatiquement les jointures ou les accès aux données de l'éditeur à partir du modèle `Book`. Par conséquent, pour accéder aux informations de l'éditeur d'un livre, il faudra effectuer une jointure manuelle dans les requêtes SQL ou ORM. Cela peut rendre les requêtes plus complexes et moins intuitives, car il n'y aura pas de navigation directe entre les modèles `Book` et `Publisher` via des attributs d'instance.

### Schemas Pydantic (`schemas.py`)

12. À quoi servent les schemas Pydantic dans ce projet ? Pourquoi ne retourne-t-on pas directement les objets SQLAlchemy ?
    - Les schemas Pydantic servent à définir la structure des données qui seront envoyées et reçues par l'API. Ils permettent de valider les données d'entrée, de contrôler les types de données, et de formater les données de sortie. On ne retourne pas directement les objets SQLAlchemy car ils contiennent souvent des informations supplémentaires (comme des méthodes ou des relations) qui ne sont pas nécessaires ou appropriées pour l'API. De plus, retourner des objets SQLAlchemy peut exposer des détails internes de la base de données et rendre l'API moins flexible en cas de changements dans les modèles. Les schemas Pydantic offrent une couche d'abstraction qui permet de séparer la logique métier de la structure des données exposée par l'API.
13. Dans `BookCreate`, expliquez le rôle des `...` dans `Field(...)` et celui de `min_length`, `max_length`.
    - Dans `BookCreate`, les `...` dans `Field(...)` indiquent que ce champ est obligatoire et doit être fourni lors de la création d'un livre. Les paramètres `min_length` et `max_length` sont des contraintes de validation qui spécifient respectivement la longueur minimale et maximale de la chaîne de caractères pour ce champ. Par exemple, si un champ `title` a `min_length=1`, cela signifie que le titre ne peut pas être une chaîne vide, et si `max_length=100`, cela signifie que le titre ne peut pas dépasser 100 caractères. Ces contraintes aident à garantir que les données fournies sont valides et conformes aux attentes de l'application.
14. Qu'est-ce que `model_config = {"from_attributes": True}` et dans quel cas est-ce nécessaire ?
    - `model_config = {"from_attributes": True}` est une configuration de Pydantic qui permet de créer un modèle à partir d'un objet SQLAlchemy en utilisant les attributs de l'objet plutôt que les champs du modèle. Cela est nécessaire lorsque vous souhaitez convertir un objet SQLAlchemy en un modèle Pydantic sans avoir à spécifier manuellement les champs du modèle. Par exemple, si vous avez un objet `Book` et que vous voulez le convertir en `BookOut`, cette configuration permet à Pydantic de lire directement les attributs de l'objet `Book` pour remplir les champs du modèle `BookOut`, ce qui simplifie le processus de conversion et réduit le risque d'erreurs.
15. Quelle est la différence entre `BookCreate` et `BookOut` ? Pourquoi avoir deux schemas séparés ?
    - `BookCreate` est un schema Pydantic utilisé pour valider les données d'entrée lors de la création d'un livre. Il contient les champs nécessaires pour créer un livre, et peut inclure des contraintes de validation spécifiques à la création (comme des champs obligatoires). `BookOut`, en revanche, est un schema utilisé pour formater les données de sortie lorsqu'on retourne un livre dans une réponse API. Il peut inclure des champs supplémentaires qui ne sont pas nécessaires pour la création, comme l'`id` généré par la base de données ou des relations avec d'autres modèles. Avoir deux schemas séparés permet de mieux contrôler les données d'entrée et de sortie, en s'assurant que les clients de l'API reçoivent uniquement les informations pertinentes et que les données d'entrée sont correctement validées.
16. Dans `AuthorUpdate`, tous les champs sont optionnels (`str | None`). Pourquoi ? Quelle est la différence avec `AuthorCreate` ?
    - Dans `AuthorUpdate`, tous les champs sont optionnels (`str | None`) parce que lors de la mise à jour d'un auteur, il n'est pas nécessaire de fournir toutes les informations. Par exemple, si vous souhaitez mettre à jour uniquement le nom d'un auteur, vous ne devriez pas être obligé de fournir son prénom ou d'autres informations. En revanche, dans `AuthorCreate`, les champs sont généralement obligatoires car ils sont nécessaires pour créer un nouvel enregistrement dans la base de données. La différence principale entre les deux schemas est que `AuthorCreate` est conçu pour valider les données nécessaires à la création d'un auteur, tandis que `AuthorUpdate` est conçu pour valider les données qui peuvent être mises à jour, sans exiger que tous les champs soient fournis.

### Routes FastAPI (`orm_simple.py`, `orm_join.py`, etc.)

17. Si le router est défini avec `prefix="/orm"`, pourquoi faut-il appeler `/orm/authors` et non `/authors` ?
    - Le `prefix="/orm"` dans la définition du router signifie que tous les endpoints définis dans ce router seront préfixés par `/orm`. Par conséquent, pour accéder à l'endpoint qui gère les auteurs, il faut inclure le préfixe dans l'URL, ce qui donne `/orm/authors`. Si on essayait d'accéder à `/authors`, cela ne fonctionnerait pas car il n'y a pas de route définie pour cette URL sans le préfixe. Le préfixe permet de regrouper logiquement les endpoints liés à l'ORM sous une même base d'URL, ce qui peut aider à organiser l'API et éviter les conflits avec d'autres routes.
18. Quelle est la différence entre un paramètre de route et un paramètre de requête (query parameter) ? Donnez un exemple de chacun.
    - Un paramètre de route est une partie de l'URL qui est utilisée pour identifier une ressource spécifique. Par exemple, dans l'endpoint `GET /orm/authors/{author_id}`, `author_id` est un paramètre de route qui permet d'identifier quel auteur doit être récupéré. Un paramètre de requête (query parameter) est une partie de l'URL qui suit le symbole `?` et est utilisée pour filtrer ou modifier la réponse. Par exemple, dans l'endpoint `GET /orm/authors?name=John`, `name` est un paramètre de requête qui peut être utilisé pour filtrer les auteurs par leur nom. Les paramètres de route sont généralement utilisés pour identifier des ressources spécifiques, tandis que les paramètres de requête sont utilisés pour affiner les résultats ou fournir des options supplémentaires.
19. Pourquoi utilise-t-on `PATCH` pour la mise à jour d'un auteur plutôt que `PUT` ?
    - On utilise `PATCH` pour la mise à jour d'un auteur plutôt que `PUT` parce que `PATCH` est conçu pour effectuer des mises à jour partielles, tandis que `PUT` est généralement utilisé pour remplacer complètement une ressource. Avec `PATCH`, vous pouvez envoyer uniquement les champs que vous souhaitez mettre à jour, et les autres champs resteront inchangés. En revanche, avec `PUT`, vous devez fournir tous les champs de l'auteur, même ceux qui ne sont pas modifiés, ce qui peut être moins pratique et plus sujet à des erreurs si vous oubliez de fournir un champ ou si vous fournissez des données incorrectes pour un champ non modifié.
20. Que fait `payload.model_dump(exclude_unset=True)` dans la route de mise à jour ? Que se passerait-il sans `exclude_unset=True` ?
    - `payload.model_dump(exclude_unset=True)` est une méthode de Pydantic qui convertit le modèle en un dictionnaire tout en excluant les champs qui n'ont pas été définis (c'est-à-dire les champs qui ont leur valeur par défaut ou qui sont optionnels et n'ont pas été fournis). Cela permet de ne mettre à jour que les champs spécifiés dans la requête. Sans `exclude_unset=True`, tous les champs du modèle seraient inclus dans le dictionnaire, même ceux qui n'ont pas été modifiés, ce qui pourrait entraîner la mise à jour de champs avec des valeurs par défaut ou `None`, ce qui n'est pas souhaitable lors d'une mise à jour partielle.
21. Pourquoi utilise-t-on `session.get(Author, author_id)` plutôt que `session.execute(select(Author).where(Author.id == author_id))` pour chercher un élément par sa clé primaire ?
    - On utilise `session.get(Author, author_id)` plutôt que `session.execute(select(Author).where(Author.id == author_id))` pour chercher un élément par sa clé primaire car `session.get()` est optimisé pour ce cas d'utilisation. Il utilise une requête plus simple et directe pour récupérer l'instance de l'auteur en fonction de sa clé primaire, ce qui est généralement plus rapide et plus efficace que d'exécuter une requête SQL complète avec `select()`. De plus, `session.get()` gère automatiquement la mise en cache des instances, ce qui peut améliorer les performances si le même auteur est demandé plusieurs fois dans la même session. En revanche, `session.execute(select(...))` est plus flexible et peut être utilisé pour des requêtes plus complexes, mais il n'est pas nécessaire pour une simple recherche par clé primaire.

### ORM et requêtes

22. Expliquez la différence entre `session.add()` et `session.commit()`. Que se passe-t-il si on appelle `session.add()` sans `session.commit()` ?
    - `session.add()` est utilisé pour ajouter une instance d'un modèle à la session, ce qui signifie que l'instance est marquée pour être insérée dans la base de données lors du prochain commit. Cependant, les changements ne sont pas encore persistés dans la base de données tant que `session.commit()` n'est pas appelé. `session.commit()` est la méthode qui envoie toutes les modifications en attente (ajouts, mises à jour, suppressions) à la base de données et les rend permanentes. Si on appelle `session.add()` sans `session.commit()`, l'instance sera ajoutée à la session mais ne sera pas enregistrée dans la base de données, ce qui signifie que si la session est fermée ou si une autre opération est effectuée sans commit, les changements seront perdus.
23. À quoi sert `session.flush()` ? Dans quels cas l'utilise-t-on ?
    - `session.flush()` est utilisé pour envoyer les changements en attente à la base de données sans les rendre permanents. Cela permet de synchroniser l'état de la session avec la base de données, ce qui peut être nécessaire pour obtenir des valeurs générées par la base de données (comme les clés primaires auto-incrémentées) avant de faire d'autres opérations qui dépendent de ces valeurs. Par exemple, si vous ajoutez un nouvel auteur et que vous avez besoin de son `id` pour créer un livre associé, vous pouvez appeler `session.flush()` après avoir ajouté l'auteur pour que son `id` soit généré et disponible dans la session avant de créer le livre.
24. Expliquez la différence entre `joinedload` et `selectinload`. Dans quel cas préfère-t-on l'un à l'autre ?
    - `joinedload` et `selectinload` sont deux stratégies de chargement des relations en SQLAlchemy. `joinedload` effectue une jointure SQL pour charger les données liées en une seule requête, ce qui peut être plus efficace lorsque vous avez besoin de charger une relation pour un petit nombre d'instances. En revanche, `selectinload` effectue une requête séparée pour charger les données liées, ce qui peut être plus efficace lorsque vous avez besoin de charger une relation pour un grand nombre d'instances, car cela évite les problèmes de duplication de données qui peuvent survenir avec `joinedload`. En général, on préfère `joinedload` pour les relations 1:N ou N:1 avec peu d'instances, et `selectinload` pour les relations N:M ou lorsque le nombre d'instances est élevé.
25. Pourquoi dans FastAPI est-il quasi-obligatoire d'utiliser `selectinload`/`joinedload` lorsqu'on veut retourner des relations ? Que se passe-t-il si on ne le fait pas ?
    - Dans FastAPI, il est quasi-obligatoire d'utiliser `selectinload` ou `joinedload` lorsqu'on veut retourner des relations pour éviter le problème de N+1. Si on ne le fait pas, SQLAlchemy effectuera une requête séparée pour chaque instance de la relation, ce qui peut entraîner un grand nombre de requêtes SQL (N+1) et ralentir considérablement les performances de l'API. Par exemple, si vous retournez une liste de livres avec leurs auteurs sans utiliser `joinedload`, SQLAlchemy exécutera une requête pour récupérer les livres, puis une requête supplémentaire pour chaque livre afin de récupérer son auteur, ce qui peut rapidement devenir inefficace si vous avez beaucoup de livres.
26. Quelle est la différence entre ces deux approches ?
    ```python
    # Approche A
    select(Book.id, Book.title, Author.name.label("author_name")).join(Author)

    # Approche B
    select(Book).options(joinedload(Book.author))
    ```

---

## Tâches à réaliser

Les tâches suivantes sont à implémenter dans de nouveaux fichiers ou dans les fichiers existants selon la logique du projet.

### Modèle

#### 1. Table `Person` ✔️ 
Créez un modèle `Person` représentant le propriétaire d'un livre.

- Une personne peut posséder plusieurs livres
- Un livre appartient à une seule personne (relation 1:N)
- Attributs minimum : `id`, `first_name`, `last_name`
- Ajoutez le champ `owner_id` dans le modèle `Book` (avec ou sans `relationship`, à vous de choisir et de justifier)
- Ajoutez des données de test dans `init_db()`

### Routes — Persons

#### 2. Créer une personne ✔️ 
`POST /orm/persons`

- Valider les données avec un schema Pydantic
- Retourner la personne créée

#### 3. Lister les personnes ✔️ 
`GET /orm/persons`

- Retourner la liste de toutes les personnes

#### 4. Personnes avec leurs livres (nom seulement) ✔️ 
`GET /orm/persons-with-books`

- Retourner chaque personne avec la liste des titres de ses livres
- Ne pas retourner l'objet `Book` complet — uniquement le titre (string)
- Choisir la bonne stratégie de chargement et justifier votre choix

### Routes — Livres enrichis

#### 5. Livres avec auteur et éditeur
`GET /orm/books-full`

- Retourner chaque livre avec le nom de l'auteur et le nom de l'éditeur
- Rappel : `publisher_id` existe dans `Book` mais il n'y a pas de `relationship` — la jointure doit être faite manuellement

#### 6. Supprimer un livre ✔️ 
`DELETE /orm/books/{book_id}`

- Retourner `204 No Content` si supprimé
- Retourner `404` si le livre n'existe pas

### Routes — Statistiques

#### 7. Statistiques générales
`GET /orm/stats`

Retourner un objet JSON avec :
- Nombre total de livres
- Nombre total d'auteurs
- Nombre total de tags
- Titre et nombre de pages du livre le plus long
- Moyenne du nombre de pages de tous les livres

#### 8. Personnes avec le nombre de livres
`GET /orm/persons-with-book-count`

- Retourner chaque personne avec le nombre de livres qu'elle possède
- Utiliser une aggregation (`COUNT`) — pas de chargement de la liste des livres

---

## Validation avec PgAdmin

- Créez un fichier `validation.sql` avec des requêtes SQL pour vérifier que les données sont correctement insérées, mises à jour et supprimées dans la base de données
- Exécutez ces requêtes dans PgAdmin pour valider les opérations effectuées par votre API
- Contrôler que les jointures fonctionnent correctement en vérifiant les données retournées par les endpoints qui utilisent des jointures
- Contrôler les valeurs des statistiques retournées par les endpoints de statistiques

## Checklist de validation

- Les nouveaux endpoints apparaissent dans Swagger UI (`/docs`)
- Les validations Pydantic renvoient bien `422` si les données sont invalides
- Les routes `404` fonctionnent correctement
- Le `DELETE` retourne bien `204`
- Les statistiques affichent des valeurs correctes
- Les requêtes avec jointure ne font pas de N+1 (vérifier avec les logs SQL si disponible)
