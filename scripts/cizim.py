"""Profil görsellerini SVG olarak çizer."""
import re
from pathlib import Path

from icerik import CORVUS_LOGO, YIGIN, Iletisim, Proje, Tema
from metin import genislik, sar, yol
from veri import Profil

IKON_DIZINI = Path(__file__).resolve().parent / "ikonlar"

YILDIZ = "M12 2.6l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.5l-5.9 3.1 1.2-6.5L2.5 9.5l6.6-.9z"
OK_DISA = "M7 17L17 7M9 7h8v8"

HAREKET = """
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
"""


def _svg(genis: int, yuksek: int, govde: str, stil: str = "") -> str:
    stil_blogu = f"<style>{stil}{HAREKET}</style>" if stil else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{genis}" height="{yuksek}" '
        f'viewBox="0 0 {genis} {yuksek}">{stil_blogu}{govde}</svg>\n'
    )


def _cerceve(genis: int, yuksek: int, rx: int, tema: Tema, cid: str) -> str:
    parlama_opak = "0.11" if tema.ad == "koyu" else "0.08"
    return (
        f'<defs>'
        f'<linearGradient id="bg-{cid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{tema.yuzey}"/>'
        f'<stop offset="1" stop-color="{tema.yuzey_alt}"/>'
        f'</linearGradient>'
        f'<radialGradient id="gl-{cid}" cx=".92" cy=".08" r=".62">'
        f'<stop offset="0" stop-color="{tema.parlama}" stop-opacity="{parlama_opak}"/>'
        f'<stop offset="1" stop-color="{tema.parlama}" stop-opacity="0"/>'
        f'</radialGradient>'
        f'<clipPath id="cl-{cid}"><rect width="{genis}" height="{yuksek}" rx="{rx}"/></clipPath>'
        f'</defs>'
        f'<g clip-path="url(#cl-{cid})">'
        f'<rect width="{genis}" height="{yuksek}" rx="{rx}" fill="url(#bg-{cid})"/>'
        f'<rect width="{genis}" height="{yuksek}" fill="url(#gl-{cid})"/>'
        f'<path stroke="{tema.cizgi_ic}" stroke-opacity="0.45" d="M{rx} 1H{genis - rx}"/>'
        f'</g>'
        f'<rect x=".5" y=".5" width="{genis - 1}" height="{yuksek - 1}" rx="{rx}" '
        f'fill="none" stroke="{tema.cizgi}"/>'
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


def _ok_ikonu(x: float, y: float, renk: str) -> str:
    return (
        f'<path transform="translate({x:.1f} {y:.1f}) scale(0.625)" '
        f'fill="none" stroke="{renk}" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round" d="{OK_DISA}"/>'
    )


def kahraman(profil: Profil, tema: Tema) -> str:
    genis, yuksek = 1200, 464
    tepsi_x, tepsi_y, tepsi_w, tepsi_h = 36, 244, 1128, 194
    takvim_x = 54
    takvim_ust = 282.0
    adim = (1092 + 4) / len(profil.haftalar)
    hucre = adim - 4
    esikler = _esikler(profil.haftalar)

    sutunlar, maske = [], []
    for s, hafta in enumerate(profil.haftalar):
        x = takvim_x + s * adim
        hucreler = []
        for g, sayi in enumerate(hafta):
            y = takvim_ust + g * adim
            seviye = _seviye(sayi, esikler)
            renk = tema.seviyeler[seviye - 1] if seviye else tema.bos
            kare = f'x="{x:.1f}" y="{y:.1f}" width="{hucre:.1f}" height="{hucre:.1f}" rx="3.5"'
            hucreler.append(f'<rect {kare} fill="{renk}"/>')
            if seviye:
                maske.append(f'<rect {kare} fill="#fff"/>')
        sutunlar.append("".join(hucreler))

    rozet_metin = "Full-stack Geliştirici · Açık Kaynak"
    rozet_w = genislik(rozet_metin, 13, "mono") + 42

    # Takvim legend (sağ üst köşe)
    legend_x = tepsi_x + tepsi_w - 18
    cok_w = genislik("Çok", 11.5, "mono")
    kareler_sol = legend_x - cok_w - 8 - 5 * 15 + 4
    az_x = kareler_sol - 8
    legend_kareler = []
    for i, renk in enumerate((tema.bos, *tema.seviyeler)):
        kx = kareler_sol + i * 15
        legend_kareler.append(f'<rect x="{kx:.1f}" y="258" width="11" height="11" rx="2.5" fill="{renk}"/>')

    govde = [
        _cerceve(genis, yuksek, 18, tema, f"hero-{tema.ad}"),
        # Sol üst durum rozeti
        f'<rect x="40" y="34" width="{rozet_w:.1f}" height="30" rx="15" '
        f'fill="{tema.yuzey2}" stroke="{tema.cizgi_ic}"/>',
        f'<circle cx="57" cy="49" r="4.5" fill="{tema.vurgu2}"/>',
        yol(rozet_metin, 70, 53.5, 13, tema.metin, "mono"),
        # Sağ üst katkı KPI özeti
        yol(f"{profil.toplam_katki}", genis - 40, 82, 54, tema.metin, "sans-kalin", "sag", -1.2),
        yol("son 12 ayda katkı", genis - 40, 108, 14, tema.vurgu, "mono", "sag"),
        yol(
            f"{profil.aktif_gun} aktif gün  ·  {profil.en_uzun_seri} gün seri",
            genis - 40,
            132,
            13,
            tema.soluk,
            "mono",
            "sag",
        ),
        # Başlık & Açıklama
        yol("Burhan Şahin", 40, 148, 68, tema.metin, "sans-kalin", aralik=-2.0),
        yol("C# ve .NET ile backend, TypeScript ve React ile arayüz yazıyorum.", 40, 190, 21.5, tema.metin),
        yol(
            "Az kaynakla çalışan, kurması kolay ve kendi sunucunda barınan yazılımlar yapıyorum.",
            40,
            218,
            18.5,
            tema.soluk,
        ),
        # İç ısı haritası tepsisi
        f'<rect x="{tepsi_x}" y="{tepsi_y}" width="{tepsi_w}" height="{tepsi_h}" rx="12" '
        f'fill="{tema.yuzey2}" stroke="{tema.cizgi}"/>',
        yol("KATKI TAKVİMİ · SON 52 HAFTA", takvim_x, 267, 11.5, tema.soluk2, "mono"),
        yol("Az", az_x, 267, 11.5, tema.soluk2, "mono", "sag"),
        "".join(legend_kareler),
        yol("Çok", legend_x, 267, 11.5, tema.soluk2, "mono", "sag"),
        "".join(sutunlar),
        f'<mask id="m-{tema.ad}">{"".join(maske)}</mask>',
        f'<linearGradient id="g-{tema.ad}"><stop offset="0" stop-color="{tema.isik}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{tema.isik}" stop-opacity=".65"/>'
        f'<stop offset="1" stop-color="{tema.isik}" stop-opacity="0"/></linearGradient>',
        f'<g mask="url(#m-{tema.ad})"><rect class="i" x="-240" y="{takvim_ust:.0f}" width="240" '
        f'height="{7 * adim:.0f}" fill="url(#g-{tema.ad})"/></g>',
    ]
    stil = (
        ".i{animation:k 11s linear infinite}"
        f"@keyframes k{{to{{transform:translateX({genis + 240}px)}}}}"
    )
    return _svg(genis, yuksek, "".join(govde), stil)


def _proje_ikonu(ikon: str, x: float, y: float, tema: Tema) -> str:
    """42x42 boyutunda proje marka/ürün vektör ikonu çizer."""
    if ikon == "koy":
        # Koy marka logosu (192 iç kutu -> tam 42x42 birim)
        return (
            f'<g transform="translate({x - 7.0:.2f} {y - 7.0:.2f}) scale(0.21875)">'
            '<rect x="32" y="32" width="192" height="192" rx="48" fill="#2563EB"/>'
            '<path fill="#93C5FD" d="M88 32C94 44 104 54 116 54H140C152 54 162 44 168 32Z"/>'
            '<rect x="76" y="82" width="30" height="108" rx="15" fill="#FFFFFF"/>'
            '<path fill="#FFFFFF" d="M106 136L148 88C154 82 164 81 170 87C176 93 176 102 170 107'
            'L134 143L170 179C176 184 176 193 170 199C164 205 154 204 148 198L106 148Z"/>'
            '</g>'
        )
    if ikon == "agy":
        # agy-context-studio marka logosu (orijinal 64 birim -> 42 birim)
        return (
            f'<g transform="translate({x:.1f} {y:.1f}) scale(0.65625)">'
            '<rect x="2" y="2" width="60" height="60" rx="16" fill="#0F172A" stroke="#334155" stroke-width="2"/>'
            '<path d="M18 40 A16 16 0 1 1 46 40" fill="none" stroke="#334155" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M18 40 A16 16 0 0 1 43.2 21.8" fill="none" stroke="#38BDF8" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M32 32 L41 23" fill="none" stroke="#F8FAFC" stroke-width="3" stroke-linecap="round"/>'
            '<circle cx="32" cy="32" r="3.5" fill="#F8FAFC"/>'
            '<rect x="20" y="45" width="24" height="3.5" rx="1.75" fill="#475569"/>'
            '<rect x="20" y="45" width="16" height="3.5" rx="1.75" fill="#38BDF8"/>'
            '</g>'
        )

    kutu = f'<rect x="{x}" y="{y}" width="42" height="42" rx="11" fill="{tema.yuzey2}" stroke="{tema.cizgi_ic}"/>'
    if ikon == "corvus":
        return (
            kutu
            + f'<g transform="translate({x + 7:.1f} {y + 8:.1f}) scale(0.11)">'
            f'<path fill-rule="evenodd" fill="{tema.vurgu}" d="{CORVUS_LOGO}"/></g>'
        )
    if ikon == "aulatray":
        # Pil göstergesi vektör ikonu
        return (
            kutu
            + f'<g transform="translate({x + 9:.1f} {y + 9:.1f})" fill="none" stroke="{tema.vurgu}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="2" y="6" width="16" height="12" rx="2.5"/>'
            '<path d="M21 10v4"/>'
            f'<rect x="5" y="9" width="7" height="6" rx="1" fill="{tema.vurgu2}" stroke="none"/>'
            '</g>'
        )
    if ikon == "netpulse":
        # Ağ nabız / dalga vektör ikonu
        return (
            kutu
            + f'<g transform="translate({x + 9:.1f} {y + 9:.1f})" fill="none" stroke="{tema.vurgu}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M2 12h4l2.5-6 4 12 3-8 2 2h4.5"/>'
            '</g>'
        )
    # qrmenu: QR ızgara vektör ikonu
    return (
        kutu
        + f'<g transform="translate({x + 9:.1f} {y + 9:.1f})" fill="none" stroke="{tema.vurgu}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="7" height="7" rx="1.5"/>'
        '<rect x="14" y="3" width="7" height="7" rx="1.5"/>'
        '<rect x="3" y="14" width="7" height="7" rx="1.5"/>'
        f'<rect x="14" y="14" width="3" height="3" rx=".5" fill="{tema.vurgu2}" stroke="none"/>'
        f'<rect x="18" y="18" width="3" height="3" rx=".5" fill="{tema.vurgu}" stroke="none"/>'
        '</g>'
    )


def _yildiz_rozeti(sayi: int, x_sag: float, y: float, tema: Tema) -> str:
    if not sayi:
        return ""
    metin = str(sayi)
    metin_w = genislik(metin, 12, "mono")
    pill_w = metin_w + 30
    pill_x = x_sag - pill_w
    return (
        f'<rect x="{pill_x:.1f}" y="{y}" width="{pill_w:.1f}" height="24" rx="12" '
        f'fill="{tema.vurgu_yumusak}" stroke="{tema.cizgi_ic}"/>'
        f'<path transform="translate({pill_x + 8:.1f} {y + 5.5:.1f}) scale(0.54)" '
        f'fill="{tema.vurgu}" d="{YILDIZ}"/>'
        + yol(metin, x_sag - 9, y + 16, 12, tema.metin, "mono", "sag")
    )


def proje_karti(proje: Proje, yildiz: int, tema: Tema) -> str:
    genis, yuksek, ic = 410, 202, 22
    satirlar = sar(proje.aciklama, 14.5, genis - 2 * ic)
    if len(satirlar) > 3:
        raise ValueError(f"{proje.ad}: açıklama karta sığmıyor")

    govde = [
        _cerceve(genis, yuksek, 14, tema, f"{proje.dosya}-{tema.ad}"),
        _proje_ikonu(proje.ikon, ic, 22, tema),
        yol(proje.ad, ic + 54, 41, 19.5, tema.metin, "sans-kalin", aralik=-0.3),
        yol(proje.kategori, ic + 54, 59, 11.5, tema.vurgu, "mono"),
        _ok_ikonu(genis - ic - 15, 25, tema.soluk2),
        _yildiz_rozeti(yildiz, genis - ic - 24, 21, tema),
    ]
    for sira, satir in enumerate(satirlar):
        govde.append(yol(satir, ic, 91 + sira * 21, 14.5, tema.soluk))

    govde.append(
        f'<path stroke="{tema.cizgi}" stroke-opacity="0.65" d="M{ic} 148H{genis - ic}"/>'
    )
    pill_x = float(ic)
    for etiket in proje.etiketler:
        w = genislik(etiket, 11.5, "mono") + 18
        govde.append(
            f'<rect x="{pill_x:.1f}" y="160" width="{w:.1f}" height="24" rx="6" '
            f'fill="{tema.yuzey2}" stroke="{tema.cizgi_ic}"/>'
        )
        govde.append(yol(etiket, pill_x + 9, 176, 11.5, tema.metin, "mono"))
        pill_x += w + 8

    return _svg(genis, yuksek, "".join(govde))


def _iletisim_ikonu(ikon: str, x: float, y: float, renk: str) -> str:
    if ikon == "site":
        return (
            f'<g transform="translate({x:.1f} {y:.1f})" fill="none" stroke="{renk}" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="9.5"/>'
            '<path d="M2.5 12h19M12 2.5a14 14 0 0 1 0 19M12 2.5a14 14 0 0 0 0 19"/>'
            '</g>'
        )
    if ikon == "linkedin":
        return (
            f'<g transform="translate({x:.1f} {y:.1f})" fill="none" stroke="{renk}" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="3" y="3" width="18" height="18" rx="4"/>'
            '<path d="M8 11v5M8 8v.01M12 16v-5M16 16v-3a2 2 0 0 0-4 0"/>'
            '</g>'
        )
    return (
        f'<g transform="translate({x:.1f} {y:.1f})" fill="none" stroke="{renk}" '
        'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2.5" y="4.5" width="19" height="15" rx="3"/>'
        '<path d="M3.5 6l8.5 6.5L20.5 6"/>'
        '</g>'
    )


def iletisim_karti(kart: Iletisim, tema: Tema) -> str:
    genis, yuksek, ic = 272, 94, 18
    kutu_boyut = 44
    metin_x = ic + kutu_boyut + 14
    govde = [
        _cerceve(genis, yuksek, 14, tema, f"{kart.dosya}-{tema.ad}"),
        f'<rect x="{ic}" y="{(yuksek - kutu_boyut) / 2}" width="{kutu_boyut}" height="{kutu_boyut}" '
        f'rx="11" fill="{tema.vurgu_yumusak}" stroke="{tema.cizgi_ic}"/>',
        _iletisim_ikonu(kart.ikon, ic + 10, (yuksek - 24) / 2, tema.vurgu),
        _ok_ikonu(genis - 26, 14, tema.soluk2),
        yol(kart.ad, metin_x, 42, 16.5, tema.metin, "sans-kalin", aralik=-0.2),
        yol(kart.deger, metin_x, 63, 11.5, tema.soluk, "mono"),
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
    genis, yuksek, ic = 826, 316, 24
    kol_w = 246
    kol_gap = 20
    kol_renkler = (tema.vurgu, tema.vurgu2, tema.vurgu_acik)

    govde = [
        _cerceve(genis, yuksek, 16, tema, f"yigin-{tema.ad}"),
        yol("TEKNOLOJİ YIĞINI", ic, 34, 12, tema.vurgu, "mono"),
        yol("Üretimde düzenli kullandığım araçlar", genis - ic, 34, 12, tema.soluk2, "mono", "sag"),
    ]
    for s, (grup, ogeler) in enumerate(YIGIN):
        px = ic + s * (kol_w + kol_gap)
        py = 52
        ph = 240
        govde.append(
            f'<rect x="{px}" y="{py}" width="{kol_w}" height="{ph}" rx="12" '
            f'fill="{tema.yuzey2}" stroke="{tema.cizgi_ic}"/>'
        )
        govde.append(f'<circle cx="{px + 18}" cy="{py + 21}" r="4" fill="{kol_renkler[s]}"/>')
        govde.append(yol(grup, px + 30, py + 26, 15, tema.metin, "sans-kalin"))
        govde.append(yol(f"{len(ogeler)}", px + kol_w - 16, py + 25, 11.5, tema.soluk2, "mono", "sag"))
        govde.append(f'<path stroke="{tema.cizgi}" d="M{px + 14} {py + 42}H{px + kol_w - 14}"/>')
        for k, (dosya, etiket) in enumerate(ogeler):
            ry = py + 54 + k * 36
            govde.append(
                f'<rect x="{px + 14}" y="{ry}" width="26" height="26" rx="7" '
                f'fill="{tema.yuzey}" stroke="{tema.cizgi}"/>'
            )
            govde.append(_ikon(dosya, px + 19, ry + 5, 16, tema.metin))
            govde.append(yol(etiket, px + 50, ry + 18, 14, tema.metin))
    return _svg(genis, yuksek, "".join(govde))


def _tamsayi(deger: float) -> str:
    return f"%{deger:.0f}" if deger >= 1 else "%<1"


def istatistik(profil: Profil, tema: Tema) -> str:
    genis, yuksek, ic = 826, 308, 24
    gostergeler = (
        (str(profil.toplam_katki), "Toplam Katkı", tema.vurgu),
        (str(profil.aktif_gun), "Aktif Gün", tema.vurgu2),
        (str(profil.en_uzun_seri), "Gün En Uzun Seri", tema.vurgu_acik),
        (str(profil.depo_sayisi), "Açık Kaynak Depo", tema.vurgu),
    )
    kart_gap = 12
    kart_w = (genis - 2 * ic - 3 * kart_gap) / 4

    govde = [
        _cerceve(genis, yuksek, 16, tema, f"stat-{tema.ad}"),
        yol("SON 12 AY · GİTHUB VERİSİ", ic, 34, 12, tema.vurgu, "mono"),
        yol("Her gün otomatik güncellenir", genis - ic, 34, 12, tema.soluk2, "mono", "sag"),
    ]
    for sira, (deger, etiket, renk) in enumerate(gostergeler):
        kx = ic + sira * (kart_w + kart_gap)
        ky = 52
        govde.append(
            f'<rect x="{kx:.1f}" y="{ky}" width="{kart_w:.1f}" height="96" rx="12" '
            f'fill="{tema.yuzey2}" stroke="{tema.cizgi_ic}"/>'
        )
        govde.append(f'<rect x="{kx + 16:.1f}" y="{ky + 16}" width="22" height="3" rx="1.5" fill="{renk}"/>')
        govde.append(yol(deger, kx + 16, ky + 56, 34, tema.metin, "sans-kalin", aralik=-0.8))
        govde.append(yol(etiket, kx + 16, ky + 80, 12.5, tema.soluk))

    # Yığılmış dil dağılım çubuğu
    bar_x, bar_y, bar_w, bar_h = ic, 194, genis - 2 * ic, 14
    govde.append(yol("Açık Kaynak Depolarda Dil Dağılımı", ic, 178, 14, tema.metin, "sans-kalin"))
    govde.append(
        f'<defs><clipPath id="bar-{tema.ad}">'
        f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7"/>'
        f'</clipPath></defs>'
    )
    parcalar = []
    imlec = float(bar_x)
    toplam_pay = sum(pay for _, pay in profil.diller) or 100.0
    for idx, (ad, pay) in enumerate(profil.diller):
        gen = bar_w * (pay / toplam_pay)
        if idx == len(profil.diller) - 1:
            gen = bar_x + bar_w - imlec
        renk = tema.dil_renkleri.get(ad, tema.vurgu)
        parcalar.append(
            f'<rect x="{imlec:.1f}" y="{bar_y}" width="{max(2.0, gen - 1.5):.1f}" '
            f'height="{bar_h}" fill="{renk}"/>'
        )
        imlec += gen
    govde.append(f'<g clip-path="url(#bar-{tema.ad})">{"".join(parcalar)}</g>')

    # 3 sütun × 2 satır dil lejantı
    kol_gen = bar_w / 3
    for sira, (ad, pay) in enumerate(profil.diller):
        sutun = sira % 3
        satir = sira // 3
        lx = ic + sutun * kol_gen
        ly = 236 + satir * 32
        renk = tema.dil_renkleri.get(ad, tema.vurgu)
        govde.append(f'<rect x="{lx:.1f}" y="{ly - 10}" width="10" height="10" rx="3" fill="{renk}"/>')
        govde.append(yol(ad, lx + 18, ly, 13.5, tema.metin))
        sag_pad = 24 if sutun < 2 else 0
        govde.append(yol(_tamsayi(pay), lx + kol_gen - sag_pad, ly, 13, tema.soluk, "mono", "sag"))

    return _svg(genis, yuksek, "".join(govde))
