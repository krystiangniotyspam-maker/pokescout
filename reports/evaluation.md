# PokeScout – test przewidywań na historii

Dane: 137 dni notowań, 4777 kart w katalogu; panel 77081 obserwacji (2024-08-11 – 2026-10-18, co 2 tygodnie).

**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, 0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. `top_excess` = średni zwrot 20 najwyżej ocenionych kart ponad medianę rynku, `top_hit_rate` = jaki odsetek z nich pobił rynek, `top_net` = ich średni zwrot netto po kosztach (prowizja 13% i wysyłka $1,5 w każdą stronę) – realny zysk, nie ponad rynek, `top_up50` = jaki odsetek z nich zdrożał o 50% lub więcej.

## Horyzont 3 mies.

Daty z wynikiem: 51. Karty, które przeszły bramki modułu A: 200 obserwacji, średni zwrot ponad rynek +1.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: gradient boosting                  |      39 |  0.31  |        4.3 | +5.9%        | 62%            | -19.1%    | 0.111538   |
| łącznie: model + ocena C                  |      39 |  0.295 |        7   | +11.3%       | 68%            | -16.7%    | 0.133333   |
| ranking: szansa na +50% + model zwrotu    |      39 |  0.273 |        3.5 | +6.7%        | 60%            | -21.4%    | 0.146154   |
| model: szansa na wzrost o 50%+            |      39 |  0.179 |        2.1 | +6.7%        | 59%            | -23.3%    | 0.169231   |
| ocena C: popularność + wiek + tania + dno |      51 |  0.174 |        3   | +13.5%       | 69%            | -14.7%    | 0.173529   |
| cecha: age_months                         |      51 |  0.156 |        1.4 | +10.5%       | 65%            | -7.9%     | 0.101961   |
| cecha: poke_pop                           |      51 |  0.151 |        3   | +9.0%        | 62%            | -5.8%     | 0.15       |
| model: ridge na rangach                   |      39 |  0.15  |        1.9 | +10.8%       | 70%            | -10.9%    | 0.125641   |
| cecha: tier_score                         |      51 |  0.145 |        2.7 | -3.7%        | 42%            | -16.5%    | 0.112745   |
| cecha: range_pos_180                      |      51 |  0.131 |        3.2 | -0.0%        | 50%            | -21.8%    | 0.148039   |
| model: gradient boosting, cel zysk netto  |      39 |  0.116 |        2.3 | +6.8%        | 66%            | -4.3%     | 0.074359   |
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
| reguły: moduł A (ocena bez bramek)        |      51 |  0.051 |        0.9 | +4.2%        | 52%            | -16.4%    | 0.138235   |
| cecha: slope_90                           |      51 |  0.036 |        0.7 | -16.6%       | 28%            | -34.5%    | 0.0735294  |
| cecha: buzz_growth                        |      51 |  0.035 |        2.4 | +2.7%        | 53%            | -21.8%    | 0.110784   |
| cecha: special                            |      51 |  0.032 |        0.8 | -10.0%       | 32%            | -29.7%    | 0.10098    |
| cecha: above_low                          |      51 |  0.031 |        0.5 | -16.5%       | 30%            | -34.2%    | 0.0803922  |
| cecha: sealed_slope_90                    |      51 |  0.023 |        0.4 | -3.2%        | 43%            | -25.9%    | 0.0529412  |
| cecha: new_same_poke_90                   |      51 |  0.006 |        0.3 | +0.0%        | 50%            | -19.9%    | 0.112745   |
| cecha: slope_180                          |      51 | -0     |       -0   | -13.4%       | 31%            | -30.4%    | 0.0843137  |
| cecha: new_same_poke_365                  |      51 | -0.005 |       -0.3 | -6.3%        | 31%            | -27.0%    | 0.0735294  |
| cecha: logp                               |      51 | -0.023 |       -0.7 | +0.1%        | 50%            | -5.1%     | 0.0745098  |
| cecha: set_rel                            |      51 | -0.023 |       -0.7 | +1.8%        | 51%            | -3.5%     | 0.0941176  |
| cecha: −slope_90                          |      51 | -0.036 |       -0.7 | -15.4%       | 24%            | -41.2%    | 0.0294118  |
| cecha: rv_z                               |      51 | -0.064 |       -3.3 | +0.2%        | 50%            | -9.1%     | 0.0754902  |
| cecha: spread                             |      51 | -0.071 |       -2.3 | -3.6%        | 45%            | -37.9%    | 0.0990196  |
| cecha: drawdown                           |      51 | -0.092 |       -1.5 | -4.6%        | 39%            | -34.2%    | 0.0901961  |
| cecha: rarity_w                           |      51 | -0.092 |       -1.6 | -19.1%       | 12%            | -28.2%    | 0.00980392 |
| cecha: −range_pos_180                     |      51 | -0.131 |       -3.2 | -14.9%       | 24%            | -35.4%    | 0.027451   |
| cecha: history_complete                   |      51 | -0.157 |       -2.6 | -18.9%       | 20%            | -38.5%    | 0.0529412  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: gradient boosting                  |      39 | 0.384 |        5   | +6.5%        | 64%            | -6.5%     |  0.0858974 |
| łącznie: model + ocena C                  |      39 | 0.354 |        5.7 | +11.2%       | 66%            | -2.9%     |  0.114103  |
| ranking: szansa na +50% + model zwrotu    |      39 | 0.343 |        4.5 | +7.8%        | 60%            | -5.2%     |  0.139744  |
| model: gradient boosting, cel zysk netto  |      39 | 0.329 |        4.4 | +6.4%        | 66%            | -4.1%     |  0.0717949 |
| model: szansa na wzrost o 50%+            |      39 | 0.201 |        2.2 | +8.4%        | 61%            | -4.7%     |  0.15641   |
| ocena C: popularność + wiek + tania + dno |      51 | 0.196 |        2.5 | +7.7%        | 60%            | -3.7%     |  0.108824  |
| reguły: moduł A (ocena bez bramek)        |      51 | 0.098 |        1.4 | +4.9%        | 53%            | -4.6%     |  0.141176  |
| reguły: moduł B1 (tania vs podobne)       |      51 | 0.016 |        0.6 | +3.2%        | 50%            | -8.1%     |  0.133333  |

