-- ##############################################
-- Validation des données pour l'API Books & Persons
-- ##############################################

-- 1 Personnes et leurs livres (owned_books)
SELECT p.id AS person_id,
       p.first_name,
       p.last_name,
       b.id AS book_id,
       b.title AS book_title
FROM persons p
LEFT JOIN books b ON p.id = b.owner_id
ORDER BY p.id, b.id;


-- 2 Livres et leurs auteurs
SELECT b.id AS book_id,
       b.title AS book_title,
       b.pages,
       a.name AS author_name
FROM books b
JOIN authors a ON b.author_id = a.id
ORDER BY b.id;


-- 3 Livres et leurs propriétaires (owners)
SELECT b.id AS book_id,
       b.title AS book_title,
       p.id AS owner_id,
       p.first_name,
       p.last_name
FROM books b
LEFT JOIN persons p ON b.owner_id = p.id
ORDER BY b.id;


-- 4 Livres et leurs tags (many-to-many)
SELECT b.id AS book_id,
       b.title AS book_title,
       t.name AS tag_name,
       bt.tagged_at
FROM books b
JOIN book_tags bt ON b.id = bt.book_id
JOIN tags t ON t.id = bt.tag_id
ORDER BY b.id, t.name;


-- 5 Statistiques

-- Total livres
SELECT COUNT(*) AS total_books FROM books;

-- Total auteurs
SELECT COUNT(*) AS total_authors FROM authors;

-- Total tags
SELECT COUNT(*) AS total_tags FROM tags;

-- Livre le plus long
SELECT id, title, pages
FROM books
ORDER BY pages DESC
LIMIT 1;

-- Moyenne de pages (arrondie à 1 chiffre après la virgule)
SELECT ROUND(AVG(pages)::numeric, 1) AS average_pages
FROM books;


-- 6 Vérification des jointures manuelles (exemple livre-auteur-propriétaire)
SELECT b.id AS book_id,
       b.title AS book_title,
       a.name AS author_name,
       p.first_name AS owner_first_name,
       p.last_name AS owner_last_name
FROM books b
JOIN authors a ON b.author_id = a.id
LEFT JOIN persons p ON b.owner_id = p.id
ORDER BY b.id;