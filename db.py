from dotenv import load_dotenv
import os

load_dotenv()


def get_database_url() -> str:
    """Return a Postgres connection URL from `DATABASE_URL` or assembled env vars.

    Looks for `DATABASE_URL` first. If not present, tries to assemble from
    `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.
    Raises RuntimeError with actionable message when insufficient info.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME")

    if not (user and password and name):
        raise RuntimeError(
            "DATABASE_URL not set and DB_USER/DB_PASSWORD/DB_NAME not fully provided in environment."
            " Set `DATABASE_URL` or provide DB_USER, DB_PASSWORD, DB_NAME."
        )

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


def create_pool(min_size: int = 1, max_size: int = 10):
    """Create and return a psycopg connection pool using the configured DB URL.

    This function requires `psycopg[binary,pool]` to be installed (your requirements
    already include it). It returns a `psycopg_pool.ConnectionPool` instance.
    """
    try:
        from psycopg_pool import ConnectionPool
    except Exception as exc:
        raise RuntimeError(
            "psycopg pool is required but not available. Install with: pip install psycopg[binary,pool]"
        ) from exc

    dsn = get_database_url()
    return ConnectionPool(conninfo=dsn, min_size=min_size, max_size=max_size)
