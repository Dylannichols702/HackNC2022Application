
DROP TABLE IF EXISTS user CASCADE; -- Why do we need this to be a cascade?
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name TEXT,
    overall_budget double precision
);

DROP TABLE IF EXISTS category CASCADE;
CREATE TABLE category(
    name TEXT PRIMARY KEY,
    budget double precision 
);

DROP TABLE IF EXISTS login CASCADE;
CREATE TABLE login(
    user_id TEXT PRIMARY KEY,
    password UNIQUE TEXT
    username UNIQUE TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS payment CASCADE;
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    user_id SERIAL,
    name TEXT,
    cost double precision,  -- might change to save space 
    category_name TEXT REFERENCES category(name),
    type_of_payment TEXT,
    due_date DATE
    FOREIGN KEY (user_id) REFERENCES user(id)

);