import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password=os.getenv("DB_PASS"),
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS person(
            id INT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            gender CHAR
);
""")

cur.execute("""
INSERT INTO person (id, name, age, gender) VALUES
            (1, 'Mike', 30, 'm'),
            (2, 'Lisa', 4, 'f'),
            (3, 'John', 80, 'm'),
            (4, 'Julie', 41, 'f');
""")

cur.execute("""
            SELECT * FROM person
            WHERE name = 'Mike';
""")

print(cur.fetchone())

cur.execute("""
            SELECT * FROM person
            WHERE age < 42;
""")

# print(cur.fetchall())
for row in cur.fetchall():
    print(row)

sql = cur.mogrify("""SELECT * FROM person WHERE starts_with(name, %s) AND age < %s""", ("J", 50))
print(sql)
cur.execute(sql)
print(cur.fetchall())

conn.commit()

cur.close()
conn.close()