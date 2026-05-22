from app.harness.ollama import OllamaBackend
from app.harness.anthropic import AnthropicBackend
import app.ingestion.pg_connection as pg_connection

if __name__ == "__main__":
    conn = pg_connection.connect_to_pgdb()

    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT 1")

            print(curs.fetchone())

    conn.close()
