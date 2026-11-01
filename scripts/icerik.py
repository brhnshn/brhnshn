"""Görsellerdeki elle yazılan içerik: temalar, projeler, teknoloji yığını."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Tema:
    ad: str
    yuzey: str
    cizgi: str
    metin: str
    soluk: str
    vurgu: str
    bos: str
    seviyeler: tuple[str, str, str, str]
    isik: str


KOYU = Tema(
    ad="koyu",
    yuzey="#11161d",
    cizgi="#2a313c",
    metin="#e6edf3",
    soluk="#9198a1",
    vurgu="#f2b35a",
    bos="#171c24",
    seviyeler=("#533712", "#8f5e1d", "#cc8830", "#f2b35a"),
    isik="#ffe2b0",
)
ACIK = Tema(
    ad="acik",
    yuzey="#ffffff",
    cizgi="#d8dee4",
    metin="#1f2328",
    soluk="#59636e",
    vurgu="#96590f",
    bos="#eff1f3",
    seviyeler=("#f6dcb2", "#e9b266", "#cf8426", "#96590f"),
    isik="#fff3dc",
)
TEMALAR = (KOYU, ACIK)


@dataclass(frozen=True)
class Proje:
    dosya: str
    ad: str
    depo: str
    aciklama: str
    yigin: str
    piksel: tuple[str, ...]


CORVUS = Proje(
    dosya="corvus",
    ad="Corvus",
    depo="corvus",
    aciklama="Homelab ve VPS filoları için kendi sunucunda çalışan kontrol paneli: Docker, uptime, SSL ve herkese açık durum sayfası.",
    yigin=".NET 9 Native AOT · React · SQLite",
    piksel=(),
)
CORVUS_OLGULAR = ("Tek konteyner", "30 MB altı RAM")
CORVUS_LOGO = (
    "M128 20L196 59.27L246 88.13L174 116L164 98.68L128 77.9L76 107.92L76 148.08"
    "L128 178.1L164 157.32L198 176.95L128 217.4L34 163.14L34 74.86ZM148 62L168 73.55L148 82Z"
)

PROJELER = (
    Proje(
        dosya="apihub",
        ad="ApiHub",
        depo="ApiHub",
        aciklama="Tek Linux sunucuda Docker, domain, SSL, PostgreSQL ve e-postayı tek panelden yönetir.",
        yigin="C# · SignalR · Nginx · Docker",
        piksel=(
            "#########",
            "#+.+....#",
            "#########",
            ".........",
            "#########",
            "#+.+....#",
            "#########",
            "....#....",
            "..#####..",
        ),
    ),
    Proje(
        dosya="gokkalkan",
        ad="Gökkalkan",
        depo="gokkalkan",
        aciklama="Hava, tarım, denizcilik ve deprem için bölgesel erken uyarı radarı. PWA olarak çalışır.",
        yigin="TypeScript · React · Hono · Leaflet",
        piksel=(
            "#########",
            "#########",
            "##+++++##",
            "##+++++##",
            "##+++++##",
            ".##+++##.",
            ".##+++##.",
            "..#####..",
            "....#....",
        ),
    ),
    Proje(
        dosya="aulatray",
        ad="AulaTray",
        depo="AulaTray",
        aciklama="AULA kablosuz klavyeler için çok hafif Windows sistem tepsisi pil izleyicisi.",
        yigin="C# · .NET 9",
        piksel=(
            ".........",
            "########.",
            "#......#.",
            "#.+++..##",
            "#.+++..##",
            "#.+++..##",
            "#......#.",
            "########.",
            ".........",
        ),
    ),
    Proje(
        dosya="netpulse",
        ad="NetPulse",
        depo="NetPulse",
        aciklama="Mikro kesintileri yakalar, servis sağlayıcına sunabileceğin HMAC imzalı kanıt raporu üretir.",
        yigin="C# · .NET 8 · WinForms",
        piksel=(
            "...#.....",
            "...##....",
            "...##....",
            "..#.#....",
            "###.#..##",
            ".....#.#.",
            ".....#.#.",
            ".....##..",
            "......#..",
        ),
    ),
    Proje(
        dosya="goburhan",
        ad="GoBurhan",
        depo="GoBurhan",
        aciklama="Redis önbellekli, analitikli ve Telegram botlu, kendi sunucunda çalışan link kısaltıcı.",
        yigin="ASP.NET Core · PostgreSQL · Redis",
        piksel=(
            ".....#...",
            "......#..",
            ".......#.",
            "+.+.#####",
            ".......#.",
            "......#..",
            ".....#...",
        ),
    ),
    Proje(
        dosya="qrmenu",
        ad="QRMenu",
        depo="QRMenu",
        aciklama="Restoran ve kafeler için gerçek zamanlı QR sipariş ve otomasyon sistemi.",
        yigin="ASP.NET Core · SignalR · PostgreSQL",
        piksel=(
            "###.+.###",
            "#.#.+.#.#",
            "###.+.###",
            "...++....",
            "+.+.+.+.+",
            ".........",
            "###.+.+.+",
            "#.#..++..",
            "###.+.+.+",
        ),
    ),
)

@dataclass(frozen=True)
class Iletisim:
    dosya: str
    ad: str
    deger: str
    piksel: tuple[str, ...]


ILETISIM = (
    Iletisim(
        dosya="iletisim-site",
        ad="Web sitesi",
        deger="burhansahin.com.tr",
        piksel=(
            "..#####..",
            ".#..#..#.",
            "#..+#+..#",
            "#..+#+..#",
            "#########",
            "#..+#+..#",
            "#..+#+..#",
            ".#..#..#.",
            "..#####..",
        ),
    ),
    Iletisim(
        dosya="iletisim-linkedin",
        ad="LinkedIn",
        deger="in/burhan-sahin",
        piksel=(
            "#########",
            "##.######",
            "#########",
            "##.#...##",
            "##.#.#.##",
            "##.#.#.##",
            "##.#.#.##",
            "##.#.#.##",
            "#########",
        ),
    ),
    Iletisim(
        dosya="iletisim-eposta",
        ad="E-posta",
        deger="sahinburhan501@gmail.com",
        piksel=(
            ".........",
            "#########",
            "##+++++##",
            "#.##+##.#",
            "#..###..#",
            "#...#...#",
            "#.......#",
            "#########",
            ".........",
        ),
    ),
)

YIGIN = (
    ("Backend", (("dotnet", ".NET / C#"), ("postgresql", "PostgreSQL"), ("sqlite", "SQLite"), ("redis", "Redis"), ("python", "Python"))),
    ("Frontend", (("typescript", "TypeScript"), ("react", "React"), ("tailwindcss", "Tailwind"), ("vite", "Vite"), ("astro", "Astro"))),
    ("Altyapı", (("docker", "Docker"), ("nginx", "Nginx"), ("cloudflare", "Cloudflare"), ("linux", "Linux"), ("githubactions", "Actions"))),
)
