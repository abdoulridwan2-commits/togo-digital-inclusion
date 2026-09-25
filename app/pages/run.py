"""
Lanceur du dashboard
"""

import sys
from pathlib import Path

# Ajoute la racine du projet au chemin Python
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.main import main

if __name__ == "__main__":
    main()