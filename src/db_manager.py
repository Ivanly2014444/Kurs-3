import psycopg2


class DBManager:
    def __init__(self, params: dict):
        self.params = params

    def get_countries_and_aeroplanes_count(self):
        """ Получает список всех стран и количество самолетов в их воздушных пространствах """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT c.country, COUNT(a.icao24) "
                            "FROM countries c "
                            "LEFT JOIN airplanes a ON c.country = a.country_name "
                            "GROUP BY c.country;")

                result = cur.fetchall()

                return result

    def get_all_aeroplanes(self):
        """ Получает список всех воздушных судов """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT icao24, callsign, latitude,longitude "
                            "FROM airplanes")

                result = cur.fetchall()
                return result

    def get_avg_speed(self):
        """ Получает среднюю скорость по самолетам """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(speed) FROM airplanes")
                result = cur.fetchone()
                return result[0] if result and result[0] else 0

    def get_aeroplanes_with_higher_speed(self):
        """ Получает список всех самолетов, у которых скорость выше средней """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT icao24, callsign, speed, latitude, longitude, country_name 
                FROM airplanes 
                WHERE speed > (SELECT AVG(speed) FROM airplanes);
                """)
                result = cur.fetchall()
                return result

    def get_aeroplanes_with_keyword(self, keyword: str):
        """ Получает список всех самолетов, в позывном которых содержатся переданные символы """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT icao24, callsign, speed, latitude, longitude, country_name 
                FROM airplanes 
                WHERE callsign ILIKE %s;
                """, (f"%{keyword}%",))
                return cur.fetchall()



