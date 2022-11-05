
DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name TEXT,
    overall_budget double precision
);

DROP TABLE IF EXISTS category CASCADE;
CREATE TABLE category(
    name TEXT PRIMARY KEY,
    budget double precision 
);

DROP TABLE IF EXISTS payment CASCADE;
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    user_id SERIAL REFERENCES person(id),
    name TEXT,
    cost double precision,  -- might change to save space 
    category_name TEXT REFERENCES category(name),
    type_of_payment TEXT,
    due_date DATE


);