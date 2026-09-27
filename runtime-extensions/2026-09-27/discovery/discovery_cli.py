from pathlib import Path
import os
import sys

from dotenv import load_dotenv

runtime = Path(__file__).resolve().parent
load_dotenv(runtime / 'argos.env', override=False)
os.environ.setdefault('ARGOS_RUNTIME_ROOT', str(runtime))
sys.path.insert(0, str(runtime / 'app'))
from src.runtime_discovery import main

main()
