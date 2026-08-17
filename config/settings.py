import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
MAX_INPUT_TOKENS = 5000        
TOKEN_CHUNK_SIZE = 3500         
TOKEN_OVERLAP = 200             
MAX_REDUCE_TOKENS = 4000        
TPM_DELAY_SECONDS = 3.0         
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", BASE_DIR / "temp"))
EXPORTS_DIR = Path(os.getenv("EXPORTS_DIR", BASE_DIR / "exports"))
DB_PATH = Path(os.getenv("DB_PATH", DATA_DIR / "app_data.db"))

for d in [DATA_DIR, TEMP_DIR, EXPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)