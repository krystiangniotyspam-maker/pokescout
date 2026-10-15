# PokeScout – test przewidywań na historii

Dane: 138 dni notowań, 4776 kart w katalogu; panel 77078 obserwacji (2024-08-11 – 2026-10-18, co 2 tygodnie).

**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, 0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. `top_excess` = średni zwrot 20 najwyżej ocenionych kart ponad medianę rynku, `top_hit_rate` = jaki odsetek z nich pobił rynek, `top_net` = ich średni zwrot netto po kosztach (prowizja 13% i wysyłka $1,5 w każdą stronę) – realny zysk, nie ponad rynek, `top_up50` = jaki odsetek z nich zdrożał o 50% lub więcej.

## Horyzont 3 mies.

Daty z wynikiem: 51. Karty, które przeszły bramki modułu A: 200 obserwacji, średni zwrot ponad rynek +1.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: gradient boosting                  |      39 |  0.309 |        4.2 | +5.6%        | 61%            | -19.5%    | 0.115385   |
| łącznie: model + ocena C                  |      39 |  0.294 |        7.1 | +11.0%       | 66%            | -17.1%    | 0.133333   |
| ranking: szansa na +50% + model zwrotu    |      39 |  0.27  |        3.4 | +5.7%        | 58%            | -22.5%    | 0.146154   |
| ocena C: popularność + wiek + tania + dno |      51 |  0.174 |        3   | +13.5%       | 69%            | -14.7%    | 0.173529   |
| model: szansa na wzrost o 50%+            |      39 |  0.174 |        2   | +5.9%        | 59%            | -24.1%    | 0.167949   |
| cecha: age_months                         |      51 |  0.156 |        1.4 | +10.5%       | 65%            | -7.9%     | 0.101961   |
| cecha: poke_pop                           |      51 |  0.151 |        3   | +9.0%        | 62%            | -5.8%     | 0.15       |
| model: ridge na rangach                   |      39 |  0.15  |        1.9 | +11.4%       | 71%            | -10.3%    | 0.137179   |
| cecha: tier_score                         |      51 |  0.145 |        2.7 | -3.7%        | 42%            | -16.5%    | 0.112745   |
| cecha: range_pos_180                      |      51 |  0.131 |        3.2 | -0.0%        | 50%            | -21.8%    | 0.148039   |
| model: gradient boosting, cel zysk netto  |      39 |  0.114 |        2.2 | +6.2%        | 64%            | -4.5%     | 0.0782051  |
| cecha: buzz_eng                           |      51 |  0.113 |        2.1 | +3.8%        | 56%            | -14.3%    | 0.120588   |
| cecha: buzz_share                         |      51 |  0.111 |        2.1 | +3.2%        | 55%            | -15.2%    | 0.116667   |
| cecha: slope_30                           |      51 |  0.101 |        2.1 | -14.1%       | 33%            | -33.0%    | 0.0882353  |
| cecha: −drawdown                          |      51 |  0.092 |        1.5 | +0.7%        | 52%            | -20.2%    | 0.167647   |
| cecha: weeks_since_low                    |      51 |  0.087 |        3.4 | +1.6%        | 51%            | -21.7%    | 0.146078   |
| cecha: set_trend_90                       |      51 |  0.076 |        1.1 | -0.5%        | 49%            | -24.5%    | 0.0784314  |
| cecha: slope_60                           |      51 |  0.073 |        1.3 | -16.7%       | 28%            | -34.3%    | 0.0715686  |
| cecha: vol_ratio                          |      51 |  0.067 |        2.9 | -1.8%        | 46%            | -24.6%    | 0.0882353  |
| reguły: moduł B1 (tania vs podobne)       |      51 |  0.064 |        3.3 | +4.1%        | 52%            | -31.2%    | 0.113725   |
| cecha: −rv_z                              |      51 |  0.064 |        3.3 | +4.1%        | 52%            | -31.2%    | 0.113725   |
| reguły: moduł A (ocena bez bramek)        |      51 |  0.051 |        0.9 | +4.1%        | 52%            | -16.4%    | 0.138235   |
| cecha: slope_90                           |      51 |  0.036 |        0.7 | -16.6%       | 28%            | -34.5%    | 0.0735294  |
| cecha: buzz_growth                        |      51 |  0.035 |        2.4 | +2.7%        | 53%            | -21.8%    | 0.110784   |
| cecha: special                            |      51 |  0.032 |        0.8 | -10.1%       | 32%            | -29.8%    | 0.10098    |
| cecha: above_low                          |      51 |  0.031 |        0.5 | -16.5%       | 30%            | -34.2%    | 0.0803922  |
| cecha: sealed_slope_90                    |      51 |  0.023 |        0.4 | -3.2%        | 43%            | -25.9%    | 0.0529412  |
| cecha: new_same_poke_90                   |      51 |  0.006 |        0.3 | +0.0%        | 50%            | -19.9%    | 0.112745   |
| cecha: slope_180                          |      51 | -0     |       -0   | -13.4%       | 31%            | -30.4%    | 0.0843137  |
| cecha: new_same_poke_365                  |      51 | -0.005 |       -0.3 | -6.3%        | 31%            | -27.0%    | 0.0735294  |
| cecha: logp                               |      51 | -0.022 |       -0.7 | +0.1%        | 50%            | -5.1%     | 0.0745098  |
| cecha: set_rel                            |      51 | -0.023 |       -0.7 | +1.8%        | 51%            | -3.5%     | 0.0941176  |
| cecha: −slope_90                          |      51 | -0.036 |       -0.7 | -15.4%       | 24%            | -41.2%    | 0.0294118  |
| cecha: rv_z                               |      51 | -0.064 |       -3.3 | +0.2%        | 51%            | -9.1%     | 0.0754902  |
| cecha: spread                             |      51 | -0.071 |       -2.3 | -3.6%        | 45%            | -37.9%    | 0.0990196  |
| cecha: drawdown                           |      51 | -0.092 |       -1.5 | -4.6%        | 39%            | -34.2%    | 0.0901961  |
| cecha: rarity_w                           |      51 | -0.092 |       -1.6 | -19.1%       | 12%            | -28.2%    | 0.00980392 |
| cecha: −range_pos_180                     |      51 | -0.131 |       -3.2 | -14.9%       | 24%            | -35.4%    | 0.027451   |
| cecha: history_complete                   |      51 | -0.157 |       -2.6 | -18.9%       | 20%            | -38.5%    | 0.0529412  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: gradient boosting                  |      39 | 0.382 |        5   | +6.8%        | 63%            | -5.9%     |  0.0961538 |
| łącznie: model + ocena C                  |      39 | 0.352 |        5.7 | +11.0%       | 67%            | -3.1%     |  0.108974  |
| ranking: szansa na +50% + model zwrotu    |      39 | 0.337 |        4.4 | +6.3%        | 58%            | -6.6%     |  0.130769  |
| model: gradient boosting, cel zysk netto  |      39 | 0.326 |        4.3 | +5.9%        | 64%            | -4.3%     |  0.0769231 |
| ocena C: popularność + wiek + tania + dno |      51 | 0.196 |        2.5 | +7.7%        | 60%            | -3.8%     |  0.108824  |
| model: szansa na wzrost o 50%+            |      39 | 0.189 |        1.9 | +7.3%        | 59%            | -5.6%     |  0.15      |
| reguły: moduł A (ocena bez bramek)        |      51 | 0.098 |        1.4 | +4.9%        | 53%            | -4.6%     |  0.141176  |
| reguły: moduł B1 (tania vs podobne)       |      51 | 0.016 |        0.6 | +3.2%        | 50%            | -8.1%     |  0.133333  |

