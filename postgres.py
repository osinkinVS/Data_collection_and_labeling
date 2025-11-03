import psycopg2
import json


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="******",
            host="localhost"
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


def create_table(conn):
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS product_data (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT,
                price DECIMAL(10, 2),
                available TEXT,
                description TEXT
            )
        """)
        conn.commit()
        print("Таблица создана успешно.")
    except Exception as e:
        print(f"Ошибка создания таблицы: {e}")


def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON из файла '{file_path}'.")
        return None


def insert_into_table(conn, data):
    if not data:
        return

    cur = conn.cursor()
    try:
        for product in data:
                if isinstance(product, dict):
                    cur.execute(""" 
                        INSERT INTO product_data (name, url, price, available, description)
                        VALUES (%s, %s, %s::decimal, %s, %s)
                    """, (
                        product.get('name'),
                        product.get('url'),
                        product.get('price'),  # Преобразуем цену в числовой формат
                        product.get('available'),
                        product.get('description')
                    ))
                else:
                    print("Неверный формат данных в JSON-файле!")
        conn.commit()
        print("Данные вставлены успешно.")
    except Exception as e:
        (print(f"Ошибка вставки данных: {e}"))


if __name__ == "__main__":
    conn = connect_to_db()
    if conn is not None:
        create_table(conn)

        # Путь к вашему JSON-файлу
        file_path = 'output.json'
        data = load_json_data(file_path)
        if data:
            insert_into_table(conn, data)

        conn.close()
