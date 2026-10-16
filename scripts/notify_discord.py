"""Krótki, czytelny raport tygodnia: zapis do reports/raport.md i wysyłka na Discord.

Czyta wyniki scripts/evaluate.py (ranking.csv, ranking_tanie.csv, sealed_ranking.csv, market.json).
Adres webhooka bierze ze zmiennej DISCORD_WEBHOOK (sekret w GitHub Actions); bez niej tylko zapisuje plik.

    python scripts/notify_discord.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CATALOG = ROOT / "data" / "catalog"
REPO_URL = "https://github.com/krystiangniotyspam-maker/pokescout/blob/main/reports"
RARITY_SHORT = {"special illustration rare": "SIR", "illustration rare": "IR", "hyper rare": "złota",
                "ultra rare": "UR", "secret rare": "secret", "double rare": "ex", "classic collection": "Classic"}


def _read(name: str) -> pd.DataFrame:
    f = REPORTS / name
    return pd.read_csv(f) if f.exists() else pd.DataFrame()


def _set(name: str) -> str:  # „SV: Shrouded Fable” → „Shrouded Fable”
    return str(name).split(": ", 1)[-1]


def _cm_link(query: str) -> str:
    return f"https://www.cardmarket.com/en/Pokemon/Products/Search?searchString={quote_plus(query)}"


def _card_line(i: int, r, rarity: dict) -> str:
    rar = RARITY_SHORT.get(str(rarity.get(r.card_id, "")).lower(), "")
    name = f"{r['name']} {rar}".strip()
    base = str(r["name"]).split(" - ")[0].split(" (")[0]
    warn = " ⚠️ dodruk" if r.get("dodruk_posty", 0) >= 3 else ""
    line = (f"{i}. **[{name}](https://www.tcgplayer.com/product/{r.card_id})** · {_set(r.set_name)} · "
            f"${r.price_now:.0f} · [Cardmarket]({_cm_link(base)}){warn}")
    if pd.notna(r.get("potencjal_rok")):
        p = r.price_now
        line += (f"\n   📈 **za rok ok. {r.potencjal_rok:+.0%} → ok. ${p * (1 + r.potencjal_rok):.0f}** "
                 f"(zwykle ${p * (1 + r.potencjal_od):.0f}–${p * (1 + r.potencjal_do):.0f})")
    if isinstance(r.get("dlaczego"), str):
        line += f"\n   💬 {r.dlaczego}"
    return line


def _section(title: str, df: pd.DataFrame, rarity: dict) -> list[str]:
    return [title, *[_card_line(i, r, rarity) for i, (_, r) in enumerate(df.iterrows(), 1)], ""]


def build() -> str:
    cards, cheap, box = _read("ranking.csv"), _read("ranking_tanie.csv"), _read("sealed_ranking.csv")
    rarity = {}
    if (CATALOG / "cards.csv").exists():
        c = pd.read_csv(CATALOG / "cards.csv")
        rarity = dict(zip(c.product_id, c.rarity))
    m = json.loads((REPORTS / "market.json").read_text()) if (REPORTS / "market.json").exists() else {}

    out = [f"🃏 **PokeScout – tydzień {m.get('date', '')}**", ""]
    if m:
        t, p = m["trend_90"], m["pct_90"]
        verdict = ("🟢 rynek tanieje lub stoi – historycznie dobry moment na zakupy" if p < 0.35 else
                   "🔴 rynek mocno rośnie – historycznie potem słabiej, nie spiesz się" if p > 0.75 else
                   "🟡 rynek w normie")
        out += [f"**Rynek:** {verdict} (ostatnie 3 mies.: {t:+.1%}/mies.)", ""]
    if len(cards):
        out += _section("🔥 **Karty na lata – top 8** (od $50)", cards.head(8), rarity)
    gems = cheap[cheap.price_now >= 15] if len(cheap) else cheap
    if len(gems):
        out += _section("💎 **Tańsze perełki – top 3** ($15–50)", gems.head(3), rarity)
    if len(box):
        out += ["📦 **Boxy i ETB – top 3**"]
        for i, (_, r) in enumerate(box.head(3).iterrows(), 1):
            eur = f" (Cardmarket ok. €{r.cardmarket_eur:.0f})" if pd.notna(r.get("cardmarket_eur")) else ""
            warn = " ⚠️ dodruk" if r.get("dodruk_posty", 0) >= 3 else ""
            out.append(f"{i}. **[{r['name']}](https://www.tcgplayer.com/product/{r.product_id})** · "
                       f"${r.price_now:.0f}{eur} · [Cardmarket]({_cm_link(r['name'])}){warn}")
        out += [""]
    out += ["📈 = prognoza na rok dla tej karty: jak w latach 2025–26 rosły karty podobnie ocenione i o podobnych cechach, "
            "i do jakiej ceny by doszła (mocny rynek – w słabszym roku mniej; dłużej niż rok nie da się jeszcze sprawdzić). "
            "💬 = dlaczego karta jest wysoko.",
            "Kupuj kilka pozycji, nie jedną. ⚠️ dodruk = dużo postów o dodruku setu.",
            f"Pełne listy: {REPO_URL}/ranking.csv · {REPO_URL}/sealed_ranking.csv"]
    return "\n".join(out)


def send(text: str, url: str) -> None:
    chunks, cur = [], ""
    for line in text.splitlines():  # limit Discorda: 2000 znaków na wiadomość
        if len(cur) + len(line) + 1 > 1900:
            chunks.append(cur)
            cur = ""
        cur += line + "\n"
    chunks.append(cur)
    for c in chunks:
        r = requests.post(url, json={"content": c, "flags": 4}, timeout=30)  # 4 = bez podglądu linków
        r.raise_for_status()
        time.sleep(1)


def main() -> int:
    text = build()
    (REPORTS / "raport.md").write_text(text + "\n")
    print(text)
    url = os.getenv("DISCORD_WEBHOOK")
    if not url:
        print("Brak DISCORD_WEBHOOK – zapisano tylko reports/raport.md")
        return 0
    send(text, url)
    print("Wysłano na Discord")
    return 0


if __name__ == "__main__":
    sys.exit(main())
