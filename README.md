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

Źródło: **[tcgcsv.com](https://tcgcsv.com)** – codzienne kopie cen TCGplayer, bez klucza API,
ok. 2 zapytania na set (kilka minut na cały przebieg). Daje też ceny **zamkniętych produktów**
(booster box, bundle, ETB), więc sygnał „sealed drożeje” działa na prawdziwych danych,
oraz (gdy jest dostępne) **archiwum dziennych cen od 08.02.2024**. W 10.2026 autor tcgcsv tymczasowo
wyłączył archiwum, więc historia rośnie na razie tylko z codziennych zrzutów (`scripts/backfill_history.py`
czeka na jego powrót).

| Plik | Zawartość |
|---|---|
| `data/catalog/sets.csv` | sety od 2019 r.: group_id, nazwa, premiera, typ (main/special/promo) |
| `data/catalog/cards.csv` | śledzone karty (rzadkość IR/SIR/Ultra/Secret/Hyper… albo cena ≥ $10); ręczne kolumny `reprint_announced`, `buzz` są zachowywane |
| `data/catalog/sealed.csv` | zamknięte produkty setu |
| `data/prices/RRRR/MM/DD.csv.gz` | ceny z dnia: product_id, sub_type, market, low, mid (USD) |

Uwaga: dla setów sprzed 02.2024 „szczyt po premierze” to tylko maksimum od początku danych
(cecha `history_complete` mówi modelowi, kiedy tak jest). Ceny Cardmarketu nie są dostępne;
pokemontcg.io (poprzednie źródło) często nie odpowiadało i miało nieaktualne ceny Cardmarketu.

## 5. Uruchomienie

```bash
pip install -r requirements.txt
python demo.py                          # demo na danych syntetycznych
python scripts/collect_prices.py        # dzisiejsze ceny + katalog
python scripts/backfill_history.py --start 2024-02-08 --every 7   # historia z archiwum
python scripts/evaluate.py              # test przewidywań → reports/evaluation.md, reports/ranking.csv
```

## 6. Test przewidywań (`scripts/evaluate.py`)

Co 2 tygodnie (data decyzji) liczymy cechy każdej karty **tylko z danych do tej daty** i sprawdzamy
zwrot po 3, 6 i 12 miesiącach **ponad medianę rynku** (żeby oceniać wybór kart, a nie to, czy cały rynek rósł).

Porównujemy:
- obecne reguły (moduł A bez bramek, moduł B1),
- każdą cechę osobno (który sygnał w ogóle coś przewiduje),
- **model uczony walk-forward** (gradient boosting i ridge): w dniu decyzji uczy się tylko na przykładach,
  których wynik był już wtedy znany.

Miary: **IC** (korelacja rang oceny ze zwrotem, liczona w każdej dacie osobno), `ic_t_adj`
(t-stat skorygowany o nakładające się okresy), zwrot top-20 ponad rynek i odsetek trafień.

Cechy przekrojowe dodane do modelu: karta vs podobne karty (`rv_z`), popularność Pokémona z danych
(`poke_pop` – mediana cen jego innych kart IR+), trend całego setu (`set_trend_90`), karta vs set (`set_rel`).

## 7. Następne kroki

1. Pierwszy test na prawdziwej historii i decyzja, czy reguły zostają, czy zastępuje je model.
2. Kalibracja progów i wag na wynikach testu (uwaga na przeuczenie – mało lat danych).
3. `buzz` z Reddita/YouTube – dodać tylko, jeśli test pokaże poprawę.
4. Raport na Discord (na razie wyłączony w workflow).

## 8. Automat w chmurze (GitHub Actions)

- `.github/workflows/daily.yml` – codziennie 5:17 UTC: `scripts/collect_prices.py` i commit danych do repo.
- Import historii (`scripts/backfill_history.py`) – do uruchomienia, gdy archiwum tcgcsv wróci.

Zapisy do repo idą po kolei (`concurrency: data-write`), więc przebiegi nie nadpisują sobie danych.
