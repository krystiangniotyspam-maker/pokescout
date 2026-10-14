# PokeScout – algorytm szukania kart w dołku i niedoszacowanych

Wersja 0.1 · październik 2026

## 1. Co wynika z historii rynku (research)

| Obserwacja | Przykład | Wniosek dla algorytmu |
|---|---|---|
| Po premierze ceny spadają, dno zwykłych setów przychodzi zwykle **6–9 miesięcy** po premierze, po kolejnych falach dodruku | wskazówki PokeInsider; ceny przedsprzedażowe spadają o 40–90% w 1–2 miesiące | Nie kupować przed ok. 9. miesiącem, pomijać pierwsze tygodnie przy liczeniu szczytu |
| Najlepsze karty długoterminowo: **kultowy Pokémon + najrzadsza wersja + świetna grafika + set, który znika z rynku** | Umbreon VMAX alt art: ok. $250–400 na premierze, dołek $200–300 na początku 2022, ok. $500 pod koniec 2022, $800–1200 w 2023–24, ok. $1800–2400 w 2026 | Popularność × rzadkość to najważniejszy składnik jakości |
| Wzrost potrafi przyjść **2–3 lata po premierze**, po długim płaskim dnie | Magikarp IR (Paldea Evolved, 06.2023): dołek ok. $267 w lutym 2026, ok. $430 w lipcu 2026 | Szukamy dna, które się **utrzymuje**, nie pierwszego spadku |
| **Set specjalny z ogromnym nakładem**: zamknięte produkty rosną, a pojedyncze karty dalej tanieją | Celebrations (2021): indeks kart ok. −64% od szczytu, a paczki z $4,30 do ok. $40; klasyczne karty (Charizard 4/102) trzymały się lepiej | Pułapka: głęboki spadek ≠ okazja. Wymagamy potwierdzonego dna, a sygnał „sealed rośnie” w setach specjalnych liczy się słabiej |
| Zamknięte produkty historycznie rosną stabilniej niż pojedyncze karty | TCGinvest: 97% ze 154 boxów powyżej ceny wejścia | Wzrost cen sealed z danego setu = sygnał, że nowa podaż wysycha |
| **Październik 2026**: korekta nowoczesnych kart, karty z 30th Celebration −20–30% w miesiąc, vintage stabilne | artykuł CardCenteringTool | Dla 30th Celebration okno zakupowe raczej za 9–15 miesięcy |

