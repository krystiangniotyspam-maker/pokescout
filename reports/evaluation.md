# PokeScout – test przewidywań na historii

Dane: 137 dni notowań, 4777 kart w katalogu; panel 77081 obserwacji (2024-08-11 – 2026-10-18, co 2 tygodnie).

**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, 0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. `top_excess` = średni zwrot 20 najwyżej ocenionych kart ponad medianę rynku, `top_hit_rate` = jaki odsetek z nich pobił rynek, `top_net` = ich średni zwrot netto po kosztach (prowizja 13% i wysyłka $1,5 w każdą stronę) – realny zysk, nie ponad rynek.

## Horyzont 3 mies.

Daty z wynikiem: 51. Karty, które przeszły bramki modułu A: 200 obserwacji, średni zwrot ponad rynek +1.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|
| model: gradient boosting                  |      39 |  0.29  |        3.8 | +8.6%        | 66%            | -17.2%    |
| łącznie: model + ocena C                  |      39 |  0.281 |        5.7 | +12.7%       | 69%            | -16.4%    |
| ocena C: popularność + wiek + tania + dno |      51 |  0.166 |        2.8 | +13.8%       | 69%            | -14.4%    |
| cecha: age_months                         |      51 |  0.148 |        1.4 | +11.2%       | 66%            | -9.5%     |
| model: ridge na rangach                   |      39 |  0.143 |        1.8 | +11.1%       | 72%            | -12.7%    |
| cecha: range_pos_180                      |      51 |  0.141 |        3.3 | +2.2%        | 52%            | -21.4%    |
| cecha: tier_score                         |      51 |  0.133 |        2.5 | -6.7%        | 37%            | -19.7%    |
| cecha: poke_pop                           |      51 |  0.115 |        2.1 | +9.1%        | 62%            | -6.1%     |
| cecha: slope_30                           |      51 |  0.111 |        2.3 | -12.7%       | 35%            | -32.0%    |
| cecha: −drawdown                          |      51 |  0.105 |        1.7 | +2.3%        | 53%            | -20.3%    |
| cecha: buzz_eng                           |      51 |  0.1   |        1.9 | +3.9%        | 56%            | -14.3%    |
| cecha: buzz_share                         |      51 |  0.098 |        1.9 | +3.2%        | 55%            | -15.1%    |
| model: gradient boosting, cel zysk netto  |      39 |  0.097 |        1.7 | +7.3%        | 67%            | -3.9%     |
| cecha: weeks_since_low                    |      51 |  0.087 |        3.4 | +3.4%        | 54%            | -20.4%    |
| cecha: slope_60                           |      51 |  0.084 |        1.5 | -14.6%       | 32%            | -33.1%    |
| cecha: set_trend_90                       |      51 |  0.082 |        1.2 | -0.2%        | 49%            | -24.5%    |
| cecha: −rv_z                              |      51 |  0.073 |        3.9 | +4.9%        | 53%            | -30.0%    |
| reguły: moduł B1 (tania vs podobne)       |      51 |  0.073 |        3.9 | +4.9%        | 53%            | -30.0%    |
| cecha: vol_ratio                          |      51 |  0.062 |        2.8 | -1.9%        | 46%            | -24.6%    |
| cecha: slope_90                           |      51 |  0.047 |        0.9 | -13.8%       | 32%            | -32.6%    |
| cecha: above_low                          |      51 |  0.042 |        0.7 | -12.7%       | 35%            | -31.9%    |
| cecha: buzz_growth                        |      51 |  0.041 |        3   | +3.0%        | 54%            | -21.5%    |
| cecha: special                            |      51 |  0.036 |        0.9 | -9.9%        | 33%            | -29.8%    |
| reguły: moduł A (ocena bez bramek)        |      51 |  0.035 |        0.6 | +4.5%        | 53%            | -15.9%    |
| cecha: sealed_slope_90                    |      51 |  0.031 |        0.6 | -2.3%        | 45%            | -25.5%    |
| cecha: slope_180                          |      51 |  0.006 |        0.1 | -10.3%       | 35%            | -29.1%    |
| cecha: new_same_poke_90                   |      51 |  0.002 |        0.1 | +0.1%        | 51%            | -19.9%    |
| cecha: new_same_poke_365                  |      51 | -0.012 |       -0.8 | -6.3%        | 30%            | -27.1%    |
| cecha: set_rel                            |      51 | -0.033 |       -1   | +1.8%        | 51%            | -3.5%     |
| cecha: logp                               |      51 | -0.039 |       -1   | +0.1%        | 50%            | -5.1%     |
| cecha: −slope_90                          |      51 | -0.047 |       -0.9 | -15.7%       | 25%            | -41.4%    |
| cecha: rv_z                               |      51 | -0.073 |       -3.9 | +0.5%        | 51%            | -9.0%     |
| cecha: spread                             |      51 | -0.077 |       -2.7 | -3.0%        | 46%            | -37.0%    |
| cecha: drawdown                           |      51 | -0.105 |       -1.7 | -4.2%        | 41%            | -31.6%    |
| cecha: rarity_w                           |      51 | -0.108 |       -1.9 | -19.1%       | 12%            | -28.2%    |
| cecha: −range_pos_180                     |      51 | -0.141 |       -3.3 | -15.3%       | 26%            | -35.5%    |
| cecha: history_complete                   |      51 | -0.144 |       -2.2 | -18.8%       | 20%            | -38.5%    |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|
| model: gradient boosting                  |      39 | 0.386 |        4.6 | +7.4%        | 65%            | -5.7%     |
| łącznie: model + ocena C                  |      39 | 0.362 |        5.6 | +11.7%       | 66%            | -2.3%     |
| model: gradient boosting, cel zysk netto  |      39 | 0.344 |        4.5 | +6.7%        | 67%            | -3.8%     |
| ocena C: popularność + wiek + tania + dno |      51 | 0.198 |        2.5 | +7.9%        | 60%            | -3.7%     |
| reguły: moduł A (ocena bez bramek)        |      51 | 0.096 |        1.4 | +4.8%        | 53%            | -4.6%     |
| reguły: moduł B1 (tania vs podobne)       |      51 | 0.013 |        0.5 | +2.5%        | 49%            | -8.7%     |

