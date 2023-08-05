import os
import dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# add .env variables before the secret key
DOTENV_FILE = os.path.join(BASE_DIR, ".env")


if os.path.isfile(DOTENV_FILE):
    dotenv.load_dotenv(DOTENV_FILE)