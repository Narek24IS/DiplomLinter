import psycopg2
from psycopg2.extras import DictCursor

# Подключение к БД
# connection = psycopg2.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     dbname="linter",
#     port=5432
# )
print("Подключение к PostgreSQL успешно")

def select(query, args=None):
    connection = psycopg2.connect(
        host="localhost",
        user="root",
        password="root",
        dbname="linter",
        port=5432
    )
    cursor = connection.cursor(cursor_factory=DictCursor)
    try:
        print(query, args if args else "")
        print("*"*40)
        cursor.execute(query, args)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка запроса: {type(e).__name__} {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def update(query, args=None):
    connection = psycopg2.connect(
        host="localhost",
        user="root",
        password="root",
        dbname="linter",
        port=5432
    )
    cursor = connection.cursor(cursor_factory=DictCursor)
    try:
        print(query, args if args else "")
        print("*"*40)
        cursor.execute(query, args)
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Ошибка запроса: {type(e).__name__} {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def insert(query, args=None):
    connection = psycopg2.connect(
        host="localhost",
        user="root",
        password="root",
        dbname="linter",
        port=5432
    )
    cursor = connection.cursor()
    try:
        print(query, args if args else "")
        print("*" * 40)
        cursor.execute(query, args)
        cursor.execute("SELECT lastval()")  # Получаем последний ID
        new_id = cursor.fetchone()[0]
        connection.commit()
        return new_id
    except Exception as e:
        print(f"Ошибка запроса: {type(e).__name__} {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
