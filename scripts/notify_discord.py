"""Raport na Discord: pełny raz w miesiącu, a w pozostałe tygodnie tylko alerty o ważnych zmianach.

Czyta wyniki scripts/evaluate.py (ranking.csv, ranking_tanie.csv, sealed_ranking.csv, market.json).
Pełny raport zawsze zapisuje do reports/raport.md. Stan z poprzedniego tygodnia (czołówka, ceny, dodruki,
rynek) trzyma w reports/discord_state.json – z porównania z nim powstają alerty.
Adres webhooka bierze ze zmiennej DISCORD_WEBHOOK (sekret w GitHub Actions); bez niej tylko wypisuje.

    python scripts/notify_discord.py              # pierwszy tydzień miesiąca: pełny raport, potem alerty
    python scripts/notify_discord.py --full       # pełny raport od razu
"""
from __future__ import annotations

import argparse
import datetime as dt
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
STATE = REPORTS / "discord_state.json"
TOP_N = 8
PRICE_DROP = 0.15  # spadek ceny karty z czołówki, przy którym wysyłamy alert „okazja”
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


def _verdict(m: dict) -> str:
    p = m["pct_90"]
    return ("🟢 rynek tanieje lub stoi – historycznie dobry moment na zakupy" if p < 0.35 else
            "🔴 rynek mocno rośnie – historycznie potem słabiej, nie spiesz się" if p > 0.75 else
            "🟡 rynek w normie")


def _market() -> dict:
    return json.loads((REPORTS / "market.json").read_text()) if (REPORTS / "market.json").exists() else {}


def _rarity() -> dict:
    if not (CATALOG / "cards.csv").exists():
        return {}
    c = pd.read_csv(CATALOG / "cards.csv")
    return dict(zip(c.product_id, c.rarity))


def state_now() -> dict:
    cards, m = _read("ranking.csv"), _market()
    top = cards.head(TOP_N)
    return {"date": m.get("date", ""), "verdict": _verdict(m)[:1] if m else "",
            "top": [int(c) for c in top.card_id],
            "prices": {str(int(r.card_id)): float(r.price_now) for _, r in top.iterrows()},
            "dodruk": sorted({_set(r.set_name) for _, r in cards.head(50).iterrows() if r.get("dodruk_posty", 0) >= 3})}


def alerts(prev: dict) -> str:
    """Krótka wiadomość o ważnych zmianach od poprzedniego tygodnia; pusta, gdy nic ważnego."""
    cards, m, rarity = _read("ranking.csv"), _market(), _rarity()
    if not prev or cards.empty:
        return ""
    out = []
    cur = cards.set_index("card_id")
    new = [c for c in cards.card_id.head(3) if c not in prev.get("top", [])]
    if new:
        lines = []
        for i, c in enumerate(new, 1):
            r = cur.loc[c].copy()
            r["card_id"] = c
            lines.append(_card_line(i, r, rarity))
        out.append("🆕 **Nowe karty w czołówce:**\n" + "\n".join(lines))
    drops = []
    for c, old in prev.get("prices", {}).items():
        c = int(c)
        if c in cur.index and cur.loc[c, "price_now"] <= old * (1 - PRICE_DROP):
            r = cur.loc[c].copy()
            r["card_id"] = c
            head, _, rest = _card_line(len(drops) + 1, r, rarity).partition("\n")
            drops.append(f"{head} · **−{1 - r.price_now / old:.0%}** (było ${old:.0f})\n{rest}".rstrip())
    if drops:
        out.append("📉 **Okazja – karty z czołówki wyraźnie potaniały:**\n" + "\n".join(drops))
    now_dodruk = {_set(r.set_name) for _, r in cards.head(50).iterrows() if r.get("dodruk_posty", 0) >= 3}
    for s_ in sorted(now_dodruk - set(prev.get("dodruk", []))):
        out.append(f"⚠️ **Dużo postów o dodruku setu {s_}** – z kupnem kart z tego setu lepiej poczekać.")
    if m and prev.get("verdict") and _verdict(m)[:1] != prev["verdict"]:
        out.append(f"🔄 **Zmiana na rynku:** {_verdict(m)}")
    if not out:
        return ""
    return "\n\n".join([f"🔔 **PokeScout – alert {m.get('date', '')}**", *out,
                         "Pełny raport przyjdzie w pierwszy poniedziałek miesiąca."])


def build() -> str:
    cards, cheap, box = _read("ranking.csv"), _read("ranking_tanie.csv"), _read("sealed_ranking.csv")
    rarity, m = _rarity(), _market()

    out = [f"🃏 **PokeScout – raport miesiąca ({m.get('date', '')})**", ""]
    if m:
        out += [f"**Rynek:** {_verdict(m)} (ostatnie 3 mies.: {m['trend_90']:+.1%}/mies.)", ""]
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="pełny raport niezależnie od daty")
    a = ap.parse_args()
    report = build()
    (REPORTS / "raport.md").write_text(report + "\n")
    prev = json.loads(STATE.read_text()) if STATE.exists() else {}
    full = a.full or dt.date.today().day <= 7  # pierwszy poniedziałek miesiąca
    text = report if full else alerts(prev)
    STATE.write_text(json.dumps(state_now(), ensure_ascii=False, indent=1) + "\n")
    if not text:
        print("Brak ważnych zmian – bez wiadomości na Discord")
        return 0
    print(text)
    url = os.getenv("DISCORD_WEBHOOK")
    if not url:
        print("Brak DISCORD_WEBHOOK – nic nie wysłano")
        return 0
    send(text, url)
    print("Wysłano na Discord")
    return 0


if __name__ == "__main__":
    sys.exit(main())
