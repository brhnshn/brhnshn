"""Profil görsellerini gerçek GitHub verisinden üretir: python scripts/uret.py"""
from pathlib import Path

import cizim
from icerik import CORVUS, ILETISIM, PROJELER, TEMALAR
from veri import profil_getir

CIKTI = Path(__file__).resolve().parent.parent / "assets" / "gorseller"


def yaz(ad: str, svg: str) -> None:
    (CIKTI / ad).write_text(svg, encoding="utf-8", newline="\n")


def main() -> None:
    profil = profil_getir()
    CIKTI.mkdir(parents=True, exist_ok=True)
    for tema in TEMALAR:
        yaz(f"kahraman-{tema.ad}.svg", cizim.kahraman(profil, tema))
        yaz(f"istatistik-{tema.ad}.svg", cizim.istatistik(profil, tema))
        yaz(f"yigin-{tema.ad}.svg", cizim.yigin(tema))
        yaz(
            f"corvus-{tema.ad}.svg",
            cizim.corvus_karti(profil.yildizlar.get(CORVUS.depo, 0), tema),
        )
        for kart in ILETISIM:
            yaz(f"{kart.dosya}-{tema.ad}.svg", cizim.iletisim_karti(kart, tema))
        for proje in PROJELER:
            yaz(
                f"{proje.dosya}-{tema.ad}.svg",
                cizim.proje_karti(proje, profil.yildizlar.get(proje.depo, 0), tema),
            )


if __name__ == "__main__":
    main()
