import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/'.env')

DEBUG = os.environ.get("DEBUG")

SECRET_KEY = os.environ.get("SECRET_KEY")