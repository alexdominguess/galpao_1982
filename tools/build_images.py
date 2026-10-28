"""
Gera as imagens otimizadas do site (AVIF + WebP) a partir das fotos originais.

Uso (na raiz do projeto):  python tools/build_images.py

Para trocar uma foto: substitua o arquivo original (ou ajuste SRC/CROPS abaixo)
e rode o script novamente.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

SRC = {
    "espetos": ROOT / "Screenshot 2026-10-28 140350.png",
    "carnes": ROOT / "Screenshot 2026-10-28 140402.png",
    "cortes": ROOT / "Screenshot 2026-10-28 141359.png",
    "burger": ROOT / "Kit hamburguer.png",
    "bar": ROOT / "bar.png",
    "almoco": ROOT / "almoço.png",
    "campari": ROOT / "Bar campari.png",
    "logo": ROOT / "Logo.png",
}

# nome: (fonte, caixa de recorte (x0, y0, x1, y1) ou None, larguras de saída)
CROPS = {
    "hero-cortes-nobres": ("cortes", (0, 345, 837, 780), [800, 1600]),
    "acougue-carnes-nobres": ("carnes", (0, 150, 425, 665), [480, 900]),
    "card-acougue": ("cortes", (420, 350, 837, 780), [420, 800]),
    "card-churrascaria": ("espetos", (285, 225, 690, 700), [420, 800]),
    "card-bar": ("bar", None, [420, 677]),
    "bar-campari": ("campari", None, [400, 679]),
    "restaurante-almoco": ("almoco", (0, 24, 686, 681), [560, 686]),
    "churrasco-brasa": ("burger", (0, 575, 1024, 1260), [800, 1400]),
    # textura de mármore preto retirada das próprias artes da marca
    "textura-marmore": ("carnes", (420, 480, 851, 650), [900]),
}


def load(key):
    return Image.open(SRC[key]).convert("RGB")


def resize(im, width):
    if im.width == width:
        return im
    h = round(im.height * width / im.width)
    out = im.resize((width, h), Image.LANCZOS)
    if width > im.width:  # ampliação: devolve um pouco de nitidez
        out = out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))
    return out


def save(im, name):
    im.save(OUT / f"{name}.avif", quality=58, speed=4)
    im.save(OUT / f"{name}.webp", quality=80, method=6)


def build_photos():
    for name, (src, box, widths) in CROPS.items():
        base = load(src)
        if box:
            base = base.crop(box)
        if name == "textura-marmore":
            arr = np.asarray(base, dtype=np.float32)
            arr = np.clip(arr * 2.6 + 6, 0, 255).astype(np.uint8)
            base = Image.fromarray(arr).filter(ImageFilter.GaussianBlur(0.8))
        for w in widths:
            save(resize(base, w), f"{name}-{w}")
        print(f"{name}: {base.size} -> {widths}")


def build_logo():
    im = Image.open(SRC["logo"]).convert("RGB")
    lum = np.asarray(im.convert("L"), dtype=np.float32)
    alpha = np.clip((lum - 28) / (230 - 28), 0, 1) * 255
    rgba = np.zeros((*lum.shape, 4), dtype=np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = alpha.astype(np.uint8)
    logo = Image.fromarray(rgba, "RGBA")
    logo = logo.crop(logo.getbbox())
    logo.save(OUT / "logo-galpao-1982.png", optimize=True)
    logo.save(OUT / "logo-galpao-1982.webp", quality=90, method=6)
    print("logo:", logo.size)

    # favicons com fundo carvão
    for size, name in [(48, "favicon-48.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
        canvas = Image.new("RGBA", (size, size), (11, 11, 11, 255))
        pad = round(size * 0.12)
        l = logo.copy()
        l.thumbnail((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
        canvas.alpha_composite(l, ((size - l.width) // 2, (size - l.height) // 2))
        canvas.convert("RGB").save(OUT / name, optimize=True)


def build_og():
    im = load("cortes").crop((0, 345, 837, 780))
    im = resize(im, 1212).crop((6, 0, 1206, 630))
    logo = Image.open(OUT / "logo-galpao-1982.png")
    logo.thumbnail((170, 170), Image.LANCZOS)
    grad = np.zeros((630, 1200, 4), dtype=np.uint8)
    grad[..., 3] = (np.linspace(200, 40, 1200)[None, :] * np.ones((630, 1))).astype(np.uint8)
    shade = Image.fromarray(grad, "RGBA")
    out = im.convert("RGBA")
    out.alpha_composite(shade)
    out.alpha_composite(logo, (48, 40))
    out.convert("RGB").save(OUT / "og-galpao-1982.jpg", quality=84, optimize=True)


if __name__ == "__main__":
    build_photos()
    build_logo()
    build_og()