Stabilność (3 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |      13 | 0.307 |        3.5 | +22.2%       | 76%            | -14.3%    |  0.203846  |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      25 | 0.241 |        3.1 | +24.2%       | 83%            | -6.4%     |  0.272     |
| 1. połowa (od 2024-08) | model: gradient boosting                  |      13 | 0.149 |        0.9 | -2.0%        | 41%            | -32.6%    |  0.0846154 |
| 1. połowa (od 2024-08) | ranking: szansa na +50% + model zwrotu    |      13 | 0.131 |        0.7 | +2.4%        | 47%            | -30.4%    |  0.153846  |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      25 | 0.103 |        1.1 | -5.4%        | 45%            | -28.3%    |  0.124     |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      25 | 0.089 |        4.9 | +10.0%       | 61%            | -28.3%    |  0.168     |
| 1. połowa (od 2024-08) | model: szansa na wzrost o 50%+            |      13 | 0.089 |        0.5 | +3.2%        | 51%            | -30.6%    |  0.161538  |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      25 | 0.081 |        0.9 | +7.9%        | 59%            | -11.4%    |  0.18      |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      25 | 0.079 |        1.9 | +1.3%        | 48%            | -23.4%    |  0.146     |
| 2. połowa (od 2025-07) | model: gradient boosting                  |      26 | 0.388 |       15.2 | +9.7%        | 72%            | -12.9%    |  0.130769  |
| 2. połowa (od 2025-07) | ranking: szansa na +50% + model zwrotu    |      26 | 0.339 |        6   | +7.4%        | 64%            | -18.5%    |  0.142308  |
| 2. połowa (od 2025-07) | łącznie: model + ocena C                  |      26 | 0.288 |        6.3 | +5.9%        | 62%            | -18.5%    |  0.0980769 |
| 2. połowa (od 2025-07) | model: szansa na wzrost o 50%+            |      26 | 0.216 |        2.4 | +7.3%        | 63%            | -20.8%    |  0.171154  |
| 2. połowa (od 2025-07) | ocena C: popularność + wiek + tania + dno |      26 | 0.111 |        1.5 | +4.0%        | 55%            | -22.6%    |  0.0788462 |
| 2. połowa (od 2025-07) | cecha: weeks_since_low                    |      26 | 0.094 |        3.1 | +2.0%        | 54%            | -20.0%    |  0.146154  |
| 2. połowa (od 2025-07) | cecha: −drawdown                          |      26 | 0.081 |        1.1 | +6.9%        | 58%            | -12.5%    |  0.209615  |
| 2. połowa (od 2025-07) | reguły: moduł B1 (tania vs podobne)       |      26 | 0.041 |        1.3 | -1.3%        | 44%            | -34.1%    |  0.0615385 |
| 2. połowa (od 2025-07) | reguły: moduł A (ocena bez bramek)        |      26 | 0.022 |        0.3 | +0.6%        | 46%            | -21.1%    |  0.0980769 |

## Horyzont 6 mies.

Daty z wynikiem: 45. Karty, które przeszły bramki modułu A: 133 obserwacji, średni zwrot ponad rynek -2.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      27 |  0.27  |        3.3 | +13.1%       | 66%            | -4.8%     |  0.348148  |
| model: szansa na wzrost o 50%+            |      27 |  0.259 |        3.2 | +12.6%       | 64%            | -5.7%     |  0.344444  |
| model: gradient boosting                  |      27 |  0.25  |        3.1 | +9.7%        | 59%            | -7.9%     |  0.318519  |
| łącznie: model + ocena C                  |      27 |  0.243 |        2.2 | +12.6%       | 66%            | -6.0%     |  0.318519  |
| ocena C: popularność + wiek + tania + dno |      45 |  0.232 |        2.2 | +27.9%       | 74%            | +12.0%    |  0.426667  |
| cecha: poke_pop                           |      45 |  0.217 |        2.7 | +17.6%       | 66%            | +14.1%    |  0.354444  |
| cecha: tier_score                         |      45 |  0.201 |        2.3 | -6.4%        | 42%            | -8.1%     |  0.213333  |
| cecha: age_months                         |      45 |  0.176 |        1   | +20.4%       | 66%            | +14.5%    |  0.336667  |
| model: gradient boosting, cel zysk netto  |      27 |  0.159 |        1.7 | +9.6%        | 60%            | +6.7%     |  0.253704  |
| cecha: buzz_eng                           |      45 |  0.153 |        1.9 | +4.5%        | 58%            | -4.2%     |  0.254444  |
| cecha: buzz_share                         |      45 |  0.149 |        1.9 | +3.6%        | 56%            | -5.3%     |  0.246667  |
| cecha: weeks_since_low                    |      45 |  0.148 |        3.5 | +1.0%        | 51%            | -10.4%    |  0.304444  |
| model: ridge na rangach                   |      27 |  0.123 |        0.9 | +17.6%       | 68%            | +6.0%     |  0.362963  |
| cecha: range_pos_180                      |      45 |  0.123 |        2.5 | -3.7%        | 48%            | -13.6%    |  0.275556  |
| cecha: slope_180                          |      45 |  0.095 |        1.5 | -17.6%       | 35%            | -23.4%    |  0.167778  |
| cecha: −drawdown                          |      45 |  0.086 |        1   | -4.7%        | 46%            | -14.1%    |  0.272222  |
| cecha: above_low                          |      45 |  0.076 |        0.9 | -22.0%       | 33%            | -27.5%    |  0.162222  |
| cecha: special                            |      45 |  0.071 |        1.1 | -9.7%        | 41%            | -16.8%    |  0.282222  |
| cecha: −rv_z                              |      45 |  0.069 |        3.1 | +8.1%        | 54%            | -17.5%    |  0.298889  |
| reguły: moduł B1 (tania vs podobne)       |      45 |  0.069 |        3.1 | +8.1%        | 54%            | -17.5%    |  0.298889  |
| reguły: moduł A (ocena bez bramek)        |      45 |  0.058 |        0.8 | +7.5%        | 58%            | -2.3%     |  0.314444  |
| cecha: vol_ratio                          |      45 |  0.051 |        1.2 | -1.2%        | 46%            | -13.5%    |  0.211111  |
| cecha: slope_30                           |      45 |  0.049 |        0.8 | -21.2%       | 31%            | -29.1%    |  0.154444  |
| cecha: set_trend_90                       |      45 |  0.048 |        0.4 | -1.4%        | 47%            | -16.3%    |  0.206667  |
| cecha: slope_60                           |      45 |  0.034 |        0.5 | -24.6%       | 27%            | -31.2%    |  0.144444  |
| cecha: slope_90                           |      45 |  0.032 |        0.5 | -23.2%       | 28%            | -29.0%    |  0.138889  |
| cecha: buzz_growth                        |      45 |  0.023 |        0.8 | +4.0%        | 53%            | -9.3%     |  0.247778  |
| cecha: logp                               |      45 | -0.011 |       -0.2 | -0.2%        | 47%            | +5.4%     |  0.198889  |
| cecha: set_rel                            |      45 | -0.014 |       -0.4 | +1.6%        | 50%            | +6.1%     |  0.191111  |
| cecha: new_same_poke_90                   |      45 | -0.017 |       -0.6 | -4.8%        | 43%            | -14.4%    |  0.23      |
| cecha: sealed_slope_90                    |      45 | -0.026 |       -0.2 | -6.3%        | 37%            | -19.1%    |  0.144444  |
| cecha: new_same_poke_365                  |      45 | -0.029 |       -1.9 | -11.6%       | 28%            | -21.9%    |  0.154444  |
| cecha: −slope_90                          |      45 | -0.032 |       -0.5 | -22.0%       | 27%            | -35.3%    |  0.136667  |
| cecha: spread                             |      45 | -0.055 |       -1.2 | -4.2%        | 47%            | -27.4%    |  0.226667  |
| cecha: rv_z                               |      45 | -0.069 |       -3.1 | +1.3%        | 53%            | +3.0%     |  0.195556  |
| cecha: drawdown                           |      45 | -0.086 |       -1   | -10.1%       | 38%            | -27.9%    |  0.187778  |
| cecha: rarity_w                           |      45 | -0.117 |       -1.5 | -30.4%       | 5%             | -31.9%    |  0.0122222 |
| cecha: −range_pos_180                     |      45 | -0.123 |       -2.5 | -20.8%       | 23%            | -31.0%    |  0.0966667 |
| cecha: history_complete                   |      45 | -0.17  |       -1.7 | -28.1%       | 19%            | -37.3%    |  0.0988889 |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ocena C: popularność + wiek + tania + dno |      45 | 0.271 |        2.1 | +15.7%       | 62%            | +16.2%    |   0.331111 |
| łącznie: model + ocena C                  |      27 | 0.269 |        1.9 | +3.0%        | 52%            | +1.6%     |   0.174074 |
| model: gradient boosting                  |      27 | 0.253 |        2.3 | +5.8%        | 56%            | +3.9%     |   0.207407 |
| ranking: szansa na +50% + model zwrotu    |      27 | 0.252 |        2.4 | +7.9%        | 60%            | +6.7%     |   0.227778 |
| model: gradient boosting, cel zysk netto  |      27 | 0.228 |        2.2 | +6.1%        | 56%            | +6.2%     |   0.2      |
| model: szansa na wzrost o 50%+            |      27 | 0.217 |        2.3 | +8.6%        | 61%            | +8.3%     |   0.222222 |
| reguły: moduł A (ocena bez bramek)        |      45 | 0.096 |        0.9 | +6.7%        | 56%            | +8.4%     |   0.304444 |
| reguły: moduł B1 (tania vs podobne)       |      45 | 0.024 |        0.4 | +8.1%        | 56%            | +8.9%     |   0.314444 |

Stabilność (6 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |       4 | 0.436 |        4.4 | +49.0%       | 98%            | +6.9%     |   0.525    |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      22 | 0.369 |        3.4 | +53.8%       | 89%            | +33.0%    |   0.620455 |
| 1. połowa (od 2024-08) | model: gradient boosting                  |       4 | 0.187 |        1.2 | +12.1%       | 54%            | -25.0%    |   0.2625   |
| 1. połowa (od 2024-08) | ranking: szansa na +50% + model zwrotu    |       4 | 0.169 |        1.5 | +16.4%       | 56%            | -20.1%    |   0.3375   |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      22 | 0.164 |        2.4 | -4.8%        | 42%            | -18.1%    |   0.247727 |
| 1. połowa (od 2024-08) | model: szansa na wzrost o 50%+            |       4 | 0.145 |        2.5 | +14.5%       | 56%            | -22.1%    |   0.275    |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      22 | 0.123 |        0.9 | -15.4%       | 33%            | -28.5%    |   0.186364 |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      22 | 0.097 |        3.4 | +18.0%       | 60%            | -11.9%    |   0.377273 |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      22 | 0.074 |        0.5 | +13.9%       | 62%            | +6.3%     |   0.393182 |
| 2. połowa (od 2025-06) | ranking: szansa na +50% + model zwrotu    |      23 | 0.287 |        3.3 | +12.5%       | 68%            | -2.1%     |   0.35     |
| 2. połowa (od 2025-06) | model: szansa na wzrost o 50%+            |      23 | 0.279 |        3.2 | +12.3%       | 66%            | -2.9%     |   0.356522 |
| 2. połowa (od 2025-06) | model: gradient boosting                  |      23 | 0.261 |        2.9 | +9.3%        | 59%            | -4.9%     |   0.328261 |
| 2. połowa (od 2025-06) | łącznie: model + ocena C                  |      23 | 0.209 |        1.9 | +7.2%        | 60%            | -8.3%     |   0.282609 |
| 2. połowa (od 2025-06) | cecha: weeks_since_low                    |      23 | 0.133 |        2.7 | +7.0%        | 60%            | -3.1%     |   0.358696 |
| 2. połowa (od 2025-06) | ocena C: popularność + wiek + tania + dno |      23 | 0.101 |        0.9 | +7.3%        | 60%            | -8.1%     |   0.241304 |
| 2. połowa (od 2025-06) | cecha: −drawdown                          |      23 | 0.052 |        0.5 | +6.7%        | 59%            | -0.3%     |   0.354348 |
| 2. połowa (od 2025-06) | reguły: moduł A (ocena bez bramek)        |      23 | 0.043 |        0.6 | +1.8%        | 54%            | -10.5%    |   0.23913  |
| 2. połowa (od 2025-06) | reguły: moduł B1 (tania vs podobne)       |      23 | 0.043 |        2.4 | -0.7%        | 48%            | -22.8%    |   0.223913 |

## Horyzont 12 mies.

Daty z wynikiem: 32. Karty, które przeszły bramki modułu A: 42 obserwacji, średni zwrot ponad rynek +21.7%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      14 |  0.441 |        2.7 | +38.2%       | 80%            | +46.6%    |  0.696429  |
| model: szansa na wzrost o 50%+            |      14 |  0.435 |        2.3 | +39.5%       | 82%            | +46.3%    |  0.710714  |
| model: gradient boosting                  |      14 |  0.401 |        2.9 | +32.7%       | 72%            | +40.6%    |  0.639286  |
| łącznie: model + ocena C                  |      14 |  0.35  |        2.2 | +35.4%       | 82%            | +38.6%    |  0.703571  |
| ocena C: popularność + wiek + tania + dno |      32 |  0.341 |        2.2 | +55.4%       | 81%            | +64.9%    |  0.715625  |
| cecha: poke_pop                           |      32 |  0.327 |        3.4 | +37.8%       | 76%            | +60.1%    |  0.646875  |
| cecha: tier_score                         |      32 |  0.325 |        2.7 | -1.4%        | 48%            | +16.2%    |  0.370312  |
| model: gradient boosting, cel zysk netto  |      14 |  0.301 |        1.8 | +30.6%       | 75%            | +57.0%    |  0.660714  |
| cecha: age_months                         |      32 |  0.273 |        1.3 | +48.5%       | 84%            | +66.0%    |  0.753125  |
| model: ridge na rangach                   |      14 |  0.263 |        1.1 | +35.6%       | 76%            | +51.8%    |  0.678571  |
| cecha: buzz_eng                           |      32 |  0.259 |        2.6 | +14.8%       | 65%            | +24.2%    |  0.478125  |
| cecha: buzz_share                         |      32 |  0.255 |        2.6 | +13.8%       | 65%            | +22.8%    |  0.460938  |
| cecha: weeks_since_low                    |      32 |  0.196 |        2.4 | -4.3%        | 48%            | -0.4%     |  0.385937  |
| cecha: range_pos_180                      |      32 |  0.152 |        1.4 | -15.8%       | 39%            | -10.4%    |  0.292188  |
| cecha: −drawdown                          |      32 |  0.141 |        1   | -18.7%       | 37%            | -13.2%    |  0.28125   |
| cecha: slope_180                          |      32 |  0.121 |        1.1 | -25.8%       | 29%            | -17.6%    |  0.192188  |
| reguły: moduł A (ocena bez bramek)        |      32 |  0.119 |        1   | +17.8%       | 66%            | +30.2%    |  0.56875   |
| cecha: above_low                          |      32 |  0.092 |        1.1 | -30.2%       | 31%            | -20.9%    |  0.229687  |
| reguły: moduł B1 (tania vs podobne)       |      32 |  0.091 |        2.8 | +20.5%       | 67%            | +13.2%    |  0.571875  |
| cecha: −rv_z                              |      32 |  0.091 |        2.8 | +20.5%       | 67%            | +13.2%    |  0.571875  |
| cecha: slope_30                           |      32 |  0.076 |        0.8 | -28.0%       | 31%            | -19.5%    |  0.235938  |
| cecha: special                            |      32 |  0.066 |        1.1 | -22.4%       | 31%            | -15.9%    |  0.221875  |
| cecha: slope_60                           |      32 |  0.064 |        0.6 | -32.6%       | 28%            | -23.2%    |  0.192188  |
| cecha: slope_90                           |      32 |  0.057 |        0.5 | -30.6%       | 27%            | -21.5%    |  0.182813  |
| cecha: vol_ratio                          |      32 |  0.045 |        0.5 | -1.4%        | 45%            | +3.2%     |  0.346875  |
| cecha: buzz_growth                        |      32 |  0.044 |        0.6 | +7.4%        | 57%            | +12.3%    |  0.409375  |
| cecha: logp                               |      32 |  0.041 |        0.4 | +2.5%        | 48%            | +26.5%    |  0.351562  |
| cecha: set_trend_90                       |      32 |  0.039 |        0.3 | -5.6%        | 43%            | -4.6%     |  0.282813  |
| cecha: set_rel                            |      32 | -0.003 |       -0.1 | +1.0%        | 44%            | +22.1%    |  0.320312  |
| cecha: new_same_poke_90                   |      32 | -0.005 |       -0.1 | -13.2%       | 38%            | -6.2%     |  0.315625  |
| cecha: new_same_poke_365                  |      32 | -0.012 |       -0.3 | -16.4%       | 34%            | -1.4%     |  0.289062  |
| cecha: sealed_slope_90                    |      32 | -0.015 |       -0.1 | -7.5%        | 42%            | -4.9%     |  0.304688  |
| cecha: spread                             |      32 | -0.031 |       -0.5 | -6.7%        | 46%            | -12.5%    |  0.371875  |
| cecha: −slope_90                          |      32 | -0.057 |       -0.5 | -31.3%       | 27%            | -31.2%    |  0.201562  |
| cecha: rv_z                               |      32 | -0.091 |       -2.8 | -3.5%        | 47%            | +15.2%    |  0.325     |
| cecha: drawdown                           |      32 | -0.141 |       -1   | -19.2%       | 37%            | -17.2%    |  0.310937  |
| cecha: −range_pos_180                     |      32 | -0.152 |       -1.4 | -34.4%       | 17%            | -32.9%    |  0.107813  |
| cecha: rarity_w                           |      32 | -0.16  |       -1.9 | -44.3%       | 1%             | -38.0%    |  0.0078125 |
| cecha: history_complete                   |      32 | -0.232 |       -2.5 | -38.7%       | 20%            | -36.1%    |  0.140625  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      14 | 0.427 |        2.8 | +25.9%       | 74%            | +53.8%    |   0.625    |
| ocena C: popularność + wiek + tania + dno |      32 | 0.4   |        2.4 | +36.3%       | 79%            | +58.5%    |   0.682813 |
| model: gradient boosting                  |      14 | 0.396 |        3.3 | +21.9%       | 70%            | +47.9%    |   0.6      |
| model: szansa na wzrost o 50%+            |      14 | 0.395 |        2.2 | +22.6%       | 72%            | +50.3%    |   0.617857 |
| łącznie: model + ocena C                  |      14 | 0.353 |        2.4 | +12.4%       | 64%            | +33.7%    |   0.496429 |
| model: gradient boosting, cel zysk netto  |      14 | 0.344 |        3.6 | +19.5%       | 70%            | +46.4%    |   0.585714 |
| reguły: moduł A (ocena bez bramek)        |      32 | 0.118 |        0.9 | +12.0%       | 62%            | +32.5%    |   0.496875 |
| reguły: moduł B1 (tania vs podobne)       |      32 | 0.094 |        0.9 | +17.4%       | 63%            | +40.3%    |   0.535937 |

Stabilność (12 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      16 | 0.472 |        8.2 | +96.5%       | 89%            | +104.4%   |   0.846875 |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      16 | 0.249 |        2.1 | -19.4%       | 33%            | -20.1%    |   0.225    |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      16 | 0.212 |        4.2 | -9.1%        | 44%            | -7.1%     |   0.315625 |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      16 | 0.118 |        3.1 | +27.9%       | 68%            | +17.4%    |   0.55     |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      16 | 0.079 |        0.5 | +24.0%       | 68%            | +41.0%    |   0.5625   |
| 2. połowa (od 2025-03) | ranking: szansa na +50% + model zwrotu    |      14 | 0.441 |        2.7 | +38.2%       | 80%            | +46.6%    |   0.696429 |
| 2. połowa (od 2025-03) | model: szansa na wzrost o 50%+            |      14 | 0.435 |        2.3 | +39.5%       | 82%            | +46.3%    |   0.710714 |
| 2. połowa (od 2025-03) | model: gradient boosting                  |      14 | 0.401 |        2.9 | +32.7%       | 72%            | +40.6%    |   0.639286 |
| 2. połowa (od 2025-03) | łącznie: model + ocena C                  |      14 | 0.35  |        2.2 | +35.4%       | 82%            | +38.6%    |   0.703571 |
| 2. połowa (od 2025-03) | ocena C: popularność + wiek + tania + dno |      16 | 0.21  |        1.1 | +23.0%       | 72%            | +25.4%    |   0.584375 |
| 2. połowa (od 2025-03) | cecha: weeks_since_low                    |      16 | 0.18  |        1.1 | +0.8%        | 52%            | +6.3%     |   0.45625  |
| 2. połowa (od 2025-03) | reguły: moduł A (ocena bez bramek)        |      16 | 0.158 |        1   | +11.9%       | 64%            | +19.4%    |   0.575    |
| 2. połowa (od 2025-03) | reguły: moduł B1 (tania vs podobne)       |      16 | 0.065 |        3.3 | +13.6%       | 67%            | +9.0%     |   0.59375  |
| 2. połowa (od 2025-03) | cecha: −drawdown                          |      16 | 0.032 |        0.2 | -18.0%       | 40%            | -6.2%     |   0.3375   |

## Bieżący ranking modelu (6 mies., karty od $20)

Stan na 2026-10-18. Kolejność wg `score` (0–1, wyżej = lepiej) = średnia rang modelu szukającego kart, które zdrożeją o 50%+ (`szansa_50`), i modelu zwrotu (`model_6m`); w teście ta para najlepiej wybierała karty na rok (sekcja 12 mies.). Z jednego setu najwyżej 3 karty na początku listy, kolejne trafiają niżej. `szansa_50` porządkuje karty, ale nie jest prawdziwym prawdopodobieństwem – faktyczny odsetek wzrostów o 50%+ zależy głównie od stanu całego rynku. `model_6m` = przewidywany log-zwrot ponad rynek w 6 mies. (0,20 ≈ +22%), `model_net_6m` = to samo po kosztach, `spread` = log(cena rynkowa / najniższa oferta), `dodruk_posty` = posty o dodruku setu na Reddicie w ostatnich 8 tyg. (3+ = ostrożnie: na historii takie karty wypadały ok. 14% gorzej od rynku w 6 mies.). To lista do sprawdzenia, nie rekomendacja zakupu.

| name                        | set_name                            |   price_now |   score |   dodruk_posty |   szansa_50 |   model_6m |   combo |   spread |   poke_pop |   rv_z |   weeks_since_low |   buzz_share |   model_net_6m |
|:----------------------------|:------------------------------------|------------:|--------:|---------------:|------------:|-----------:|--------:|---------:|-----------:|-------:|------------------:|-------------:|---------------:|
| Cresselia - 071/064         | SV: Shrouded Fable                  |       27.50 |    0.99 |              0 |        0.85 |       0.23 |   -0.26 |     0.14 |     nan    |   1.14 |                25 |         0.32 |           0.36 |
| Zorua - 075/064             | SV: Shrouded Fable                  |       22.47 |    0.99 |              0 |        0.85 |       0.22 |   -0.22 |     0.12 |       1.00 |   0.85 |                25 |         0.43 |           0.35 |
| Eevee - 188/167             | SV06: Twilight Masquerade           |       69.37 |    0.98 |              0 |        0.73 |       0.24 |   -0.26 |     0.03 |       2.43 |  -0.05 |                 0 |         2.47 |           0.48 |
| Lickitung - 180/162         | SV05: Temporal Forces               |       28.54 |    0.98 |              0 |        0.79 |       0.21 |   -0.23 |     0.16 |     nan    |   1.20 |                25 |         0.21 |           0.32 |
| Metagross - 178/162         | SV05: Temporal Forces               |       31.09 |    0.98 |              0 |        0.71 |       0.24 |   -0.09 |     0.18 |     nan    |   0.58 |                25 |         0.21 |           0.35 |
| Houndoom - 066/064          | SV: Shrouded Fable                  |       57.02 |    0.98 |              0 |        0.82 |       0.20 |   -0.83 |     0.13 |      -0.53 |   2.21 |                25 |         0.54 |           0.35 |
| Arbok - 176/162             | SV05: Temporal Forces               |       28.88 |    0.98 |              0 |        0.75 |       0.21 |   -0.24 |     0.10 |     nan    |   1.21 |                25 |         0.00 |           0.32 |
| Espeon ex - 155/131         | SV: Prismatic Evolutions            |      284.77 |    0.97 |              0 |        0.77 |       0.20 |    0.15 |     0.16 |       2.95 |   0.00 |                24 |         1.39 |           0.42 |
| Hisuian Growlithe - 181/167 | SV06: Twilight Masquerade           |       26.48 |    0.97 |              0 |        0.75 |       0.20 |   -0.23 |     0.14 |     nan    |   1.09 |                25 |         0.11 |           0.31 |
| ______'s Pikachu            | Celebrations: Classic Collection    |       30.27 |    0.97 |              0 |        0.64 |       0.27 |    0.23 |     0.09 |     nan    |  -0.70 |                 9 |         0.00 |           0.31 |
| Pikachu ex - 219/191        | SV08: Surging Sparks                |       26.87 |    0.97 |              0 |        0.64 |       0.27 |   -0.41 |     0.23 |       2.33 |   0.15 |                 0 |        14.48 |           0.36 |
| Espeon V (Full Art)         | SWSH07: Evolving Skies              |       25.93 |    0.97 |              0 |        0.67 |       0.23 |    0.69 |     0.17 |       2.95 |  -0.21 |                24 |         1.39 |           0.34 |
| Latios - 203/191            | SV08: Surging Sparks                |       28.92 |    0.96 |              0 |        0.65 |       0.23 |   -0.79 |     0.19 |     nan    |   0.48 |                 0 |         0.75 |           0.35 |
| Umbreon VMAX                | SWSH07: Evolving Skies              |       28.06 |    0.96 |              0 |        0.63 |       0.24 |    0.50 |     0.35 |       3.58 |  -0.15 |                 9 |         5.79 |           0.34 |
| Tatsugiri - 186/167         | SV06: Twilight Masquerade           |       20.10 |    0.96 |              0 |        0.68 |       0.19 |   -0.80 |     0.06 |     nan    |   0.68 |                 0 |         0.00 |           0.30 |
| Pikachu - 173/165           | SV: Scarlet & Violet 151            |       66.28 |    0.96 |              0 |        0.59 |       0.25 |   -0.16 |     0.06 |       2.50 | nan    |                 0 |        14.48 |           0.45 |
| Eevee ex - 167/131          | SV: Prismatic Evolutions            |      168.94 |    0.95 |              0 |        0.65 |       0.20 |   -0.28 |     0.16 |       1.54 |  -0.69 |                 0 |         2.47 |           0.40 |
| Shining Magikarp            | Celebrations: Classic Collection    |       32.33 |    0.95 |              0 |        0.58 |       0.25 |    0.52 |     0.14 |       3.64 |  -0.66 |                 0 |         2.15 |           0.32 |
| Ceruledge - 197/191         | SV08: Surging Sparks                |       21.77 |    0.94 |              0 |        0.76 |       0.17 |   -0.06 |     0.25 |       1.84 |   0.80 |                25 |         0.21 |           0.27 |
| Magby - 186/182             | SV04: Paradox Rift                  |       22.18 |    0.94 |              0 |        0.71 |       0.18 |   -0.03 |     0.18 |     nan    |   0.61 |                25 |         0.00 |           0.26 |
| Yveltal - 205/182           | SV04: Paradox Rift                  |       28.80 |    0.94 |              0 |        0.71 |       0.17 |   -0.11 |     0.20 |     nan    |   0.94 |                25 |         0.11 |           0.28 |
| Minior - 201/182            | SV04: Paradox Rift                  |       27.81 |    0.94 |              0 |        0.73 |       0.17 |   -0.10 |     0.14 |     nan    |   0.90 |                25 |         0.00 |           0.28 |
| Snorlax                     | SWSH11: Lost Origin Trainer Gallery |       22.40 |    0.94 |              0 |        0.56 |       0.21 |    0.37 |     0.31 |     nan    |  -0.04 |                25 |         1.72 |           0.32 |
| Mew ex - 232/091            | SV: Paldean Fates                   |      863.93 |    0.93 |              0 |        0.58 |       0.19 |   -0.20 |     0.17 |       1.32 |   1.46 |                25 |        18.23 |           0.41 |
| Charmander - 168/165        | SV: Scarlet & Violet 151            |       87.88 |    0.93 |              0 |        0.58 |       0.19 |   -0.68 |     0.15 |     nan    |   0.67 |                 0 |         0.54 |           0.36 |

## Tanie karty ($5–20)

Ta sama ocena co wyżej, dla tańszych kart (pełna lista w `reports/ranking_tanie.csv`). Przy takich kwotach wysyłka zjada dużą część zysku, więc to raczej lista na lata niż na szybki obrót.

| name                         | set_name                         |   price_now |   score |   dodruk_posty |   szansa_50 |   model_6m |   combo |   spread |   poke_pop |   rv_z |   weeks_since_low |   buzz_share |   model_net_6m |
|:-----------------------------|:---------------------------------|------------:|--------:|---------------:|------------:|-----------:|--------:|---------:|-----------:|-------:|------------------:|-------------:|---------------:|
| Cufant - 076/064             | SV: Shrouded Fable               |       15.25 |    0.99 |              0 |        0.84 |       0.24 |   -0.04 |     0.13 |     nan    |   0.28 |                25 |         0.00 |           0.32 |
| Fezandipiti                  | SV: Shrouded Fable               |       10.88 |    0.99 |              0 |        0.86 |       0.23 |    0.12 |     0.11 |       0.91 |  -0.21 |                25 |         0.00 |           0.27 |
| Umbreon V                    | SWSH07: Evolving Skies           |        8.45 |    0.98 |              0 |        0.77 |       0.35 |    1.36 |     0.50 |       3.58 |  -1.09 |                25 |         5.79 |           0.20 |
| Mew ex                       | Celebrations: Classic Collection |       15.54 |    0.98 |              0 |        0.76 |       0.32 |    0.45 |     0.13 |       2.32 |  -1.03 |                 0 |        18.23 |           0.34 |
| Meltan - 179/162             | SV05: Temporal Forces            |        6.33 |    0.98 |              0 |        0.81 |       0.23 |    0.52 |     0.39 |     nan    |  -1.00 |                25 |         0.00 |           0.02 |
| Gyarados VMAX                | SWSH07: Evolving Skies           |        8.48 |    0.98 |              0 |        0.74 |       0.35 |    0.40 |     0.24 |      -1.02 |  -1.09 |                25 |         0.86 |           0.14 |
| Venusaur                     | Celebrations: Classic Collection |       11.16 |    0.97 |              0 |        0.74 |       0.30 |    0.63 |     0.25 |       2.02 |  -1.19 |                10 |         1.39 |           0.24 |
| Chimecho - 179/167           | SV06: Twilight Masquerade        |        5.55 |    0.97 |              0 |        0.81 |       0.22 |    0.55 |     0.33 |     nan    |  -1.19 |                25 |         0.00 |          -0.09 |
| Flying Pikachu VMAX          | Celebrations                     |        5.55 |    0.97 |              1 |        0.72 |       0.30 |    0.26 |     0.30 |     nan    |  -1.42 |                 0 |         0.21 |          -0.11 |
| Fraxure - 077/064            | SV: Shrouded Fable               |       17.10 |    0.97 |              0 |        0.81 |       0.21 |   -0.20 |     0.20 |       0.72 |   0.45 |                25 |         0.00 |           0.32 |
| Gardevoir ex (Delta Species) | Celebrations: Classic Collection |        9.41 |    0.97 |              0 |        0.72 |       0.30 |    0.85 |     0.21 |       2.53 |  -1.28 |                23 |         0.32 |           0.22 |
| Surfing Pikachu VMAX         | Celebrations                     |        5.94 |    0.97 |              1 |        0.73 |       0.29 |    0.26 |     0.40 |     nan    |  -1.37 |                 0 |         0.21 |          -0.04 |
| Shiftry - 163/162            | SV05: Temporal Forces            |       10.39 |    0.97 |              0 |        0.79 |       0.22 |   -0.04 |     0.24 |     nan    |  -0.28 |                24 |         0.00 |           0.17 |
| Rayquaza VMAX                | SWSH07: Evolving Skies           |       13.15 |    0.97 |              0 |        0.72 |       0.29 |    1.18 |     0.27 |       2.92 |  -0.74 |                25 |         3.22 |           0.28 |
| Dipplin - 170/167            | SV06: Twilight Masquerade        |       11.86 |    0.97 |              0 |        0.80 |       0.21 |    0.13 |     0.20 |     nan    |  -0.09 |                25 |         0.00 |           0.23 |
| Pinsir - 168/167             | SV06: Twilight Masquerade        |       14.21 |    0.96 |              0 |        0.79 |       0.21 |    0.02 |     0.21 |     nan    |   0.18 |                25 |         0.00 |           0.28 |
| Milcery - 152/142            | SV07: Stellar Crown              |       15.87 |    0.96 |              0 |        0.79 |       0.21 |   -0.08 |     0.16 |     nan    |   0.34 |                25 |         0.00 |           0.29 |
| Reuniclus - 171/162          | SV05: Temporal Forces            |       15.59 |    0.96 |              0 |        0.79 |       0.21 |   -0.44 |     0.61 |     nan    |   0.31 |                20 |         0.00 |           0.24 |
| Mew V                        | SWSH03: Darkness Ablaze          |        6.20 |    0.96 |              0 |        0.70 |       0.28 |    1.21 |     0.33 |       1.87 |  -1.33 |                25 |        18.23 |          -0.03 |
| Pikachu VMAX                 | SWSH04: Vivid Voltage            |       12.23 |    0.96 |              0 |        0.67 |       0.29 |    0.80 |     0.31 |       2.33 |  -0.80 |                23 |        14.48 |           0.24 |

## Rynek: kiedy kupować

Trend rynku = mediana trendów cen wszystkich kart (%/mies.). Na historii szybki wzrost rynku zapowiadał słabsze kolejne miesiące, a spokojny lub spadający rynek – lepsze (korelacja rang poniżej; to tylko ok. 2 cykle, więc traktuj orientacyjnie).

|           |   zwrot_3m |   zwrot_6m |
|:----------|-----------:|-----------:|
| trend_90  |      -0.34 |      -0.48 |
| trend_180 |      -0.65 |      -0.48 |

Teraz (2026-10-18): trend 90 dni -2.3%/mies. (wyżej niż w 2% historii), trend 180 dni +2.1%/mies. (wyżej niż w 55% historii).

## Produkty zamknięte (booster box, ETB, bundle)

Ocena = ranga typu produktu (ETB i booster bundle wyżej) + bliskość wieku 1,5 roku od premiery + cena (droższe wyżej). Test: średni zwrot 10 najwyżej ocenionych produktów vs wszystkie, bez kosztów.

| horyzont   |   dat |    ic | top10   | wszystkie   | top10 ze stratą   | top: 1. / 2. połowa   |
|:-----------|------:|------:|:--------|:------------|:------------------|:----------------------|
| 6 mies.    |    57 | 0.226 | +52%    | +37%        | 3%                | +58% / +46%           |
| 12 mies.   |    44 | 0.315 | +143%   | +99%        | 0%                | +165% / +120%         |

Ranking na 2026-10-18 (produkty od $20, pełna lista w `reports/sealed_ranking.csv`):

| name                                                               | kind           | set_name                           | release_date   |   age_months |   price_now |   score |   cardmarket_eur |   dodruk_posty |
|:-------------------------------------------------------------------|:---------------|:-----------------------------------|:---------------|-------------:|------------:|--------:|-----------------:|---------------:|
| Paldean Fates Elite Trainer Box                                    | etb            | SV: Paldean Fates                  | 2024-01-26     |        32.72 |      430.62 |    0.75 |           207.30 |              0 |
| 151 Elite Trainer Box                                              | etb            | SV: Scarlet & Violet 151           | 2023-09-22     |        36.86 |      497.34 |    0.74 |           404.41 |              0 |
| Black Bolt Elite Trainer Box                                       | etb            | SV: Black Bolt                     | 2025-07-18     |        15.01 |      165.00 |    0.72 |           109.29 |              0 |
| White Flare Elite Trainer Box                                      | etb            | SV: White Flare                    | 2025-07-18     |        15.01 |      147.05 |    0.70 |           104.58 |              0 |
| Journey Together Elite Trainer Box                                 | etb            | SV09: Journey Together             | 2025-03-28     |        18.69 |      134.07 |    0.70 |            85.27 |              0 |
| Trick or Trade BOOster Bundle 2024 (120 ct)                        | booster_bundle | Trick or Trade BOOster Bundle 2024 | 2024-08-30     |        25.59 |      186.85 |    0.70 |           nan    |              0 |
| Stellar Crown Elite Trainer Box                                    | etb            | SV07: Stellar Crown                | 2024-09-13     |        25.13 |      159.80 |    0.69 |            94.95 |              0 |
| Crown Zenith Elite Trainer Box                                     | etb            | SWSH: Crown Zenith                 | 2023-01-20     |        44.91 |      322.86 |    0.67 |           255.41 |              0 |
| Destined Rivals Booster Box                                        | booster_box    | SV10: Destined Rivals              | 2025-05-30     |        16.62 |      403.55 |    0.66 |           293.04 |              2 |
| Obsidian Flames Elite Trainer Box                                  | etb            | SV03: Obsidian Flames              | 2023-08-11     |        38.24 |      272.32 |    0.66 |           206.22 |              0 |
| Destined Rivals Elite Trainer Box                                  | etb            | SV10: Destined Rivals              | 2025-05-30     |        16.62 |      112.86 |    0.66 |           123.52 |              2 |
| Prismatic Evolutions Elite Trainer Box                             | etb            | SV: Prismatic Evolutions           | 2025-01-17     |        20.99 |      120.28 |    0.66 |           149.90 |              0 |
| Paldean Fates Booster Bundle                                       | booster_bundle | SV: Paldean Fates                  | 2024-01-26     |        32.72 |      180.34 |    0.65 |           131.70 |              0 |
| Evolving Skies Elite Trainer Box [Flareon/Jolteon/Umbreon/Leafeon] | etb            | SWSH07: Evolving Skies             | 2021-08-27     |        61.70 |      568.05 |    0.65 |           nan    |              0 |
| Trick or Trade BOOster Bundle 2023 (120 ct)                        | booster_bundle | Trick or Trade BOOster Bundle 2023 | 2023-09-01     |        37.55 |      191.98 |    0.64 |           nan    |              0 |

## Kontrola na żywo

Każdy przebieg zapisuje top-20 do `reports/picks_log.csv`; po 3 i 6 mies. liczymy, jak wypadły.

Zapisane dni z wyborami: 1. Pierwsze wyniki po 3 mies. od 2026-10-18.
