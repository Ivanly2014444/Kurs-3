import psycopg2
from config import params
from src.api_client import get_airplanes_in_country, get_country_coordinates
from src.db_loader import create_tables
from src.db_manager import DBManager


def main():
    db_name = 'sky_is_over'
    create_tables(db_name, params)

    db_params = params.copy()
    db_params['dbname'] = db_name

    countries = ["Germany", "France", "Poland", "Turkey", "India", "Canada", "Australia", "Japan", "Estonia",
                 "Bulgaria"]

    conn = psycopg2.connect(**db_params)
    try:
        with conn.cursor() as cur:
            for country in countries:
                bbox = get_country_coordinates(country)
                if not bbox:
                    continue

                lat_center = (float(bbox[0]) + float(bbox[1])) / 2
                lon_center = (float(bbox[2]) + float(bbox[3])) / 2

                cur.execute(
                    """
                    INSERT INTO countries (country, latitude, longitude)
                    VALUES (%s, %s, %s) ON CONFLICT (country) DO NOTHING;
                    """,
                    (country, lat_center, lon_center)
                )

                airplanes = get_airplanes_in_country(bbox)

                for plane in airplanes:
                    cur.execute(
                        """
                        INSERT INTO airplanes (icao24, callsign, speed, latitude, longitude, country_name)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (icao24) DO UPDATE SET
                            callsign = EXCLUDED.callsign,
                            speed = EXCLUDED.speed,
                            latitude = EXCLUDED.latitude,
                            longitude = EXCLUDED.longitude,
                            country_name = EXCLUDED.country_name;
                        """,
                        (
                            plane[0],
                            plane[1].strip() if plane[1] else None,
                            plane[9],
                            plane[6],
                            plane[5],
                            country
                        )
                    )
                conn.commit()  # Сохраняем прогресс по каждой стране отдельно
    finally:
        conn.close()


    manager = DBManager(db_params)

    print("1. Количество самолетов по странам:")
    for row in manager.get_countries_and_aeroplanes_count():
        print(f" • {row[0]}: {row[1]} шт.")

    avg_speed = manager.get_avg_speed() or 0
    print(f"\n2. Средняя скорость: {avg_speed:.2f} м/с")

    print("\n3. Быстрее средней скорости (топ-5):")
    for row in manager.get_aeroplanes_with_higher_speed()[:5]:
        print(f" • {row[1]} | {row[2]} м/с ({row[5]})")

    keyword = "TVF"
    print(f"\n4. Поиск по '{keyword}':")
    for row in manager.get_aeroplanes_with_keyword(keyword)[:5]:
        print(f" • {row[0]} ({row[1]}) -> {row[5]}")


if __name__ == "__main__":
    main()
