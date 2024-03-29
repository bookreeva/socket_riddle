import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
QUESTIONS = os.path.join(BASE_DIR, 'src', 'questions.json')
INDEX = os.path.join(BASE_DIR, 'frontend', 'index.html')
ASSETS = os.path.join(BASE_DIR, 'frontend', 'assets')
