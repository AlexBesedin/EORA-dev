import os
from pathlib import Path
from dotenv import load_dotenv
import pymorphy3
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).parent.parent

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN", "")
    PROXYAPI_URL = os.getenv("PROXYAPI_URL", "")


class Resources:
    morph = pymorphy3.MorphAnalyzer()
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    # model = SentenceTransformer('distiluse-base-multilingual-cased-v2') #bad
    # model = SentenceTransformer('bert-base-nli-mean-tokens')
