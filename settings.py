"""File with settings and configs for the project"""

from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:kamil4015@127.0.0.1:5432/postgres"
)  # connect string for the database
