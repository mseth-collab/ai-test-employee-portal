# config.py
import os
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.1")  # default if not set

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please set it in your .env file.")
