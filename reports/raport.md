# PokeScout — raport wstrzymany do ponownego przeliczenia

**Status: 16 października 2026 r.** Ten plik zawierał wcześniej niesprawdzone prognozy wzrostów cen kart oraz scenariusz „słabego rynku” oparty na historycznym teście z wykorzystaniem danych z przyszłości względem daty zakupu. Te wyniki zostały **wycofane** po [audycie metodologii (Issue #13)](https://github.com/krystiangniotyspam-maker/pokescout/issues/13).

Zmiany generatora wdrożone w [PR #16](https://github.com/krystiangniotyspam-maker/pokescout/pull/16) nie przeliczyły automatycznie opublikowanych artefaktów, dlatego nie udostępniamy starego raportu jako aktualnego rankingu ani rekomendacji. **Raport zostanie odtworzony dopiero podczas kolejnego prawidłowego przebiegu pipeline** z nowym formatem: pozycje w rankingu, jawne ograniczenia danych i historia wyraźnie oddzielona od prognoz.

Pliki `reports/ranking.csv` i `reports/ranking_tanie.csv` zostały w ramach poprawki A.1 oczyszczone z wycofanych pól prognoz; same pozycje są historycznym stanem danych i nie stanowią porady inwestycyjnej. `reports/picks_log.csv` pozostaje bez zmian, ponieważ jest archiwum decyzji i nie wolno go przepisywać wstecz.

**Ograniczenia:** ceny TCGplayer w USD nie uwzględniają realnych cen wykonania, płynności i kosztów transakcyjnych na rynku europejskim (np. Cardmarket w Polsce). Wyników z krótkiej i nakładającej się próby 12-miesięcznej nie należy traktować jako zwalidowanej przewagi strategii.
