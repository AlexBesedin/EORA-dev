import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import pymorphy3
from openai import OpenAI

BASE_DIR = Path(__file__).parent.parent

load_dotenv()


@dataclass
class Config:
    DB_URL = os.getenv("DB_URL", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN", "")
    PROXYAPI_URL = os.getenv("PROXYAPI_URL", "")


class Resources:
    morph = pymorphy3.MorphAnalyzer()
