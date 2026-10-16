# Protokół testów PokeScout

Ustalony w [Issue #13](https://github.com/krystiangniotyspam-maker/pokescout/issues/13). Zmiana tego pliku wymaga
PR z uzasadnieniem i przeglądem drugiego modelu. Każdy nowy wariant testowany na historii trafia do
[docs/experiments.md](docs/experiments.md), także gdy wypadł źle.

## 1. Próba (universe)

- Karty z katalogu `data/catalog/cards.csv` (TCGplayer, karty po angielsku), bez setów promo.
- **Do oceny strategii tylko rzadkości „chase”** (`pokescout/tcgcsv.py: CHASE_RARITIES`). Pozostałe karty są
  w katalogu, bo dziś kosztują $10+, więc ich wyniki znają przyszłość. Do bieżącego rankingu trafiają normalnie.
- Karta jest w próbie w dniu decyzji, gdy miała notowanie w ciągu 21 dni przed nią i co najmniej 8 tygodni historii.
- Progi cenowe w dniu decyzji: główny ranking od $50, lista tańsza $5–50, wyniki „inwestycyjne” od $20.

## 2. Daty

- Dzień decyzji = niedziela kończąca tydzień (`date` w panelu), co 2 tygodnie. Mediana tygodnia zawiera tylko dane
  do tej niedzieli włącznie.
- W logu na żywo zapisujemy też `observed_at` (dzień najnowszych cen) i `run_at` (czas przebiegu, UTC).
  `observed_at` nigdy nie może być późniejsze od najnowszego pliku cen ani od `run_at` (test w `tests/`).

## 3. Cechy i model

- Cechy liczone wyłącznie z danych do dnia decyzji (`pokescout/features.py`, `build_panel`).
- Uczenie walk-forward: w dniu `d` model zna tylko wiersze z `date + horyzont ≤ d` (`walk_forward`).
- Wersja modelu = `model_sha` (skrót kodu cech, modelu i rankingu oraz listy cech; `scripts/evaluate.py: model_sha`).

## 4. Wynik

- Zwrot: `log(cena po h mies. / cena w dniu decyzji)`, h = 3, 6, 12 mies.; cena po h = ostatnie notowanie
  nie starsze niż 21 dni przed końcem horyzontu.
- Zwrot ponad rynek: minus mediana próby z punktu 1 w tej dacie.
- Zwrot netto: obecnie koszty sprzedawcy w USA (13% + $1,5 w każdą stronę). **Docelowo koszty EU/PL**
  (prowizja Cardmarket, wysyłka, VAT i cło przy zakupie z USA, kurs) – plan C w Issue #13.
- Braki ceny końcowej: top-K wybieramy przed rozliczeniem; raportujemy odsetek braków. Brak nie oznacza −100%
  (karta fizycznie istnieje); wariant ostrożny = ostatnia znana cena.

## 5. Porównania (baseline)

Każdy wynik strategii podajemy obok: mediany rynku (cała próba), prostej oceny C (stałe rangi czterech cech,
bez uczenia) i losowego wyboru tej samej liczby kart.

## 6. Ocena na żywo

- `reports/picks_log.csv` jest **tylko dopisywany**. Ponowny przebieg tej samej daty tym samym modelem niczego
  nie zmienia, innym modelem dopisuje się obok.
- Liczy się **pierwszy** zapis dla danej daty (`first_runs`). To jedyna miara, której nie da się dopasować
  do historii; po 3 i 6 mies. rozliczamy ją w `reports/evaluation.md`.

## 7. Co wolno pokazywać w raporcie

- Pozycję karty w rankingu i opis historii z wyraźnym oznaczeniem „historia, nie prognoza”.
- Nie pokazujemy jako prognozy liczb, które nie przeszły testu poza próbą (point-in-time, out-of-sample).
- Wyniki retrospektywne (model uczony na danych późniejszych niż decyzja) opisujemy jako retrospektywne
  i nie używamy ich jako dowodu przewagi strategii.

## 8. Kryteria jakości zmian

Point-in-time, out-of-sample, wykonalność (koszty i płynność w EU/PL), odtwarzalność (skrypt i dane w repo).
Przy sporze: hipoteza, test falsyfikujący, wynik, koszt alternatyw; niepewność zaznaczamy zamiast ogłaszać zwycięzcę.
