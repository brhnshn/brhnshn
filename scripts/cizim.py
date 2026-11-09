"""Profil görsellerini SVG olarak çizer."""
import re
from pathlib import Path

from icerik import CORVUS_LOGO, YIGIN, Iletisim, Proje, Tema
from metin import genislik, sar, yol
from veri import Profil

IKON_DIZINI = Path(__file__).resolve().parent / "ikonlar"

YILDIZ = "M12 2.6l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.5l-5.9 3.1 1.2-6.5L2.5 9.5l6.6-.9z"

HAREKET = """
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
"""


def _svg(genis: int, yuksek: int, govde: str, stil: str = "") -> str:
    stil_blogu = f"<style>{stil}{HAREKET}</style>" if stil else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{genis}" height="{yuksek}" '
        f'viewBox="0 0 {genis} {yuksek}">{stil_blogu}{govde}</svg>\n'
    )


def _seviye(sayi: int, esikler: tuple[int, int, int]) -> int:
    if not sayi:
        return 0
    return 1 + sum(sayi > esik for esik in esikler)


def _esikler(haftalar: list[list[int]]) -> tuple[int, int, int]:
    dolu = sorted(sayi for hafta in haftalar for sayi in hafta if sayi)
    if not dolu:
        return (0, 0, 0)
    return tuple(dolu[len(dolu) * oran // 4] for oran in (1, 2, 3))


def kahraman(profil: Profil, tema: Tema) -> str:
    genis, yuksek = 1200, 436
    kenar = 8
    adim = (genis - 2 * kenar + 4) / len(profil.haftalar)
    hucre = adim - 4
    takvim_ust = 236.0
    esikler = _esikler(profil.haftalar)

    sutunlar, maske = [], []
    for s, hafta in enumerate(profil.haftalar):
        x = kenar + s * adim
        hucreler = []
        for g, sayi in enumerate(hafta):
            y = takvim_ust + g * adim
            seviye = _seviye(sayi, esikler)
            renk = tema.seviyeler[seviye - 1] if seviye else tema.bos
            kare = f'x="{x:.1f}" y="{y:.1f}" width="{hucre:.1f}" height="{hucre:.1f}" rx="3"'
            hucreler.append(f'<rect {kare} fill="{renk}"/>')
            if seviye:
                maske.append(f'<rect {kare} fill="#fff"/>')
        sutunlar.append("".join(hucreler))

    govde = [
        yol("Burhan Şahin", kenar, 104, 88, tema.metin, "sans-kalin", aralik=-2.4),
        yol("Full-stack geliştirici", kenar, 154, 32, tema.vurgu, "sans-kalin", aralik=-0.3),
        yol("Hafif, hızlı, kendi sunucunda çalışan yazılımlar yapıyorum.", kenar, 196, 28, tema.soluk),
        yol(f"{profil.toplam_katki}", genis - kenar, 104, 56, tema.metin, "sans-kalin", "sag", -1),
        yol("son 12 ayda katkı", genis - kenar, 140, 20, tema.soluk, "mono", "sag"),
        "".join(sutunlar),
        f'<mask id="m">{"".join(maske)}</mask>',
        f'<linearGradient id="g"><stop offset="0" stop-color="{tema.isik}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{tema.isik}" stop-opacity=".75"/>'
        f'<stop offset="1" stop-color="{tema.isik}" stop-opacity="0"/></linearGradient>',
        f'<g mask="url(#m)"><rect class="i" x="-240" y="{takvim_ust:.0f}" width="240" '
        f'height="{7 * adim:.0f}" fill="url(#g)"/></g>',
    ]
    # Hücreler animasyona bağlı değil; ışık çalışmazsa takvim yine tam görünür.
    stil = (
        ".i{animation:k 11s linear infinite}"
        f"@keyframes k{{to{{transform:translateX({genis + 240}px)}}}}"
    )
    return _svg(genis, yuksek, "".join(govde), stil)


def _piksel(harita: tuple[str, ...], x: float, y: float, hucre: float, tema: Tema) -> str:
    bosluk = max(1, round(hucre / 6))
    parcalar = []
    for s, satir in enumerate(harita):
        for k, karakter in enumerate(satir):
            if karakter == ".":
                continue
            renk = tema.vurgu if karakter == "#" else tema.seviyeler[1]
            parcalar.append(
                f'<rect x="{x + k * (hucre + bosluk):.1f}" y="{y + s * (hucre + bosluk):.1f}" '
                f'width="{hucre}" height="{hucre}" rx="1" fill="{renk}"/>'
            )
    return "".join(parcalar)


def _cerceve(genis: int, yuksek: int, tema: Tema) -> str:
    return (
        f'<rect x=".5" y=".5" width="{genis - 1}" height="{yuksek - 1}" rx="12" '
        f'fill="{tema.yuzey}" stroke="{tema.cizgi}"/>'
    )


def _yildiz(sayi: int, x_sag: float, y: float, boyut: float, tema: Tema) -> str:
    if not sayi:
        return ""
    metin = str(sayi)
    metin_genis = genislik(metin, boyut, "mono")
    ikon = boyut + 2
    ikon_x = x_sag - metin_genis - ikon - 5
    olcek = ikon / 24
    return (
        f'<path transform="translate({ikon_x:.1f} {y - ikon + 2:.1f}) scale({olcek:.3f})" '
        f'fill="{tema.soluk}" d="{YILDIZ}"/>'
        + yol(metin, x_sag, y, boyut, tema.soluk, "mono", "sag")
    )


def proje_karti(proje: Proje, yildiz: int, tema: Tema) -> str:
    genis, yuksek, ic = 410, 188, 22
    hucre = 5
    ikon_genis = len(proje.piksel[0]) * (hucre + 1) - 1
    ikon_x = genis - ic - ikon_genis
    satirlar = sar(proje.aciklama, 15, genis - 2 * ic)
    if len(satirlar) > 3:
        raise ValueError(f"{proje.ad}: açıklama karta sığmıyor")
    baslik_genis = genislik(proje.ad, 23, "sans-kalin", -0.3)
    govde = [
        _cerceve(genis, yuksek, tema),
        yol(proje.ad, ic, 49, 23, tema.metin, "sans-kalin", aralik=-0.3),
        _yildiz(yildiz, ic + baslik_genis + 52, 48, 13, tema),
        _piksel(proje.piksel, ikon_x, ic, hucre, tema),
    ]
    for sira, satir in enumerate(satirlar):
        govde.append(yol(satir, ic, 96 + sira * 22, 15, tema.soluk))
    govde.append(yol(proje.yigin, ic, yuksek - 20, 12.5, tema.vurgu, "mono"))
    return _svg(genis, yuksek, "".join(govde))


def corvus_logo(tema: Tema) -> str:
    return f'<path fill-rule="evenodd" fill="{tema.vurgu}" d="{CORVUS_LOGO}"/>'


def koy_logo() -> str:
    # Koy marka logosu (assets/branding/koy-symbol-flat.svg, 256 birim): marka mavisi, sabit renkler.
    return (
        '<rect x="32" y="32" width="192" height="192" rx="48" fill="#2563EB"/>'
        '<path fill="#93C5FD" d="M88 32C94 44 104 54 116 54H140C152 54 162 44 168 32Z"/>'
        '<rect x="76" y="82" width="30" height="108" rx="15" fill="#FFFFFF"/>'
        '<path fill="#FFFFFF" d="M106 136L148 88C154 82 164 81 170 87C176 93 176 102 170 107'
        'L134 143L170 179C176 184 176 193 170 199C164 205 154 204 148 198L106 148Z"/>'
    )


def one_cikan_karti(proje: Proje, logo: str, olgular: tuple[str, ...], yildiz: int, tema: Tema) -> str:
    genis, yuksek, ic = 826, 226, 32
    logo_boyut = 150
    logo_x = genis - ic - logo_boyut + 8
    metin_genis = logo_x - ic - 32
    ad_genis = genislik(proje.ad, 42, "sans-kalin", -0.9)
    govde = [
        _cerceve(genis, yuksek, tema),
        yol("Şu an üzerinde çalıştığım", ic, 48, 15, tema.vurgu, "mono"),
        yol(proje.ad, ic, 96, 42, tema.metin, "sans-kalin", aralik=-0.9),
        _yildiz(yildiz, ic + ad_genis + 58, 94, 15, tema),
        f'<g transform="translate({logo_x} 38) scale({logo_boyut / 256:.4f})">{logo}</g>',
    ]
    for sira, satir in enumerate(sar(proje.aciklama, 18, metin_genis)):
        govde.append(yol(satir, ic, 132 + sira * 27, 18, tema.soluk))
    olgu_x = float(ic)
    for olgu in (proje.yigin, *olgular):
        govde.append(yol(olgu, olgu_x, yuksek - 26, 14, tema.metin, "mono"))
        olgu_x += genislik(olgu, 14, "mono") + 26
    return _svg(genis, yuksek, "".join(govde))


def iletisim_karti(kart: Iletisim, tema: Tema) -> str:
    genis, yuksek, ic = 272, 92, 20
    hucre = 4
    ikon_boyut = len(kart.piksel) * (hucre + 1) - 1
    metin_x = ic + ikon_boyut + 16
    govde = [
        _cerceve(genis, yuksek, tema),
        _piksel(kart.piksel, ic, (yuksek - ikon_boyut) / 2, hucre, tema),
        yol(kart.ad, metin_x, 42, 18, tema.metin, "sans-kalin", aralik=-0.2),
        yol(kart.deger, metin_x, 64, 11.5, tema.soluk, "mono"),
    ]
    return _svg(genis, yuksek, "".join(govde))


def _ikon(dosya: str, x: float, y: float, boyut: float, renk: str) -> str:
    kaynak = (IKON_DIZINI / f"{dosya}.svg").read_text(encoding="utf-8")
    d = re.search(r'<path d="([^"]+)"', kaynak).group(1)
    return (
        f'<path transform="translate({x:.1f} {y:.1f}) scale({boyut / 24:.3f})" '
        f'fill="{renk}" d="{d}"/>'
    )


def yigin(tema: Tema) -> str:
    genis, satir_yuksek, ic = 826, 104, 28
    etiket_genis = 126
    sutun = (genis - 2 * ic - etiket_genis) / 5
    yuksek = satir_yuksek * len(YIGIN) + 2 * 14
    govde = [_cerceve(genis, yuksek, tema)]
    for s, (grup, ogeler) in enumerate(YIGIN):
        y = 14 + s * satir_yuksek
        if s:
            govde.append(f'<path stroke="{tema.cizgi}" d="M{ic} {y}H{genis - ic}"/>')
        govde.append(yol(grup, ic, y + 58, 16, tema.soluk, "mono"))
        for k, (dosya, etiket) in enumerate(ogeler):
            orta = ic + etiket_genis + k * sutun + sutun / 2
            govde.append(_ikon(dosya, orta - 16, y + 20, 32, tema.metin))
            govde.append(yol(etiket, orta, y + 80, 15, tema.soluk, hiza="orta"))
    return _svg(genis, yuksek, "".join(govde))


def _tamsayi(deger: float) -> str:
    return f"%{deger:.0f}" if deger >= 1 else "%<1"


def istatistik(profil: Profil, tema: Tema) -> str:
    genis, ic = 826, 28
    gostergeler = (
        (str(profil.toplam_katki), "katkı"),
        (str(profil.aktif_gun), "aktif gün"),
        (str(profil.en_uzun_seri), "gün en uzun seri"),
        (str(profil.depo_sayisi), "açık kaynak depo"),
    )
    sutun = (genis - 2 * ic) / len(gostergeler)
    dil_ust = 176
    satir = 32
    yuksek = dil_ust + satir * len(profil.diller) + 20
    etiket_genis = 112
    sag_genis = 56
    bar_azami = genis - 2 * ic - etiket_genis - sag_genis
    en_buyuk = max(pay for _, pay in profil.diller)

    govde = [
        _cerceve(genis, yuksek, tema),
        yol("Son 12 ay", ic, 42, 14, tema.vurgu, "mono"),
    ]
    for sira, (deger, etiket) in enumerate(gostergeler):
        x = ic + sira * sutun
        govde.append(yol(deger, x, 92, 40, tema.metin, "sans-kalin", aralik=-0.8))
        govde.append(yol(etiket, x, 118, 15, tema.soluk))
    govde.append(yol("Açık kaynak depolarda dil payı", ic, dil_ust - 18, 14, tema.vurgu, "mono"))
    for sira, (ad, pay) in enumerate(profil.diller):
        y = dil_ust + sira * satir
        bar = max(4.0, bar_azami * pay / en_buyuk)
        renk = tema.soluk if ad == "Diğer" else tema.vurgu
        govde.append(yol(ad, ic, y + 16, 15, tema.metin))
        govde.append(
            f'<rect x="{ic + etiket_genis}" y="{y + 5}" width="{bar:.1f}" height="12" '
            f'rx="4" fill="{renk}"/>'
        )
        govde.append(yol(_tamsayi(pay), genis - ic, y + 16, 14, tema.soluk, "mono", "sag"))
    return _svg(genis, yuksek, "".join(govde))
