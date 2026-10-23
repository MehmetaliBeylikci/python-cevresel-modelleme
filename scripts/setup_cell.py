"""Her notebook'un ilk kod hücresi. Notebook'lara birebir bu metin konur."""

SETUP_CELL = """\
# Kurulum: Colab'da repoyu indirir, yerelde hiçbir şey yapmaz.
import os, sys
REPO = "https://github.com/mehmetalibeylikci/python-cevresel-modelleme"
if "google.colab" in sys.modules:
    if not os.path.exists("/content/python-cevresel-modelleme"):
        !git clone -q {REPO} /content/python-cevresel-modelleme
    %cd /content/python-cevresel-modelleme
    %pip install -q sweetviz
else:
    while not os.path.exists("src/model.py") and os.getcwd() != "/":
        os.chdir("..")
sys.path.insert(0, os.getcwd())"""