Źródła: [PokemonPriceTracker – Moonbreon](https://www.pokemonpricetracker.com/blog/posts/moonbreon-price-history-is-umbreon-vmax-still-rising), [TCGIndex – Magikarp 203](https://tcgindex.io/pokemon/card/pokemon-sv02-paldea-evolved-magikarp-203-193-illustration-rare), [Bad Moon Rising – Celebrations vs 30th](https://www.badmoonrising.com/news/pokemon-celebrations-25th-vs-30th-celebration), [TCGinvest – overprinting](https://tcginvest.io/blog/does-overprinting-kill-pokemon-card-value), [PokeInsider – timing](https://pokeinsider.com/2025/11/05/when-to-buy-pokemon-cards-a-collectors-guide-to-timing-the-market/), [CardCenteringTool – październik 2026](https://blog.cardcenteringtool.com/pokemon-card-prices-dropping-october-2026-what-collectors-must-know/).
Część liczb pochodzi z blogów sprzedawców – traktuj je jako orientacyjne.

## 2. Algorytm

### Moduł A – „dołek po premierze”

**Bramki** (karta musi przejść wszystkie, inaczej ocena = 0 i lista powodów):

| Bramka | Domyślnie |
|---|---|
| Rzadkość | Illustration Rare i wyżej (waga ≥ 0,75) |
| Popularność Pokémona | tier 1 lub 2 (`tiers.py`) |
| Karta promo | odrzucona (duży nakład) |
| Wiek setu | zwykły set 9–48 mies., set specjalny 15–48 mies. |
| Spadek od szczytu po premierze | ≥ 35% |
| Trend 60 dni | nie gorszy niż −3%/mies. |
| **Potwierdzone dno** | minimum z 180 dni ≥ 6 tygodni temu **i** cena ≥ 5% nad nim |
| Cena | ≥ 8 € (płynność, wysyłka) |
| Zapowiedziany dodruk | odrzuca |

**Ocena 0–100** (wagi w `Config`):

| Składnik | Waga | Jak liczony |
|---|---|---|
| Jakość | 25% | 0,6 × popularność Pokémona + 0,4 × rzadkość |
| Głębokość dołka | 20% | max przy 75–85% pod szczytem; >85% lekko karane (ryzyko trwałego załamania) |
| Stabilizacja | 20% | trend 60 dni + „zwrot” (trend 30 dni > trend 90 dni) + jak długo cena trzyma się nad dnem |
| Podaż | 15% | wiek setu w „słodkim punkcie” (12–30 mies., specjalne 18–36) + zamknięte produkty drożeją szybciej niż karta |
| Uspokojenie | 10% | zmienność 60 dni / 180 dni < 1 |
| Szum w sieci | 10% | 0–1 z analizy forów/YouTube; na razie 0,5 (neutralnie) |

### Moduł B – niedoszacowane i okazje

- **B1 wartość względna**: grupa podobnych kart (tier × rzadkość × epoka 2-letnia). Karta z ceną ≥ 1 odchylenie (robust z-score, mediana/MAD) poniżej grupy i bez spadającego trendu.
- **B2 para kart**: proporcja cen dwóch kart, które zwykle chodzą razem (np. Espeon i Umbreon z tego samego setu). Sygnał, gdy obecna proporcja jest ≥ 25% niższa niż typowa z ostatniego roku.
- **B3 sprawdzenie oferty**: cena oferty / cena trend. ≤ 75% → okazja, < 40% albo ≥ 2 czerwone flagi (mało opinii, brak zdjęcia rewersu, jedno zdjęcie) → podejrzane.

### Test na historii (`backtest.py`)

Co miesiąc: ocena tylko z danych do tej daty → top N → zwrot po 24 miesiącach → porównanie z bazą (wszystkie karty IR+ tier ≤ 2 dostępne w tym momencie). Algorytm ma sens tylko, jeśli **wyraźnie bije bazę** na prawdziwych danych.

## 3. Co pokazało demo (dane syntetyczne)

Demo (`python demo.py`) używa wymyślonych przebiegów cen, żeby sprawdzić mechanikę. Wyniki **nie są dowodem skuteczności**, ale wyłapały ważny błąd:

| Wersja | Mediana zwrotu wyborów (24 mies.) | Baza | Wybory ≥2x |
|---|---|---|---|
| bez reguły „potwierdzonego dna” | −14% | +6% | 24% |
| z regułą „potwierdzonego dna” | +41% | +6% | 28% |

Bez tej reguły algorytm wybierał głównie karty z powoli tanieącego setu specjalnego – dokładnie pułapkę Celebrations.

## 4. Dane

Format wejściowy jest niezależny od źródła (`data.py`): `prices.csv` (card_id, date, price), `cards.csv` (card_id, name, set_id, rarity, release_date, set_type, reprint_announced, buzz), `sealed.csv` (set_id, date, price).

| Źródło | Uwagi |
|---|---|
| pokemontcg.io (darmowe) | Katalog + ceny TCGplayer aktualne. **Ceny Cardmarketu w API nieaktualizowane od 11.2025** (sprawdzone na Magikarp 203) – dla Europy nie polegać |
| PokemonPriceTracker (100 zapytań/dzień za darmo) | Historia dzienna Cardmarket/TCGplayer/eBay – do sprawdzenia głębokość historii |
| PriceCharting (płatne) | Długa historia, karty z oceną |
| Własne zrzuty | Od dziś codziennie zapisywać ceny – każdy dzień to dzień historii więcej |

## 5. Uruchomienie

```bash
pip install pandas numpy
python demo.py                                   # demo na danych syntetycznych
python run.py --prices prices.csv --cards cards.csv --sealed sealed.csv --as-of 2026-10-14
```

## 6. Następne kroki

1. Pobrać prawdziwą historię dla ok. 300–500 kart IR/SIR/alt art z setów 2020–2024 i uruchomić `backtest.py`.
2. Skalibrować progi i wagi na tych danych (uwaga na przeuczenie – mało „zwycięzców”, testować na latach, których nie użyto do kalibracji).
3. Skalibrować listę popularności Pokémonów danymi (mediana cen kart danego Pokémona).
4. Dodać `buzz` z Reddita/YouTube (Gemini API) – najpierw sprawdzić w teście, czy w ogóle poprawia wyniki.
5. Codzienny przebieg (GitHub Actions) + raport na Discord.

## 7. Automat w chmurze (GitHub Actions)

Workflow `.github/workflows/daily.yml` codziennie ok. 7:17:
1. `scripts/collect_prices.py` – zrzut cen kart IR/SIR/secret itd. z setów od 2019 r. (pokemontcg.io) do `data/prices/RRRR/MM/DD.csv`,
2. commit danych do repo (historia rośnie z każdym dniem),
3. `scripts/report.py --send` – ranking i wysyłka na Discord.

Sekrety (Settings → Secrets and variables → Actions):
- `DISCORD_WEBHOOK_RAPORT` – adres webhooka kanału z raportem,
- `POKEMONTCG_API_KEY` – opcjonalnie (bez klucza też działa).

Ręczne uruchomienie: zakładka **Actions → Codzienne ceny i raport → Run workflow**.
Oceny ruszą po ok. 8 tygodniach zbierania (albo wcześniej po wczytaniu historii z PokemonPriceTracker).
