import psycopg2


def create_tables(database_name, params: dict):
    """ Создает таблицы countries и airplanes в базе данных PostgreSQL """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True

    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE countries (
    latitude float,
	country varchar(50) PRIMARY KEY,
	longitude float
);
        """)

        cur.execute("""
            CREATE TABLE airplanes (
    icao24 varchar(50) PRIMARY KEY,
    callsign varchar(20),
    speed float,
    latitude float,  
    longitude float,  
    country_name varchar(50) REFERENCES countries(country) 
);
        """)

    conn.close()
