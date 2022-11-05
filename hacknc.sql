DROP TABLE IF EXISTS person CASCADE; -- Why do we need this to be a cascade? I deleted the if exists because it gave me an error at the end.
CREATE TABLE person(
    id SERIAL PRIMARY KEY,
    name TEXT
);

DROP TABLE IF EXISTS budget CASCADE;
CREATE TABLE budget(
    user_id SERIAL,
    budget_id SERIAL PRIMARY KEY,
    overall_budget_limit double precision,
    budget_amount double precision,
    FOREIGN KEY (user_id) REFERENCES person(id)
);



DROP TABLE IF EXISTS category CASCADE;
CREATE TABLE category(
    name TEXT PRIMARY KEY,
    budget_id SERIAL,
    FOREIGN KEY (budget_id) REFERENCES budget(budget_id)
);

DROP TABLE IF EXISTS login CASCADE;
CREATE TABLE login(
    user_id SERIAL,
    password TEXT UNIQUE,
    user_name TEXT UNIQUE,
    FOREIGN KEY (user_id) REFERENCES person(id)
);

DROP TABLE IF EXISTS payment CASCADE;
CREATE TABLE payment(
    payment_id SERIAL PRIMARY KEY,
    user_id SERIAL,
    name TEXT,
    cost double precision,  -- might change to save space 
    category_name TEXT,
    type_of_payment TEXT,
    due_date DATE,
    FOREIGN KEY (user_id) REFERENCES person(id),
    FOREIGN KEY (category_name) REFERENCES category(name)

);

DROP TABLE IF EXISTS saving_goals CASCADE;
CREATE TABLE saving_goals(
    user_id SERIAL DEFAULT NULL,
    name TEXT,
    amount double precision,
    dead_line date,
    FOREIGN KEY (user_id) REFERENCES person(id)
);

INSERT INTO saving_goals(name,amount,dead_line)
    VALUES('bob','22.22','2022-02-22');