"""Metni SVG yoluna çevirir.

GitHub, depodaki SVG'leri web fontu yükletmeyen bir CSP ile sunar. Yazılar bu yüzden
<text> yerine <path> olarak gömülür; görsel her cihazda aynı görünür.
"""
from functools import lru_cache
from io import BytesIO
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIZINI = Path(__file__).resolve().parent.parent / "assets" / "fonts"
AILELER = {
    "sans": ("inter-400-latin", "inter-400-ext"),
    "sans-kalin": ("inter-600-latin", "inter-600-ext"),
    "mono": ("mono-400-latin", "mono-400-ext"),
}


class Yazi:
    def __init__(self, ad: str):
        self.tt = TTFont(FONT_DIZINI / f"{ad}.woff2")
        self.tt.flavor = None
        tampon = BytesIO()
        self.tt.save(tampon)
        self.hb_font = hb.Font(hb.Face(hb.Blob(tampon.getvalue())))
        self.cmap = self.tt.getBestCmap()
        self.gliflar = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm

    def sekillendir(self, metin: str):
        tampon = hb.Buffer()
        tampon.add_str(metin)
        tampon.guess_segment_properties()
        hb.shape(self.hb_font, tampon, {"kern": True, "liga": False})
        return [
            (self.tt.getGlyphName(bilgi.codepoint), konum.x_advance, konum.x_offset)
            for bilgi, konum in zip(tampon.glyph_infos, tampon.glyph_positions)
        ]


@lru_cache(maxsize=None)
def _yazi(ad: str) -> Yazi:
    return Yazi(ad)


def _parcalar(metin: str, aile: str):
    """Metni, her karakteri kapsayan font dosyasına göre ardışık parçalara böler."""
    yazilar = [_yazi(ad) for ad in AILELER[aile]]
    parcalar: list[tuple[Yazi, str]] = []
    for karakter in metin:
        yazi = next((y for y in yazilar if ord(karakter) in y.cmap), None)
        if yazi is None:
            raise ValueError(f"{aile} ailesinde karakter yok: {karakter!r}")
        if parcalar and parcalar[-1][0] is yazi:
            parcalar[-1] = (yazi, parcalar[-1][1] + karakter)
        else:
            parcalar.append((yazi, karakter))
    return parcalar


def genislik(metin: str, boyut: float, aile: str = "sans", aralik: float = 0) -> float:
    toplam = 0.0
    for yazi, parca in _parcalar(metin, aile):
        olcek = boyut / yazi.upem
        toplam += sum(ilerleme * olcek + aralik for _, ilerleme, _ in yazi.sekillendir(parca))
    return toplam


def yol(
    metin: str,
    x: float,
    y: float,
    boyut: float,
    renk: str,
    aile: str = "sans",
    hiza: str = "sol",
    aralik: float = 0,
) -> str:
    if hiza != "sol":
        olcu = genislik(metin, boyut, aile, aralik)
        x -= olcu if hiza == "sag" else olcu / 2
    d: list[str] = []
    imlec = x
    for yazi, parca in _parcalar(metin, aile):
        olcek = boyut / yazi.upem
        for glif, ilerleme, kayma in yazi.sekillendir(parca):
            kalem = SVGPathPen(yazi.gliflar, ntos=lambda n: f"{n:.1f}".rstrip("0").rstrip("."))
            donusum = (olcek, 0, 0, -olcek, imlec + kayma * olcek, y)
            yazi.gliflar[glif].draw(TransformPen(kalem, donusum))
            d.append(kalem.getCommands())
            imlec += ilerleme * olcek + aralik
    return f'<path fill="{renk}" d="{"".join(d)}"/>'


def sar(metin: str, boyut: float, azami: float, aile: str = "sans") -> list[str]:
    satirlar: list[str] = []
    satir = ""
    for kelime in metin.split():
        aday = f"{satir} {kelime}".strip()
        if genislik(aday, boyut, aile) <= azami:
            satir = aday
        else:
            satirlar.append(satir)
            satir = kelime
    satirlar.append(satir)
    return satirlar
