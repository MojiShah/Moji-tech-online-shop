from pathlib import Path

from dotenv import load_dotenv


load_dotenv(
    Path(__file__).resolve().parents[2] / ".env"
)


from .base import *


DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

API_DOCS_ENABLED = True