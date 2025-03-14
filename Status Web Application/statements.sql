CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL
    description TEXT NOT NULL,
    date INT,
    time INT)
    CHECK ((username IS NOT NULL AND description IS NOT NULL) OR (username IS NULL AND description IS NULL));