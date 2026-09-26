import subprocess
import sys

print("Tentative installation python-pptx...")
try:
    res = subprocess.run([sys.executable, "-m", "pip", "install", "python-pptx"], capture_output=True, text=True, timeout=60)
    print("STDOUT:", res.stdout[:200])
    print("STDERR:", res.stderr[:200])
    print("Return code:", res.returncode)
except Exception as e:
    print("Erreur subprocess:", e)
