from faker import Faker
import psycopg2

def seed_data():
    fake = Faker()
    conn = psycopg2.connect(
        dbname="task_management",
        user="postgres",
        password="postgres_pass",
        host="localhost"
    )
    cursor = conn.cursor()

    # Додавання користувачів
    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

    # Додавання статусів
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING", statuses)

    # Додавання завдань
    cursor.execute("SELECT id FROM users")
    user_ids = cursor.fetchall()

    cursor.execute("SELECT id FROM status")
    status_ids = cursor.fetchall()

    for _ in range(30):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        user_id = fake.random_element(user_ids)[0]
        status_id = fake.random_element(status_ids)[0]
        cursor.execute(
            "INSERT INTO tasks (title, description, user_id, status_id) VALUES (%s, %s, %s, %s)",
            (title, description, user_id, status_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_data()