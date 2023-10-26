-- Create the styles table
CREATE TABLE styles (
  id INTEGER PRIMARY KEY,
  style TEXT NOT NULL,
  price REAL NOT NULL
);

-- Insert data into the styles table
INSERT INTO styles (id, style, price) VALUES (1, 'Classic', 500);
INSERT INTO styles (id, style, price) VALUES (2, 'Modern', 710);
INSERT INTO styles (id, style, price) VALUES (3, 'Vintage', 965);

-- Create the sizes table
CREATE TABLE sizes (
  id INTEGER PRIMARY KEY,
  carets REAL NOT NULL,
  price REAL NOT NULL
);

-- Insert data into the sizes table
INSERT INTO sizes (id, carets, price) VALUES (1, 0.5, 405);
INSERT INTO sizes (id, carets, price) VALUES (2, 0.75, 782);
INSERT INTO sizes (id, carets, price) VALUES (3, 1, 1470);
INSERT INTO sizes (id, carets, price) VALUES (4, 1.5, 1997);
INSERT INTO sizes (id, carets, price) VALUES (5, 2, 3638);

-- Create the metals table
CREATE TABLE metals (
  id INTEGER PRIMARY KEY,
  metal TEXT NOT NULL,
  price REAL NOT NULL
);

-- Insert data into the metals table
INSERT INTO metals (id, metal, price) VALUES (1, 'Sterling Silver', 12.42);
INSERT INTO metals (id, metal, price) VALUES (2, '14K Gold', 736.4);
INSERT INTO metals (id, metal, price) VALUES (3, '24K Gold', 1258.9);
INSERT INTO metals (id, metal, price) VALUES (4, 'Platinum', 795.45);
INSERT INTO metals (id, metal, price) VALUES (5, 'Palladium', 1241);

-- Create the orders table
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  metalId INTEGER NOT NULL,
  sizeId INTEGER NOT NULL,
  styleId INTEGER NOT NULL,
  FOREIGN KEY (metalId) REFERENCES metals(id),
  FOREIGN KEY (sizeId) REFERENCES sizes(id),
  FOREIGN KEY (styleId) REFERENCES styles(id)
);

-- Insert data into the orders table
INSERT INTO orders (id, metalId, sizeId, styleId) VALUES (1, 2, 3, 2);
INSERT INTO orders (id, metalId, sizeId, styleId) VALUES (2, 3, 2, 1);