Stabilność (3 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |      13 | 0.309 |        3.4 | +22.6%       | 77%            | -13.4%    |  0.2       |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      25 | 0.241 |        3.1 | +24.2%       | 83%            | -6.4%     |  0.272     |
| 1. połowa (od 2024-08) | model: gradient boosting                  |      13 | 0.155 |        0.9 | -1.3%        | 44%            | -31.9%    |  0.0846154 |
| 1. połowa (od 2024-08) | ranking: szansa na +50% + model zwrotu    |      13 | 0.139 |        0.8 | +4.0%        | 49%            | -28.3%    |  0.169231  |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      25 | 0.103 |        1.1 | -5.4%        | 45%            | -28.3%    |  0.124     |
| 1. połowa (od 2024-08) | model: szansa na wzrost o 50%+            |      13 | 0.098 |        0.6 | +4.7%        | 51%            | -28.9%    |  0.165385  |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      25 | 0.089 |        4.9 | +10.0%       | 61%            | -28.3%    |  0.168     |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      25 | 0.081 |        0.9 | +7.9%        | 59%            | -11.4%    |  0.18      |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      25 | 0.079 |        1.9 | +1.3%        | 48%            | -23.4%    |  0.146     |
| 2. połowa (od 2025-07) | model: gradient boosting                  |      26 | 0.388 |       14.1 | +9.6%        | 70%            | -12.7%    |  0.125     |
| 2. połowa (od 2025-07) | ranking: szansa na +50% + model zwrotu    |      26 | 0.34  |        6.1 | +8.1%        | 66%            | -17.9%    |  0.134615  |
| 2. połowa (od 2025-07) | łącznie: model + ocena C                  |      26 | 0.288 |        6.3 | +6.1%        | 63%            | -18.3%    |  0.1       |
| 2. połowa (od 2025-07) | model: szansa na wzrost o 50%+            |      26 | 0.219 |        2.5 | +7.8%        | 64%            | -20.5%    |  0.171154  |
| 2. połowa (od 2025-07) | ocena C: popularność + wiek + tania + dno |      26 | 0.111 |        1.5 | +4.0%        | 55%            | -22.6%    |  0.0788462 |
| 2. połowa (od 2025-07) | cecha: weeks_since_low                    |      26 | 0.094 |        3.1 | +2.0%        | 54%            | -20.0%    |  0.146154  |
| 2. połowa (od 2025-07) | cecha: −drawdown                          |      26 | 0.081 |        1.1 | +6.9%        | 58%            | -12.5%    |  0.209615  |
| 2. połowa (od 2025-07) | reguły: moduł B1 (tania vs podobne)       |      26 | 0.041 |        1.3 | -1.4%        | 44%            | -34.1%    |  0.0615385 |
| 2. połowa (od 2025-07) | reguły: moduł A (ocena bez bramek)        |      26 | 0.022 |        0.3 | +0.7%        | 46%            | -21.1%    |  0.0980769 |

## Horyzont 6 mies.

Daty z wynikiem: 45. Karty, które przeszły bramki modułu A: 133 obserwacji, średni zwrot ponad rynek -2.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      27 |  0.277 |        3.6 | +12.8%       | 66%            | -4.8%     |  0.344444  |
| model: szansa na wzrost o 50%+            |      27 |  0.265 |        3.3 | +12.5%       | 65%            | -5.6%     |  0.35      |
| model: gradient boosting                  |      27 |  0.258 |        3.3 | +9.7%        | 58%            | -7.3%     |  0.314815  |
| łącznie: model + ocena C                  |      27 |  0.246 |        2.3 | +12.3%       | 65%            | -5.7%     |  0.318519  |
| ocena C: popularność + wiek + tania + dno |      45 |  0.232 |        2.2 | +27.9%       | 74%            | +12.0%    |  0.426667  |
| cecha: poke_pop                           |      45 |  0.217 |        2.7 | +17.6%       | 66%            | +14.1%    |  0.354444  |
| cecha: tier_score                         |      45 |  0.201 |        2.3 | -6.4%        | 42%            | -8.1%     |  0.214444  |
| cecha: age_months                         |      45 |  0.176 |        1   | +20.4%       | 66%            | +14.4%    |  0.336667  |
| model: gradient boosting, cel zysk netto  |      27 |  0.166 |        1.8 | +8.5%        | 57%            | +5.9%     |  0.251852  |
| cecha: buzz_eng                           |      45 |  0.153 |        1.9 | +4.5%        | 58%            | -4.2%     |  0.254444  |
| cecha: buzz_share                         |      45 |  0.149 |        1.9 | +3.6%        | 56%            | -5.3%     |  0.246667  |
| cecha: weeks_since_low                    |      45 |  0.148 |        3.5 | +1.1%        | 51%            | -10.4%    |  0.304444  |
| model: ridge na rangach                   |      27 |  0.125 |        0.9 | +17.6%       | 68%            | +6.0%     |  0.357407  |
| cecha: range_pos_180                      |      45 |  0.123 |        2.5 | -3.7%        | 48%            | -13.6%    |  0.275556  |
| cecha: slope_180                          |      45 |  0.096 |        1.5 | -17.6%       | 35%            | -23.4%    |  0.167778  |
| cecha: −drawdown                          |      45 |  0.086 |        1   | -4.7%        | 47%            | -14.1%    |  0.272222  |
| cecha: above_low                          |      45 |  0.077 |        0.9 | -22.0%       | 33%            | -27.5%    |  0.162222  |
| cecha: special                            |      45 |  0.071 |        1.1 | -9.7%        | 41%            | -16.8%    |  0.282222  |
| cecha: −rv_z                              |      45 |  0.069 |        3.1 | +8.0%        | 54%            | -17.5%    |  0.298889  |
| reguły: moduł B1 (tania vs podobne)       |      45 |  0.069 |        3.1 | +8.0%        | 54%            | -17.5%    |  0.298889  |
| reguły: moduł A (ocena bez bramek)        |      45 |  0.058 |        0.8 | +7.5%        | 58%            | -2.3%     |  0.314444  |
| cecha: vol_ratio                          |      45 |  0.051 |        1.2 | -1.2%        | 46%            | -13.4%    |  0.211111  |
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
| cecha: spread                             |      45 | -0.054 |       -1.2 | -4.2%        | 47%            | -27.4%    |  0.226667  |
| cecha: rv_z                               |      45 | -0.069 |       -3.1 | +1.3%        | 53%            | +3.0%     |  0.195556  |
| cecha: drawdown                           |      45 | -0.086 |       -1   | -10.1%       | 38%            | -27.9%    |  0.187778  |
| cecha: rarity_w                           |      45 | -0.116 |       -1.5 | -30.4%       | 5%             | -31.9%    |  0.0122222 |
| cecha: −range_pos_180                     |      45 | -0.123 |       -2.5 | -20.8%       | 23%            | -31.0%    |  0.0966667 |
| cecha: history_complete                   |      45 | -0.17  |       -1.7 | -28.1%       | 19%            | -37.3%    |  0.0988889 |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ocena C: popularność + wiek + tania + dno |      45 | 0.271 |        2.1 | +15.7%       | 62%            | +16.2%    |   0.331111 |
| łącznie: model + ocena C                  |      27 | 0.269 |        1.9 | +2.8%        | 51%            | +1.3%     |   0.172222 |
| ranking: szansa na +50% + model zwrotu    |      27 | 0.258 |        2.6 | +7.9%        | 60%            | +6.5%     |   0.225926 |
| model: gradient boosting                  |      27 | 0.257 |        2.4 | +5.0%        | 54%            | +3.2%     |   0.205556 |
| model: gradient boosting, cel zysk netto  |      27 | 0.239 |        2.3 | +5.2%        | 54%            | +5.3%     |   0.192593 |
| model: szansa na wzrost o 50%+            |      27 | 0.222 |        2.5 | +8.4%        | 61%            | +8.1%     |   0.222222 |
| reguły: moduł A (ocena bez bramek)        |      45 | 0.096 |        0.9 | +6.7%        | 56%            | +8.4%     |   0.304444 |
| reguły: moduł B1 (tania vs podobne)       |      45 | 0.024 |        0.4 | +8.1%        | 56%            | +8.9%     |   0.314444 |

Stabilność (6 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |       4 | 0.435 |        5.8 | +50.6%       | 98%            | +9.1%     |   0.5375   |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      22 | 0.369 |        3.4 | +53.8%       | 89%            | +33.0%    |   0.620455 |
| 1. połowa (od 2024-08) | model: gradient boosting                  |       4 | 0.184 |        1.7 | +12.1%       | 56%            | -25.7%    |   0.225    |
| 1. połowa (od 2024-08) | ranking: szansa na +50% + model zwrotu    |       4 | 0.181 |        2.2 | +14.9%       | 56%            | -22.0%    |   0.3125   |
| 1. połowa (od 2024-08) | model: szansa na wzrost o 50%+            |       4 | 0.171 |        2.2 | +14.4%       | 56%            | -20.7%    |   0.275    |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      22 | 0.164 |        2.4 | -4.8%        | 42%            | -18.1%    |   0.247727 |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      22 | 0.123 |        0.9 | -15.4%       | 33%            | -28.5%    |   0.186364 |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      22 | 0.097 |        3.4 | +18.0%       | 60%            | -11.9%    |   0.377273 |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      22 | 0.074 |        0.5 | +13.9%       | 62%            | +6.3%     |   0.393182 |
| 2. połowa (od 2025-06) | ranking: szansa na +50% + model zwrotu    |      23 | 0.294 |        3.5 | +12.4%       | 67%            | -1.8%     |   0.35     |
| 2. połowa (od 2025-06) | model: szansa na wzrost o 50%+            |      23 | 0.282 |        3.3 | +12.2%       | 66%            | -3.0%     |   0.363043 |
| 2. połowa (od 2025-06) | model: gradient boosting                  |      23 | 0.27  |        3.1 | +9.3%        | 59%            | -4.1%     |   0.330435 |
| 2. połowa (od 2025-06) | łącznie: model + ocena C                  |      23 | 0.213 |        2   | +6.7%        | 59%            | -8.2%     |   0.280435 |
| 2. połowa (od 2025-06) | cecha: weeks_since_low                    |      23 | 0.133 |        2.7 | +7.1%        | 60%            | -3.1%     |   0.358696 |
| 2. połowa (od 2025-06) | ocena C: popularność + wiek + tania + dno |      23 | 0.101 |        0.9 | +7.3%        | 60%            | -8.0%     |   0.241304 |
| 2. połowa (od 2025-06) | cecha: −drawdown                          |      23 | 0.051 |        0.5 | +6.8%        | 59%            | -0.3%     |   0.354348 |
| 2. połowa (od 2025-06) | reguły: moduł A (ocena bez bramek)        |      23 | 0.043 |        0.6 | +1.7%        | 54%            | -10.5%    |   0.23913  |
| 2. połowa (od 2025-06) | reguły: moduł B1 (tania vs podobne)       |      23 | 0.043 |        2.4 | -0.7%        | 48%            | -22.8%    |   0.223913 |

## Horyzont 12 mies.

Daty z wynikiem: 32. Karty, które przeszły bramki modułu A: 42 obserwacji, średni zwrot ponad rynek +21.8%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: szansa na wzrost o 50%+            |      14 |  0.439 |        2.4 | +38.9%       | 82%            | +46.8%    |  0.717857  |
| ranking: szansa na +50% + model zwrotu    |      14 |  0.436 |        2.8 | +37.0%       | 79%            | +46.2%    |  0.689286  |
| model: gradient boosting                  |      14 |  0.386 |        2.9 | +33.5%       | 74%            | +42.5%    |  0.635714  |
| ocena C: popularność + wiek + tania + dno |      32 |  0.341 |        2.2 | +55.4%       | 81%            | +64.9%    |  0.715625  |
| łącznie: model + ocena C                  |      14 |  0.339 |        2.2 | +34.9%       | 81%            | +39.9%    |  0.696429  |
| cecha: poke_pop                           |      32 |  0.327 |        3.4 | +37.8%       | 76%            | +60.1%    |  0.646875  |
| cecha: tier_score                         |      32 |  0.325 |        2.7 | -1.3%        | 48%            | +16.3%    |  0.370312  |
| model: gradient boosting, cel zysk netto  |      14 |  0.293 |        1.8 | +27.3%       | 72%            | +52.7%    |  0.628571  |
| cecha: age_months                         |      32 |  0.273 |        1.3 | +48.5%       | 84%            | +66.0%    |  0.753125  |
| model: ridge na rangach                   |      14 |  0.259 |        1.1 | +35.1%       | 76%            | +51.4%    |  0.675     |
| cecha: buzz_eng                           |      32 |  0.259 |        2.6 | +14.8%       | 65%            | +24.3%    |  0.478125  |
| cecha: buzz_share                         |      32 |  0.255 |        2.6 | +13.8%       | 65%            | +22.8%    |  0.460938  |
| cecha: weeks_since_low                    |      32 |  0.196 |        2.4 | -4.3%        | 48%            | -0.4%     |  0.385937  |
| cecha: range_pos_180                      |      32 |  0.152 |        1.4 | -15.8%       | 39%            | -10.4%    |  0.292188  |
| cecha: −drawdown                          |      32 |  0.14  |        1   | -18.7%       | 37%            | -13.1%    |  0.28125   |
| cecha: slope_180                          |      32 |  0.121 |        1.1 | -25.8%       | 29%            | -17.6%    |  0.192188  |
| reguły: moduł A (ocena bez bramek)        |      32 |  0.119 |        1   | +17.8%       | 66%            | +30.2%    |  0.56875   |
| cecha: above_low                          |      32 |  0.092 |        1.1 | -30.2%       | 31%            | -20.9%    |  0.229687  |
| reguły: moduł B1 (tania vs podobne)       |      32 |  0.092 |        2.8 | +20.5%       | 67%            | +13.2%    |  0.571875  |
| cecha: −rv_z                              |      32 |  0.092 |        2.8 | +20.5%       | 67%            | +13.2%    |  0.571875  |
| cecha: slope_30                           |      32 |  0.076 |        0.8 | -28.0%       | 31%            | -19.5%    |  0.235938  |
| cecha: special                            |      32 |  0.066 |        1.1 | -22.4%       | 31%            | -15.9%    |  0.221875  |
| cecha: slope_60                           |      32 |  0.064 |        0.6 | -32.6%       | 28%            | -23.2%    |  0.192188  |
| cecha: slope_90                           |      32 |  0.057 |        0.5 | -30.6%       | 27%            | -21.5%    |  0.182813  |
| cecha: vol_ratio                          |      32 |  0.045 |        0.5 | -1.5%        | 45%            | +3.2%     |  0.346875  |
| cecha: buzz_growth                        |      32 |  0.044 |        0.6 | +7.4%        | 57%            | +12.4%    |  0.409375  |
| cecha: logp                               |      32 |  0.041 |        0.4 | +2.4%        | 48%            | +26.5%    |  0.351562  |
| cecha: set_trend_90                       |      32 |  0.039 |        0.3 | -5.6%        | 43%            | -4.6%     |  0.282813  |
| cecha: set_rel                            |      32 | -0.003 |       -0.1 | +1.0%        | 44%            | +22.2%    |  0.320312  |
| cecha: new_same_poke_90                   |      32 | -0.005 |       -0.1 | -13.2%       | 38%            | -6.1%     |  0.315625  |
| cecha: new_same_poke_365                  |      32 | -0.012 |       -0.3 | -16.4%       | 34%            | -1.4%     |  0.289062  |
| cecha: sealed_slope_90                    |      32 | -0.015 |       -0.1 | -7.5%        | 42%            | -4.9%     |  0.304688  |
| cecha: spread                             |      32 | -0.031 |       -0.5 | -6.7%        | 46%            | -12.5%    |  0.371875  |
| cecha: −slope_90                          |      32 | -0.057 |       -0.5 | -31.3%       | 27%            | -31.2%    |  0.201562  |
| cecha: rv_z                               |      32 | -0.092 |       -2.8 | -3.5%        | 47%            | +15.3%    |  0.325     |
| cecha: drawdown                           |      32 | -0.14  |       -1   | -19.2%       | 37%            | -17.1%    |  0.310937  |
| cecha: −range_pos_180                     |      32 | -0.152 |       -1.4 | -34.4%       | 17%            | -32.9%    |  0.107813  |
| cecha: rarity_w                           |      32 | -0.16  |       -1.9 | -44.3%       | 1%             | -38.0%    |  0.0078125 |
| cecha: history_complete                   |      32 | -0.232 |       -2.5 | -38.7%       | 20%            | -36.1%    |  0.140625  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      14 | 0.421 |        2.8 | +25.0%       | 74%            | +52.4%    |   0.625    |
| model: szansa na wzrost o 50%+            |      14 | 0.403 |        2.3 | +22.5%       | 72%            | +50.3%    |   0.617857 |
| ocena C: popularność + wiek + tania + dno |      32 | 0.399 |        2.4 | +36.3%       | 79%            | +58.5%    |   0.682813 |
| model: gradient boosting                  |      14 | 0.373 |        2.7 | +19.7%       | 68%            | +45.4%    |   0.578571 |
| łącznie: model + ocena C                  |      14 | 0.338 |        2.1 | +12.2%       | 63%            | +33.5%    |   0.5      |
| model: gradient boosting, cel zysk netto  |      14 | 0.332 |        2.8 | +17.3%       | 68%            | +43.8%    |   0.557143 |
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
| 2. połowa (od 2025-03) | model: szansa na wzrost o 50%+            |      14 | 0.439 |        2.4 | +38.9%       | 82%            | +46.8%    |   0.717857 |
| 2. połowa (od 2025-03) | ranking: szansa na +50% + model zwrotu    |      14 | 0.436 |        2.8 | +37.0%       | 79%            | +46.2%    |   0.689286 |
| 2. połowa (od 2025-03) | model: gradient boosting                  |      14 | 0.386 |        2.9 | +33.5%       | 74%            | +42.5%    |   0.635714 |
| 2. połowa (od 2025-03) | łącznie: model + ocena C                  |      14 | 0.339 |        2.2 | +34.9%       | 81%            | +39.9%    |   0.696429 |
| 2. połowa (od 2025-03) | ocena C: popularność + wiek + tania + dno |      16 | 0.21  |        1.1 | +23.0%       | 72%            | +25.4%    |   0.584375 |
| 2. połowa (od 2025-03) | cecha: weeks_since_low                    |      16 | 0.18  |        1.1 | +0.8%        | 52%            | +6.3%     |   0.45625  |
| 2. połowa (od 2025-03) | reguły: moduł A (ocena bez bramek)        |      16 | 0.158 |        1   | +11.9%       | 64%            | +19.4%    |   0.575    |
| 2. połowa (od 2025-03) | reguły: moduł B1 (tania vs podobne)       |      16 | 0.065 |        3.3 | +13.6%       | 67%            | +9.0%     |   0.59375  |
| 2. połowa (od 2025-03) | cecha: −drawdown                          |      16 | 0.032 |        0.2 | -18.0%       | 40%            | -6.2%     |   0.3375   |

## Bieżący ranking modelu (6 mies., karty od $20)

Stan na 2026-10-18. Kolejność wg `score` (0–1, wyżej = lepiej) = średnia rang modelu szukającego kart, które zdrożeją o 50%+ (`szansa_50`), i modelu zwrotu (`model_6m`); w teście ta para najlepiej wybierała karty na rok (sekcja 12 mies.). Z jednego setu najwyżej 3 karty na początku listy, kolejne trafiają niżej. `szansa_50` porządkuje karty, ale nie jest prawdziwym prawdopodobieństwem – faktyczny odsetek wzrostów o 50%+ zależy głównie od stanu całego rynku. `model_6m` = przewidywany log-zwrot ponad rynek w 6 mies. (0,20 ≈ +22%), `model_net_6m` = to samo po kosztach, `spread` = log(cena rynkowa / najniższa oferta). To lista do sprawdzenia, nie rekomendacja zakupu.

| name                        | set_name                            |   price_now |   score |   szansa_50 |   model_6m |   combo |   spread |   poke_pop |   rv_z |   weeks_since_low |   buzz_share |   model_net_6m |
|:----------------------------|:------------------------------------|------------:|--------:|------------:|-----------:|--------:|---------:|-----------:|-------:|------------------:|-------------:|---------------:|
| Cresselia - 071/064         | SV: Shrouded Fable                  |       27.48 |    0.99 |        0.87 |       0.24 |   -0.27 |     0.14 |     nan    |   1.15 |                25 |         0.32 |           0.38 |
| Zorua - 075/064             | SV: Shrouded Fable                  |       22.75 |    0.99 |        0.87 |       0.23 |   -0.23 |     0.13 |       1.00 |   0.87 |                25 |         0.43 |           0.34 |
| Lickitung - 180/162         | SV05: Temporal Forces               |       28.48 |    0.98 |        0.82 |       0.22 |   -0.23 |     0.16 |     nan    |   1.20 |                25 |         0.21 |           0.32 |
| Eevee - 188/167             | SV06: Twilight Masquerade           |       69.06 |    0.98 |        0.74 |       0.26 |   -0.26 |     0.00 |       2.44 |  -0.05 |                 0 |         2.47 |           0.48 |
| Arbok - 176/162             | SV05: Temporal Forces               |       28.91 |    0.98 |        0.77 |       0.21 |   -0.24 |     0.11 |     nan    |   1.22 |                25 |         0.00 |           0.33 |
| Hisuian Growlithe - 181/167 | SV06: Twilight Masquerade           |       26.49 |    0.98 |        0.79 |       0.20 |   -0.24 |     0.14 |     nan    |   1.09 |                25 |         0.11 |           0.32 |
| Litten - 167/162            | SV05: Temporal Forces               |       38.48 |    0.97 |        0.80 |       0.20 |   -0.31 |     0.12 |     nan    |   1.64 |                25 |         0.00 |           0.33 |
| ______'s Pikachu            | Celebrations: Classic Collection    |       30.47 |    0.97 |        0.68 |       0.26 |    0.22 |     0.10 |     nan    |  -0.69 |                 9 |         0.00 |           0.31 |
| Houndoom - 066/064          | SV: Shrouded Fable                  |       56.97 |    0.97 |        0.86 |       0.19 |   -0.83 |     0.13 |      -0.51 |   2.22 |                25 |         0.54 |           0.36 |
| Espeon V (Full Art)         | SWSH07: Evolving Skies              |       25.93 |    0.96 |        0.67 |       0.22 |    0.68 |     0.12 |       2.96 |  -0.21 |                24 |         1.39 |           0.34 |
| Tatsugiri - 186/167         | SV06: Twilight Masquerade           |       20.24 |    0.96 |        0.72 |       0.20 |   -0.81 |     0.08 |     nan    |   0.70 |                 0 |         0.00 |           0.31 |
| Latios - 203/191            | SV08: Surging Sparks                |       28.94 |    0.96 |        0.65 |       0.23 |   -0.80 |     0.19 |     nan    |   0.49 |                 0 |         0.75 |           0.36 |
| Umbreon VMAX                | SWSH07: Evolving Skies              |       27.93 |    0.96 |        0.63 |       0.24 |    0.50 |     0.22 |       3.58 |  -0.15 |                 9 |         5.79 |           0.35 |
| Espeon ex - 155/131         | SV: Prismatic Evolutions            |      284.67 |    0.95 |        0.75 |       0.18 |    0.15 |     0.16 |       2.96 |   0.00 |                24 |         1.39 |           0.43 |
| Pikachu ex - 219/191        | SV08: Surging Sparks                |       27.02 |    0.95 |        0.63 |       0.21 |   -0.42 |     0.26 |       2.34 |   0.14 |                 0 |        14.48 |           0.36 |
| Shining Magikarp            | Celebrations: Classic Collection    |       32.43 |    0.95 |        0.58 |       0.26 |    0.51 |     0.15 |       3.64 |  -0.66 |                 0 |         2.15 |           0.32 |
| Pikachu - 173/165           | SV: Scarlet & Violet 151            |       66.09 |    0.95 |        0.57 |       0.27 |   -0.17 |     0.05 |       2.51 | nan    |                 0 |        14.48 |           0.46 |
| Magby - 186/182             | SV04: Paradox Rift                  |       22.17 |    0.95 |        0.71 |       0.18 |   -0.03 |     0.18 |     nan    |   0.63 |                25 |         0.00 |           0.26 |
| Eevee ex - 167/131          | SV: Prismatic Evolutions            |      170.27 |    0.95 |        0.63 |       0.20 |   -0.30 |     0.17 |       1.53 |  -0.67 |                 0 |         2.47 |           0.42 |
| Scolipede - 134/086         | SV: Black Bolt                      |       25.78 |    0.94 |        0.60 |       0.20 |   -0.41 |     0.08 |     nan    |   1.05 |                25 |         0.00 |           0.26 |
| Aipom - 211/182             | SV04: Paradox Rift                  |       28.20 |    0.94 |        0.74 |       0.18 |   -0.11 |     0.12 |     nan    |   0.94 |                25 |         0.00 |           0.27 |
| Ceruledge - 197/191         | SV08: Surging Sparks                |       21.85 |    0.94 |        0.77 |       0.17 |   -0.07 |     0.22 |       1.84 |   0.81 |                25 |         0.21 |           0.29 |
| Yveltal - 205/182           | SV04: Paradox Rift                  |       29.01 |    0.94 |        0.73 |       0.17 |   -0.12 |     0.21 |     nan    |   0.98 |                25 |         0.11 |           0.28 |
| Umbreon Star                | Celebrations: Classic Collection    |       75.76 |    0.93 |        0.56 |       0.23 |    0.37 |     0.06 |       4.24 |  -0.24 |                 0 |         5.79 |           0.40 |
| Snorlax                     | SWSH11: Lost Origin Trainer Gallery |       22.37 |    0.93 |        0.56 |       0.21 |    0.37 |     0.31 |     nan    |  -0.04 |                25 |         1.72 |           0.31 |

## Rynek: kiedy kupować

Trend rynku = mediana trendów cen wszystkich kart (%/mies.). Na historii szybki wzrost rynku zapowiadał słabsze kolejne miesiące, a spokojny lub spadający rynek – lepsze (korelacja rang poniżej; to tylko ok. 2 cykle, więc traktuj orientacyjnie).

|           |   zwrot_3m |   zwrot_6m |
|:----------|-----------:|-----------:|
| trend_90  |      -0.34 |      -0.48 |
| trend_180 |      -0.65 |      -0.48 |

Teraz (2026-10-18): trend 90 dni -2.2%/mies. (wyżej niż w 3% historii), trend 180 dni +2.1%/mies. (wyżej niż w 55% historii).

## Kontrola na żywo

Każdy przebieg zapisuje top-20 do `reports/picks_log.csv`; po 3 i 6 mies. liczymy, jak wypadły.

Zapisane dni z wyborami: 1. Pierwsze wyniki po 3 mies. od 2026-10-18.
