"""GitHub'dan gerçek profil verisini çeker ve özetler."""
import json
import os
import urllib.request
from dataclasses import dataclass

KULLANICI = "brhnshn"
GOSTERILEN_DIL = 5

SORGU = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
    repositories(first: 100, privacy: PUBLIC, isFork: false, ownerAffiliations: OWNER) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


@dataclass
class Profil:
    haftalar: list[list[int]]
    toplam_katki: int
    aktif_gun: int
    en_uzun_seri: int
    depo_sayisi: int
    yildizlar: dict[str, int]
    diller: list[tuple[str, float]]


def _graphql() -> dict:
    jeton = os.environ["GITHUB_TOKEN"]
    govde = json.dumps({"query": SORGU, "variables": {"login": KULLANICI}}).encode()
    istek = urllib.request.Request(
        "https://api.github.com/graphql",
        data=govde,
        headers={"Authorization": f"bearer {jeton}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(istek, timeout=30) as yanit:
        sonuc = json.load(yanit)
    if sonuc.get("errors"):
        raise RuntimeError(sonuc["errors"])
    return sonuc["data"]["user"]


def _en_uzun_seri(gunler: list[int]) -> int:
    en_uzun = seri = 0
    for sayi in gunler:
        seri = seri + 1 if sayi else 0
        en_uzun = max(en_uzun, seri)
    return en_uzun


def _dil_paylari(depolar: list[dict]) -> list[tuple[str, float]]:
    baytlar: dict[str, int] = {}
    for depo in depolar:
        for kenar in depo["languages"]["edges"]:
            ad = kenar["node"]["name"]
            baytlar[ad] = baytlar.get(ad, 0) + kenar["size"]
    toplam = sum(baytlar.values()) or 1
    sirali = sorted(baytlar.items(), key=lambda oge: oge[1], reverse=True)
    paylar = [(ad, bayt / toplam * 100) for ad, bayt in sirali[:GOSTERILEN_DIL]]
    kalan = sum(bayt for _, bayt in sirali[GOSTERILEN_DIL:])
    if kalan:
        paylar.append(("Diğer", kalan / toplam * 100))
    return paylar


def profil_getir() -> Profil:
    kullanici = _graphql()
    takvim = kullanici["contributionsCollection"]["contributionCalendar"]
    haftalar = [
        [gun["contributionCount"] for gun in hafta["contributionDays"]]
        for hafta in takvim["weeks"]
    ]
    gunler = [sayi for hafta in haftalar for sayi in hafta]
    depolar = kullanici["repositories"]["nodes"]
    return Profil(
        haftalar=haftalar,
        toplam_katki=takvim["totalContributions"],
        aktif_gun=sum(1 for sayi in gunler if sayi),
        en_uzun_seri=_en_uzun_seri(gunler),
        depo_sayisi=kullanici["repositories"]["totalCount"],
        yildizlar={depo["name"]: depo["stargazerCount"] for depo in depolar},
        diller=_dil_paylari(depolar),
    )
