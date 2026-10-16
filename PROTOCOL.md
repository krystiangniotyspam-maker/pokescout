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

- **Backtest:** `date` to etykieta niedzieli kończącej tygodniowy koszyk, co 2 tygodnie. Mediana tygodnia
  zawiera tylko obserwacje rzeczywiście dostępne do chwili liczenia danych (ostatni tydzień bywa niepełny).
- **Live:** pole `date` w historycznym formacie CSV **nie jest dniem decyzji** — jest etykietą koszyka
  `week_bucket_end` (niedziela, która może jeszcze nie nadejść). Faktyczny dzień decyzji to
  `decision_at` w UTC, obliczony z `run_at`; `observed_at` to dzień ostatnich plików cen.
  Weryfikujemy `observed_at <= decision_at <= data UTC z run_at`. Nigdy nie przedstawiamy
  `week_bucket_end` jako rzeczywistej daty rekomendacji.
- Historyczne rekordy zapisane **przed PR B.1** nie mają wiarygodnego `decision_at`; nie przypisujemy
  im go wstecz na podstawie przyszłej niedzieli.

## 3. Cechy i model

- Cechy liczone wyłącznie z danych do dnia decyzji (`pokescout/features.py`, `build_panel`).
- Uczenie walk-forward: w dniu `d` model zna tylko wiersze z `date + horyzont ≤ d` (`walk_forward`).
- Wersja modelu = `model_sha` (skrót kodu cech, modelu, rankingu oraz listy cech).
- Pochodzenie danych = `data_snapshot_hash` (SHA-256 nad ścieżkami i dokładnymi bajtami plików
  wejściowych w `data/prices`, `data/catalog`, `data/buzz`, `data/cardmarket`; czytane strumieniowo).
  `code_commit_sha` wskazuje commit kodu, `run_id` jedno uruchomienie, a `market`/`variant`/
  `instrument_id` identyfikują kartę. `variant=unverified` to uczciwy brak rozpoznania wariantu,
  nie zapewnienie o poprawności mapowania.
- Sam SHA-256 **nie archiwizuje** snapshotu; odtworzenie wymaga zachowania źródłowych plików o tym hashu
  (w historii Git lub osobnym niezmiennym magazynie). Na razie jest to fingerprint i kontrola zmian.

## 4. Wynik

- Zwrot: `log(cena po h mies. / cena w dniu decyzji)`, h = 3, 6, 12 mies.; cena po h = ostatnie notowanie
  nie starsze niż 21 dni przed końcem horyzontu.
- Zwrot ponad rynek: minus mediana próby z punktu 1 w tej dacie.
- Zwrot netto: obecnie koszty sprzedawcy w USA (13% + $1,5 w każdą stronę). **Docelowo koszty EU/PL**
  (prowizja Cardmarket, wysyłka, VAT i cło przy zakupie z USA, kurs) – plan C w Issue #13.
- **Stan obecny (do PR E):** `evaluate_scores` oraz `sealed.evaluate` filtrują brakujące ceny
  końcowe przed Top-K. Dla kart chase od $20 test nie wykazał braków; dla sealed braki występują.
  **Plan PR E:** Top-K wybierać przed rozliczeniem, raportować odsetek braków; brak ceny nie oznacza −100%.

## 5. Porównania (baseline)

**Stan obecny:** porównujemy medianę rynku i prostą ocenę C (stałe rangi czterech cech, bez uczenia).
**Plan PR C/E:** dodać losowy wybór tej samej liczby kart oraz koszt wykonania transakcji EU/PL.

## 6. Ocena na żywo

- `reports/picks_log.csv` jest logicznie **tylko dopisywany** (istniejące wiersze zachowują treść;
  przy zmianie schematu CSV dochodzą nowe puste kolumny w rekordach historycznych). Powtórny przebieg
  z tą samą etykietą tygodniową, `model_sha` i `data_snapshot_hash` jest pomijany.
  **Zmiana choćby samych danych przy tym samym kodzie dopisuje nową rewizję**, z własnym `run_at`
  i `run_id`. Dla oceny na żywo liczy się tylko najwcześniejszy zapis tygodnia
  (w `first_runs`; dawne wiersze bez `run_at` są traktowane jako pierwotne).
- Dane głównego rankingu są z TCGplayer USD; wariant karty nie jest jeszcze rzetelnie zmapowany.
- W przyszłości osobne etykiety `primary/revision` można dodać dla czytelności; obecnie wynika to
  z `first_runs`. Sama obserwacja `date` nadal oznacza koszyk, nie datę zakupu/wykonania.

## 7. Co wolno pokazywać w raporcie

- Pozycję karty w rankingu i opis historii z wyraźnym oznaczeniem „historia, nie prognoza”.
- Nie pokazujemy jako prognozy liczb, które nie przeszły testu poza próbą (point-in-time, out-of-sample).
- Wyniki retrospektywne (model uczony na danych późniejszych niż decyzja) opisujemy jako retrospektywne
  i nie używamy ich jako dowodu przewagi strategii.

## 8. Kryteria jakości zmian

Point-in-time, out-of-sample, wykonalność (koszty i płynność w EU/PL), odtwarzalność (skrypt i dane w repo).
Przy sporze: hipoteza, test falsyfikujący, wynik, koszt alternatyw; niepewność zaznaczamy zamiast ogłaszać zwycięzcę.
