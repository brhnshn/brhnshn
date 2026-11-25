"""Görsellerdeki elle yazılan içerik: temalar, projeler, teknoloji yığını."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Tema:
    ad: str
    yuzey: str
    yuzey_alt: str
    yuzey2: str
    cizgi: str
    cizgi_ic: str
    metin: str
    soluk: str
    soluk2: str
    vurgu: str
    vurgu_acik: str
    vurgu_yumusak: str
    vurgu2: str
    vurgu2_yumusak: str
    bos: str
    seviyeler: tuple[str, str, str, str]
    isik: str
    parlama: str
    dil_renkleri: dict[str, str]


KOYU = Tema(
    ad="koyu",
    yuzey="#121822",
    yuzey_alt="#0d121a",
    yuzey2="#182130",
    cizgi="#243044",
    cizgi_ic="#2f3e57",
    metin="#f1f5f9",
    soluk="#94a3b8",
    soluk2="#64748b",
    vurgu="#38bdf8",
    vurgu_acik="#7dd3fc",
    vurgu_yumusak="#132a40",
    vurgu2="#34d399",
    vurgu2_yumusak="#102c26",
    bos="#17202d",
    seviyeler=("#15354b", "#1c5778", "#2585b3", "#38bdf8"),
    isik="#bae6fd",
    parlama="#0ea5e9",
    dil_renkleri={
        "C#": "#a78bfa",
        "TypeScript": "#38bdf8",
        "HTML": "#fb923c",
        "JavaScript": "#facc15",
        "CSS": "#34d399",
        "Python": "#60a5fa",
        "Astro": "#f472b6",
        "Shell": "#94a3b8",
        "Diğer": "#64748b",
    },
)

ACIK = Tema(
    ad="acik",
    yuzey="#ffffff",
    yuzey_alt="#f5f8fc",
    yuzey2="#eef3f9",
    cizgi="#dce4ef",
    cizgi_ic="#cbd5e1",
    metin="#0f172a",
    soluk="#475569",
    soluk2="#64748b",
    vurgu="#0284c7",
    vurgu_acik="#0369a1",
    vurgu_yumusak="#e0f2fe",
    vurgu2="#059669",
    vurgu2_yumusak="#d1fae5",
    bos="#dce5f0",
    seviyeler=("#bae6fd", "#7dd3fc", "#38bdf8", "#0284c7"),
    isik="#ffffff",
    parlama="#38bdf8",
    dil_renkleri={
        "C#": "#7c3aed",
        "TypeScript": "#0284c7",
        "HTML": "#ea580c",
        "JavaScript": "#ca8a04",
        "CSS": "#059669",
        "Python": "#2563eb",
        "Astro": "#db2777",
        "Shell": "#475569",
        "Diğer": "#64748b",
    },
)

TEMALAR = (KOYU, ACIK)


@dataclass(frozen=True)
class Proje:
    dosya: str
    ad: str
    depo: str
    url: str
    kategori: str
    aciklama: str
    etiketler: tuple[str, ...]
    ikon: str


CORVUS_LOGO = (
    "M128 20L196 59.27L246 88.13L174 116L164 98.68L128 77.9L76 107.92L76 148.08"
    "L128 178.1L164 157.32L198 176.95L128 217.4L34 163.14L34 74.86ZM148 62L168 73.55L148 82Z"
)

PROJELER = (
    Proje(
        dosya="koy",
        ad="Koy",
        depo="koy",
        url="https://github.com/koyhq/koy",
        kategori="Masaüstü · Windows 11",
        aciklama="Windows 11 için hafif, tarayıcısız, yay animasyonlu Notch ve akıllı masaüstü Dock'u.",
        etiketler=("C#", ".NET 10", "WPF"),
        ikon="koy",
    ),
    Proje(
        dosya="agy-context-studio",
        ad="agy-context-studio",
        depo="agy-context-studio",
        url="https://github.com/brhnshn/agy-context-studio",
        kategori="Geliştirici Aracı",
        aciklama="Google Antigravity için sıfır token maliyetli canlı bağlam penceresi izleyicisi ve yöneticisi.",
        etiketler=("TypeScript", "React", "Node.js"),
        ikon="agy",
    ),
    Proje(
        dosya="corvus",
        ad="Corvus",
        depo="corvus",
        url="https://github.com/brhnshn/corvus",
        kategori="Sunucu Kontrol Paneli",
        aciklama="Homelab ve VPS filoları için 30 MB altı RAM kullanan, tek konteynerli kontrol paneli.",
        etiketler=(".NET 9 AOT", "React", "SQLite"),
        ikon="corvus",
    ),
    Proje(
        dosya="aulatray",
        ad="AulaTray",
        depo="AulaTray",
        url="https://github.com/brhnshn/AulaTray",
        kategori="Sistem Tepsisi",
        aciklama="AULA kablosuz klavyeler için çok hafif Windows sistem tepsisi pil izleyicisi.",
        etiketler=("C#", ".NET 9", "Windows"),
        ikon="aulatray",
    ),
    Proje(
        dosya="netpulse",
        ad="NetPulse",
        depo="NetPulse",
        url="https://github.com/brhnshn/NetPulse",
        kategori="Ağ İzleme",
        aciklama="Mikro kesintileri yakalar, servis sağlayıcına sunabileceğin HMAC imzalı kanıt raporu üretir.",
        etiketler=("C#", ".NET 8", "WinForms"),
        ikon="netpulse",
    ),
    Proje(
        dosya="qrmenu",
        ad="QRMenu",
        depo="QRMenu",
        url="https://github.com/brhnshn/QRMenu",
        kategori="Gerçek Zamanlı Sistem",
        aciklama="Restoran ve kafeler için gerçek zamanlı QR sipariş ve masa otomasyon sistemi.",
        etiketler=("ASP.NET Core", "SignalR", "PostgreSQL"),
        ikon="qrmenu",
    ),
)


@dataclass(frozen=True)
class Iletisim:
    dosya: str
    ad: str
    deger: str
    ikon: str


ILETISIM = (
    Iletisim(
        dosya="iletisim-site",
        ad="Web sitesi",
        deger="burhansahin.com.tr",
        ikon="site",
    ),
    Iletisim(
        dosya="iletisim-linkedin",
        ad="LinkedIn",
        deger="in/burhan-sahin",
        ikon="linkedin",
    ),
    Iletisim(
        dosya="iletisim-eposta",
        ad="E-posta",
        deger="me@burhansahin.com.tr",
        ikon="eposta",
    ),
)

YIGIN = (
    (
        "Backend",
        (("dotnet", ".NET / C#"), ("postgresql", "PostgreSQL"), ("sqlite", "SQLite"), ("redis", "Redis"), ("python", "Python")),
    ),
    (
        "Frontend",
        (("typescript", "TypeScript"), ("react", "React"), ("tailwindcss", "Tailwind"), ("vite", "Vite"), ("astro", "Astro")),
    ),
    (
        "Altyapı",
        (("docker", "Docker"), ("nginx", "Nginx"), ("cloudflare", "Cloudflare"), ("linux", "Linux"), ("githubactions", "Actions")),
    ),
)
