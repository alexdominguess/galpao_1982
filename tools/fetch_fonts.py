"""Baixa as fontes (subconjunto latin) do Google Fonts para assets/fonts e gera assets/css/fonts.css."""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
FONTS.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
URL = ("https://fonts.googleapis.com/css2?family=Oswald:wght@400..700"
       "&family=Inter:wght@400..700&family=Parisienne&display=swap")


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read()


css = get(URL).decode()
blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S)
out = []
for subset, block in blocks:
    if subset != "latin":
        continue
    family = re.search(r"font-family: '([^']+)'", block).group(1)
    weight = re.search(r"font-weight: ([^;]+);", block).group(1)
    src = re.search(r"url\((https://[^)]+)\)", block).group(1)
    fname = f"{family.lower()}-latin.woff2"
    (FONTS / fname).write_bytes(get(src))
    block = block.replace(src, f"../fonts/{fname}")
    out.append(block)
    print(family, weight, fname)

(ROOT / "assets" / "css").mkdir(parents=True, exist_ok=True)
(ROOT / "assets" / "css" / "fonts.css").write_text("\n".join(out) + "\n", encoding="utf-8")
