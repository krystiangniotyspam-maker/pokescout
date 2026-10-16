# Rejestr eksperymentów

Każdy wariant sprawdzany na historii, z datą i wynikiem – także odrzucone. Liczby: karty chase od $20, top 20,
walk-forward, chyba że napisano inaczej. Szczegóły i skrypty: [Issue #13](https://github.com/krystiangniotyspam-maker/pokescout/issues/13).

| Data | Eksperyment | Wynik | Decyzja |
|---|---|---|---|
| 2026-10 | Ranking główny: szansa na +50% + model zwrotu 6 mies. (wybierany spośród kilku wariantów na tej samej historii 2024–26) | 6 mies.: IC +0,25, top20 +7,9% ponad rynek (90% bootstrap: +1,0% … +15,4%); 1. połowa dat +14,2%, 2. połowa +2,4%. 12 mies.: 14 dat, ok. 0,5 niezależnego okresu – niewalidowalne | w użyciu; wynik obciążony wyborem wariantu na tej samej historii |
| 2026-10 | Tabela potencjału z całej historii vs test poza próbą (tabela z dat < 2025-07-27) | mediany górnych przedziałów zawyżone o 8–21 p.p.; przedział p25–p75 obejmował 59–73% wyników | raport pokazuje historię, nie prognozę |
| 2026-10 | `szansa_50` jako prawdopodobieństwo | najwyższy kwintyl: przewidywane 68%, faktycznie 23% (gorzej niż 4. kwintyl) | usunięte z list publicznych |
| 2026-10 | Korekta potencjału karty modelem rocznym (uczony na całym panelu) | bez walk-forward, niezwalidowane | usunięte |
| 2026-10 | Ablacja cech z Reddita | bez `buzz_eng`: 12 mies. top20 +25,0% (z nią +25,9%); bez całego Reddita +24,2% | `buzz_eng` do usunięcia (point-in-time) |
| 2026-10 | Kolejność selekcji top-K i `dropna` | braki ceny końcowej 0,00% (karty); sealed 2,2–2,9% | zabezpieczenie w kodzie, bez wpływu na karty |
| 2026-10 | PriceCharting 2020–24, spokojny rynek, walk-forward (decyzje 2022-08 – 2023-11) | top20 +45% w 12 mies. vs rynek +6%; 24 mies. tylko 4 daty | point-in-time; obciążenie: nazwy kart z dzisiejszych list top 150 setu |
| 2026-10 | PriceCharting, zakupy 2021, model uczony na 2023 | +9% vs −8% (12 mies.) | **wycofane: look-ahead** (przy 24/36 mies. okno wyniku nakłada się na etykiety treningowe) |
| 2026-10 | PriceCharting, zakupy 2021, prosta ocena C bez uczenia | top 5% od $50: −17,0% vs rynek −16,9% (12 mies.), −11,9% vs −9,8% (36 mies.) | brak dowodu przewagi rankingu w krachu |
