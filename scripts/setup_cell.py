"""Her notebook'un ilk kod hücresi. Notebook'lara birebir bu metin konur."""

SETUP_CELL = """\
# Kurulum: Colab'da repoyu indirir, yerelde repo klasörünü bulur.
import os, sys
REPO = "https://github.com/MehmetaliBeylikci/python-cevresel-modelleme"
TARGET = "/content/python-cevresel-modelleme"
if "google.colab" in sys.modules:
    if not os.path.exists(TARGET + "/src/model.py"):  # hiç indirilmemiş ya da yarıda kalmış
        !rm -rf {TARGET}
        !git clone -q {REPO} {TARGET}
    %cd {TARGET}
    %pip install -q sweetviz
else:
    while not os.path.exists("src/model.py") and os.getcwd() != "/":
        os.chdir("..")
    if not os.path.exists("src/model.py"):
        raise RuntimeError("Eğitim repo klasörü bulunamadı. Notebook'u repo içinden açın ya da Colab'da çalıştırın.")
sys.path.insert(0, os.getcwd())"""
