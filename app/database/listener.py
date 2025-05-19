import asyncio
import psycopg2
import os

HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")

CHANNEL = 'todo'


class Listener:
    def init(self):
        loop = asyncio.get_event_loop()

        conn = psycopg2.connect(host=HOST, dbname=DB_NAME,
                                user=USER, password=PASSWORD)
        conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        cursor.execute(f"LISTEN {CHANNEL};")
        print(f"🔔 Listening on channel: {CHANNEL}")

        def handle_notify():
            conn.poll()
            for notify in conn.notifies:
                print(notify.payload, flush=True)
            conn.notifies.clear()

        loop.add_reader(conn, handle_notify)
