import os
import psycopg2


conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')


# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS person CASCADE;')
cur.execute('CREATE TABLE person(id SERIAL PRIMARY KEY, name TEXT);')

cur.execute('DROP TABLE IF EXISTS budget CASCADE;')
cur.execute('CREATE TABLE budget(user_id SERIAL,budget_id SERIAL PRIMARY KEY,overall_budget_limit double precision,budget_amount double precision,FOREIGN KEY (user_id) REFERENCES person(id));')
# 
cur.execute('DROP TABLE IF EXISTS category CASCADE;')
cur.execute('CREATE TABLE category(name TEXT PRIMARY KEY,budget_id SERIAL,FOREIGN KEY (budget_id) REFERENCES budget(budget_id));')
# 
cur.execute('DROP TABLE IF EXISTS login CASCADE;')
cur.execute('CREATE TABLE login(user_id SERIAL,password TEXT UNIQUE,user_name TEXT UNIQUE,FOREIGN KEY (user_id) REFERENCES person(id));')

#
cur.execute('DROP TABLE IF EXISTS saving_goals CASCADE;')
cur.execute('CREATE TABLE saving_goals(user_id SERIAL,name TEXT,amount double precision,dead_line date,FOREIGN KEY (user_id) REFERENCES person(id));')

cur.execute('INSERT INTO person(name)'
"VALUES(%s)",["davit phan"])
cur.execute('INSERT INTO saving_goals(name,amount,dead_line)'
'VALUES(%s,%s,%s)',
('davit phan',22.22,'2022-02-22'))
# Execute a command: this creates a new table


# Insert data into the table






conn.commit()

cur.close()
conn.close()