Stabilność (3 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |
|:-----------------------|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |      13 |  0.311 |        3.2 | +22.0%       | 75%            | -13.5%    |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      25 |  0.242 |        3   | +23.2%       | 81%            | -7.6%     |
| 1. połowa (od 2024-08) | model: gradient boosting                  |      13 |  0.151 |        0.9 | -1.0%        | 46%            | -30.8%    |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      25 |  0.113 |        1.1 | -5.6%        | 44%            | -28.5%    |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      25 |  0.088 |        4.9 | +9.2%        | 60%            | -28.8%    |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      25 |  0.085 |        1.9 | +1.3%        | 48%            | -23.4%    |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      25 |  0.079 |        0.8 | +7.9%        | 59%            | -11.4%    |
| 2. połowa (od 2025-07) | model: gradient boosting                  |      26 |  0.359 |        8   | +13.8%       | 75%            | -10.4%    |
| 2. połowa (od 2025-07) | łącznie: model + ocena C                  |      26 |  0.266 |        4.8 | +8.4%        | 66%            | -17.8%    |
| 2. połowa (od 2025-07) | cecha: −drawdown                          |      26 |  0.096 |        1.4 | +10.4%       | 62%            | -12.5%    |
| 2. połowa (od 2025-07) | ocena C: popularność + wiek + tania + dno |      26 |  0.093 |        1.3 | +5.5%        | 56%            | -21.0%    |
| 2. połowa (od 2025-07) | cecha: weeks_since_low                    |      26 |  0.089 |        3.7 | +5.5%        | 60%            | -17.5%    |
| 2. połowa (od 2025-07) | reguły: moduł B1 (tania vs podobne)       |      26 |  0.058 |        1.9 | +1.0%        | 46%            | -31.2%    |
| 2. połowa (od 2025-07) | reguły: moduł A (ocena bez bramek)        |      26 | -0.008 |       -0.1 | +1.3%        | 48%            | -20.2%    |

## Horyzont 6 mies.

Daty z wynikiem: 45. Karty, które przeszły bramki modułu A: 133 obserwacji, średni zwrot ponad rynek -2.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|
| ocena C: popularność + wiek + tania + dno |      45 |  0.226 |        2   | +28.2%       | 74%            | +11.9%    |
| łącznie: model + ocena C                  |      27 |  0.221 |        1.7 | +16.4%       | 69%            | -3.0%     |
| model: gradient boosting                  |      27 |  0.219 |        2.4 | +11.7%       | 64%            | -7.3%     |
| cecha: tier_score                         |      45 |  0.189 |        2.2 | -11.4%       | 37%            | -13.5%    |
| cecha: poke_pop                           |      45 |  0.177 |        1.9 | +18.1%       | 67%            | +14.2%    |
| cecha: age_months                         |      45 |  0.175 |        1   | +22.0%       | 69%            | +13.1%    |
| cecha: weeks_since_low                    |      45 |  0.147 |        3   | +1.5%        | 52%            | -10.4%    |
| cecha: buzz_eng                           |      45 |  0.137 |        1.7 | +4.5%        | 58%            | -4.2%     |
| cecha: buzz_share                         |      45 |  0.134 |        1.7 | +3.5%        | 56%            | -5.3%     |
| cecha: range_pos_180                      |      45 |  0.132 |        2.4 | -1.3%        | 50%            | -12.5%    |
| model: gradient boosting, cel zysk netto  |      27 |  0.132 |        1.2 | +8.7%        | 58%            | +6.7%     |
| cecha: −drawdown                          |      45 |  0.1   |        1.2 | -2.7%        | 48%            | -13.4%    |
| cecha: slope_180                          |      45 |  0.099 |        1.6 | -13.9%       | 39%            | -21.4%    |
| model: ridge na rangach                   |      27 |  0.096 |        0.7 | +19.8%       | 72%            | +5.9%     |
| cecha: above_low                          |      45 |  0.084 |        1   | -17.3%       | 37%            | -23.8%    |
| reguły: moduł B1 (tania vs podobne)       |      45 |  0.077 |        4   | +7.8%        | 53%            | -17.3%    |
| cecha: −rv_z                              |      45 |  0.077 |        4   | +7.8%        | 53%            | -17.3%    |
| cecha: special                            |      45 |  0.07  |        1   | -10.1%       | 41%            | -17.7%    |
| cecha: slope_30                           |      45 |  0.062 |        0.9 | -19.3%       | 33%            | -27.1%    |
| cecha: set_trend_90                       |      45 |  0.051 |        0.5 | -1.3%        | 47%            | -16.5%    |
| cecha: slope_60                           |      45 |  0.047 |        0.7 | -21.6%       | 32%            | -28.5%    |
| cecha: vol_ratio                          |      45 |  0.047 |        1.1 | -1.2%        | 46%            | -13.5%    |
| cecha: slope_90                           |      45 |  0.044 |        0.7 | -19.8%       | 32%            | -26.1%    |
| reguły: moduł A (ocena bez bramek)        |      45 |  0.039 |        0.5 | +7.8%        | 58%            | -2.0%     |
| cecha: buzz_growth                        |      45 |  0.027 |        1.1 | +3.7%        | 53%            | -9.2%     |
| cecha: sealed_slope_90                    |      45 | -0.02  |       -0.2 | -5.2%        | 39%            | -18.5%    |
| cecha: new_same_poke_90                   |      45 | -0.023 |       -0.8 | -5.3%        | 43%            | -15.1%    |
| cecha: set_rel                            |      45 | -0.025 |       -0.6 | +1.6%        | 50%            | +6.1%     |
| cecha: logp                               |      45 | -0.03  |       -0.4 | -0.2%        | 47%            | +5.4%     |
| cecha: new_same_poke_365                  |      45 | -0.039 |       -2.2 | -11.8%       | 28%            | -22.2%    |
| cecha: −slope_90                          |      45 | -0.044 |       -0.7 | -22.3%       | 28%            | -35.1%    |
| cecha: spread                             |      45 | -0.058 |       -1.3 | -3.0%        | 48%            | -26.3%    |
| cecha: rv_z                               |      45 | -0.077 |       -4   | +2.1%        | 54%            | +3.8%     |
| cecha: drawdown                           |      45 | -0.1   |       -1.2 | -9.6%        | 39%            | -24.9%    |
| cecha: −range_pos_180                     |      45 | -0.132 |       -2.4 | -21.9%       | 25%            | -31.5%    |
| cecha: rarity_w                           |      45 | -0.137 |       -2   | -30.4%       | 5%             | -31.9%    |
| cecha: history_complete                   |      45 | -0.162 |       -1.4 | -27.9%       | 19%            | -37.2%    |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|
| łącznie: model + ocena C                  |      27 | 0.273 |        1.9 | +3.3%        | 51%            | +2.2%     |
| ocena C: popularność + wiek + tania + dno |      45 | 0.272 |        2.1 | +15.9%       | 63%            | +16.3%    |
| model: gradient boosting                  |      27 | 0.258 |        2.3 | +6.1%        | 56%            | +4.4%     |
| model: gradient boosting, cel zysk netto  |      27 | 0.246 |        2.3 | +6.0%        | 56%            | +6.2%     |
| reguły: moduł A (ocena bez bramek)        |      45 | 0.089 |        0.8 | +6.5%        | 56%            | +8.3%     |
| reguły: moduł B1 (tania vs podobne)       |      45 | 0.017 |        0.3 | +7.0%        | 55%            | +8.0%     |

Stabilność (6 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |       4 | 0.432 |        6   | +50.3%       | 98%            | +8.1%     |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      22 | 0.371 |        3.3 | +51.3%       | 86%            | +30.6%    |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      22 | 0.169 |        2.3 | -4.8%        | 42%            | -18.1%    |
| 1. połowa (od 2024-08) | model: gradient boosting                  |       4 | 0.159 |        1.3 | +7.9%        | 49%            | -29.6%    |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      22 | 0.132 |        0.9 | -15.5%       | 33%            | -28.7%    |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      22 | 0.095 |        3.4 | +16.2%       | 59%            | -13.3%    |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      22 | 0.069 |        0.5 | +13.9%       | 62%            | +6.3%     |
| 2. połowa (od 2025-06) | model: gradient boosting                  |      23 | 0.229 |        2.2 | +12.3%       | 66%            | -3.4%     |
| 2. połowa (od 2025-06) | łącznie: model + ocena C                  |      23 | 0.184 |        1.4 | +11.3%       | 65%            | -4.9%     |
| 2. połowa (od 2025-06) | cecha: weeks_since_low                    |      23 | 0.126 |        2.1 | +7.9%        | 62%            | -3.1%     |
| 2. połowa (od 2025-06) | ocena C: popularność + wiek + tania + dno |      23 | 0.087 |        0.7 | +9.4%        | 62%            | -6.1%     |
| 2. połowa (od 2025-06) | cecha: −drawdown                          |      23 | 0.07  |        0.7 | +11.3%       | 63%            | +1.2%     |
| 2. połowa (od 2025-06) | reguły: moduł B1 (tania vs podobne)       |      23 | 0.059 |        3   | +0.4%        | 48%            | -21.0%    |
| 2. połowa (od 2025-06) | reguły: moduł A (ocena bez bramek)        |      23 | 0.011 |        0.1 | +2.3%        | 55%            | -9.9%     |

## Horyzont 12 mies.

Daty z wynikiem: 32. Karty, które przeszły bramki modułu A: 42 obserwacji, średni zwrot ponad rynek +21.8%.

| signal                                    |   dates |     ic | ic_t_adj   | top_excess   | top_hit_rate   | top_net   |
|:------------------------------------------|--------:|-------:|:-----------|:-------------|:---------------|:----------|
| ocena C: popularność + wiek + tania + dno |      32 |  0.347 | +2.2       | +57.4%       | 82%            | +66.2%    |
| cecha: tier_score                         |      32 |  0.316 | +2.6       | -9.2%        | 40%            | +6.2%     |
| cecha: poke_pop                           |      32 |  0.309 | +2.7       | +39.6%       | 77%            | +61.3%    |
| cecha: age_months                         |      32 |  0.288 | +1.4       | +51.3%       | 86%            | +65.1%    |
| cecha: buzz_eng                           |      32 |  0.248 | +2.5       | +14.8%       | 65%            | +24.3%    |
| cecha: buzz_share                         |      32 |  0.244 | +2.5       | +13.8%       | 65%            | +22.9%    |
| cecha: weeks_since_low                    |      32 |  0.2   | +2.3       | -4.4%        | 48%            | -0.5%     |
| cecha: range_pos_180                      |      32 |  0.16  | +1.6       | -15.8%       | 39%            | -10.7%    |
| cecha: −drawdown                          |      32 |  0.155 | +1.2       | -18.8%       | 37%            | -13.4%    |
| łącznie: model + ocena C                  |       1 |  0.13  | +nan       | +10.8%       | 65%            | +8.1%     |
| cecha: slope_180                          |      32 |  0.125 | +1.1       | -21.9%       | 34%            | -12.3%    |
| model: gradient boosting                  |       1 |  0.123 | +nan       | +2.6%        | 55%            | +2.0%     |
| reguły: moduł A (ocena bez bramek)        |      32 |  0.105 | +0.8       | +17.9%       | 66%            | +30.3%    |
| cecha: above_low                          |      32 |  0.092 | +1.0       | -25.5%       | 35%            | -14.2%    |
| cecha: −rv_z                              |      32 |  0.092 | +3.2       | +19.4%       | 66%            | +13.0%    |
| reguły: moduł B1 (tania vs podobne)       |      32 |  0.092 | +3.2       | +19.4%       | 66%            | +13.0%    |
| model: gradient boosting, cel zysk netto  |       1 |  0.091 | +nan       | -4.5%        | 45%            | +1.6%     |
| cecha: slope_30                           |      32 |  0.081 | +0.9       | -27.5%       | 32%            | -18.9%    |
| cecha: slope_60                           |      32 |  0.068 | +0.8       | -30.8%       | 30%            | -20.1%    |
| cecha: slope_90                           |      32 |  0.06  | +0.7       | -28.5%       | 29%            | -18.7%    |
| cecha: special                            |      32 |  0.051 | +0.9       | -22.4%       | 31%            | -16.0%    |
| cecha: buzz_growth                        |      32 |  0.048 | +0.7       | +7.2%        | 57%            | +12.3%    |
| cecha: vol_ratio                          |      32 |  0.045 | +0.5       | -0.9%        | 46%            | +3.2%     |
| cecha: set_trend_90                       |      32 |  0.045 | +0.4       | -4.8%        | 44%            | -3.4%     |
| model: ridge na rangach                   |       1 |  0.035 | +nan       | +19.8%       | 70%            | +19.8%    |
| cecha: logp                               |      32 |  0.031 | +0.3       | +2.4%        | 48%            | +26.5%    |
| cecha: sealed_slope_90                    |      32 | -0.008 | -0.0       | -5.1%        | 44%            | -1.6%     |
| cecha: new_same_poke_90                   |      32 | -0.009 | -0.2       | -13.6%       | 38%            | -6.9%     |
| cecha: set_rel                            |      32 | -0.009 | -0.2       | +1.0%        | 44%            | +22.2%    |
| cecha: new_same_poke_365                  |      32 | -0.019 | -0.4       | -16.5%       | 34%            | -1.6%     |
| cecha: spread                             |      32 | -0.029 | -0.4       | -4.5%        | 49%            | -10.6%    |
| cecha: −slope_90                          |      32 | -0.06  | -0.7       | -30.9%       | 29%            | -29.0%    |
| cecha: rv_z                               |      32 | -0.092 | -3.2       | -2.9%        | 47%            | +16.3%    |
| cecha: drawdown                           |      32 | -0.155 | -1.2       | -19.5%       | 36%            | -16.0%    |
| cecha: −range_pos_180                     |      32 | -0.16  | -1.6       | -36.5%       | 17%            | -33.9%    |
| cecha: rarity_w                           |      32 | -0.169 | -1.8       | -44.3%       | 1%             | -38.0%    |
| cecha: history_complete                   |      32 | -0.24  | -2.5       | -38.6%       | 20%            | -36.1%    |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic | ic_t_adj   | top_excess   | top_hit_rate   | top_net   |
|:------------------------------------------|--------:|------:|:-----------|:-------------|:---------------|:----------|
| ocena C: popularność + wiek + tania + dno |      32 | 0.405 | +2.5       | +36.7%       | 79%            | +58.8%    |
| łącznie: model + ocena C                  |       1 | 0.286 | +nan       | +4.6%        | 65%            | +14.3%    |
| model: gradient boosting, cel zysk netto  |       1 | 0.254 | +nan       | -3.6%        | 50%            | +8.2%     |
| model: gradient boosting                  |       1 | 0.208 | +nan       | -3.6%        | 55%            | +5.6%     |
| reguły: moduł A (ocena bez bramek)        |      32 | 0.106 | +0.7       | +11.4%       | 61%            | +31.8%    |
| reguły: moduł B1 (tania vs podobne)       |      32 | 0.086 | +0.8       | +15.8%       | 63%            | +39.3%    |

## Bieżący ranking modelu (6 mies., karty od $20)

Stan na 2026-10-18. Kolejność wg `score` = średnia rang modelu (`model_6m`) i oceny C (`combo`), 1 = najlepsza. `model_6m` = przewidywany log-zwrot ponad rynek w 6 mies. (0,20 ≈ +22%), `model_net_6m` = to samo po kosztach, `spread` = log(cena rynkowa / najniższa oferta). To lista do sprawdzenia, nie rekomendacja zakupu.

| name                                              | set_name                               |   price_now |   spread |   poke_pop |   rv_z |   weeks_since_low |   buzz_share |   combo |   model_6m |   model_net_6m |   score |
|:--------------------------------------------------|:---------------------------------------|------------:|---------:|-----------:|-------:|------------------:|-------------:|--------:|-----------:|---------------:|--------:|
| Venusaur & Snivy GX                               | SM - Cosmic Eclipse                    |       26.06 |     0.21 |       1.25 |  -1.57 |                25 |         1.39 |    1.12 |       0.26 |           0.28 |    0.98 |
| Lugia                                             | SM - Team Up                           |       21.49 |     0.42 |       3.51 |   0.29 |                25 |        12.12 |    1.10 |       0.21 |           0.23 |    0.97 |
| Gardevoir & Sylveon GX (205) (Alternate Full Art) | SM - Unbroken Bonds                    |      700.80 |    -0.25 |       1.67 |   0.00 |                25 |         0.32 |    0.84 |       0.31 |           0.50 |    0.96 |
| Gengar                                            | SM - Unbroken Bonds                    |       22.94 |     0.44 |       4.40 |   0.09 |                25 |         7.40 |    1.18 |       0.20 |           0.13 |    0.96 |
| Rayquaza VMAX (Secret)                            | SWSH12: Silver Tempest Trainer Gallery |       24.31 |     0.01 |       2.92 |   0.04 |                25 |         3.22 |    0.70 |       0.28 |           0.33 |    0.94 |
| Espeon V (Full Art)                               | SWSH07: Evolving Skies                 |       25.93 |     0.12 |       2.96 |  -0.21 |                24 |         1.39 |    0.68 |       0.27 |           0.36 |    0.94 |
| Umbreon V (Alternate Full Art)                    | SWSH07: Evolving Skies                 |      380.03 |     0.13 |       3.70 |   0.57 |                25 |         5.79 |    0.74 |       0.21 |           0.39 |    0.93 |
| Slowpoke & Psyduck GX (Full Art)                  | SM - Unified Minds                     |      156.98 |    -0.05 |       2.05 |   1.16 |                25 |         0.21 |    0.58 |       0.25 |           0.47 |    0.92 |
| Gardevoir & Sylveon GX (204) (Full Art)           | SM - Unbroken Bonds                    |      117.69 |    -0.02 |       2.04 |   0.01 |                25 |         0.32 |    0.94 |       0.17 |           0.36 |    0.91 |
| Pikachu VMAX (Secret)                             | SWSH11: Lost Origin Trainer Gallery    |       24.15 |     0.20 |       2.34 |   0.04 |                25 |        14.48 |    0.59 |       0.23 |           0.28 |    0.91 |
| Lucario                                           | Hidden Fates: Shiny Vault              |       21.77 |     0.18 |       2.58 |  -1.12 |                25 |         1.61 |    1.45 |       0.15 |           0.18 |    0.91 |
| Shining Magikarp                                  | Celebrations: Classic Collection       |       32.43 |     0.15 |       3.64 |  -0.66 |                 0 |         2.15 |    0.51 |       0.25 |           0.28 |    0.90 |
| Umbreon VMAX                                      | SWSH07: Evolving Skies                 |       27.93 |     0.22 |       3.58 |  -0.15 |                 9 |         5.79 |    0.50 |       0.27 |           0.36 |    0.90 |
| Mew                                               | SM - Unbroken Bonds                    |       25.37 |     0.70 |       1.87 |   0.53 |                25 |        18.23 |    0.71 |       0.18 |           0.19 |    0.89 |
| M Rayquaza EX                                     | Celebrations: Classic Collection       |       34.98 |     0.15 |       3.96 |  -0.62 |                 0 |         3.22 |    0.50 |       0.22 |           0.30 |    0.89 |
| Leafeon V (Full Art)                              | SWSH07: Evolving Skies                 |       22.41 |     0.11 |       2.85 |   0.69 |                25 |         0.32 |    0.61 |       0.18 |           0.29 |    0.88 |
| Rayquaza                                          | SWSH04: Vivid Voltage                  |       21.39 |     0.17 |       2.92 |  -0.36 |                 0 |         3.22 |    0.45 |       0.23 |           0.29 |    0.88 |
| Gengar & Mimikyu GX (Alternate Full Art)          | SM - Team Up                           |     2119.05 |    -0.18 |       4.12 |   2.04 |                21 |         7.40 |    0.38 |       0.30 |           0.51 |    0.88 |
| Flareon V (Full Art)                              | SWSH07: Evolving Skies                 |       21.37 |     0.17 |       2.43 |   0.63 |                25 |         0.54 |    0.53 |       0.20 |           0.29 |    0.87 |
| Charizard ex - 215/197                            | SV03: Obsidian Flames                  |       21.60 |     0.26 |       2.57 |  -0.07 |                25 |        13.84 |    0.57 |       0.18 |           0.25 |    0.87 |
| Umbreon Star                                      | Celebrations: Classic Collection       |       75.76 |     0.06 |       4.24 |  -0.24 |                 0 |         5.79 |    0.37 |       0.24 |           0.35 |    0.86 |
| Espeon (Master Ball Pattern)                      | SV: Prismatic Evolutions               |       28.04 |     0.09 |       2.96 | nan    |                25 |         1.39 |    0.42 |       0.21 |           0.31 |    0.86 |
| Snorlax                                           | SWSH11: Lost Origin Trainer Gallery    |       22.37 |     0.31 |     nan    |  -0.04 |                25 |         1.72 |    0.37 |       0.23 |           0.25 |    0.86 |
| Whimsicott GX (Secret)                            | SM - Unbroken Bonds                    |       27.49 |    -0.21 |       0.54 |   0.63 |                25 |         0.11 |    0.35 |       0.24 |           0.36 |    0.86 |
| Umbreon V (Full Art)                              | SWSH07: Evolving Skies                 |       56.00 |     0.23 |       3.58 |   0.39 |                25 |         5.79 |    0.78 |       0.15 |           0.34 |    0.86 |

## Rynek: kiedy kupować

Trend rynku = mediana trendów cen wszystkich kart (%/mies.). Na historii szybki wzrost rynku zapowiadał słabsze kolejne miesiące, a spokojny lub spadający rynek – lepsze (korelacja rang poniżej; to tylko ok. 2 cykle, więc traktuj orientacyjnie).

|           |   zwrot_3m |   zwrot_6m |
|:----------|-----------:|-----------:|
| trend_90  |      -0.3  |      -0.46 |
| trend_180 |      -0.61 |      -0.48 |

Teraz (2026-10-18): trend 90 dni -2.2%/mies. (wyżej niż w 3% historii), trend 180 dni +2.1%/mies. (wyżej niż w 55% historii).

## Kontrola na żywo

Każdy przebieg zapisuje top-20 do `reports/picks_log.csv`; po 3 i 6 mies. liczymy, jak wypadły.

Zapisane dni z wyborami: 1. Pierwsze wyniki po 3 mies. od 2026-10-18.
