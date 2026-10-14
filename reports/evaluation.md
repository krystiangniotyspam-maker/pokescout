# PokeScout – test przewidywań na historii

Dane: 137 dni notowań, 4777 kart w katalogu; panel 77081 obserwacji (2024-08-11 – 2026-10-18, co 2 tygodnie).

**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, 0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. `top_excess` = średni zwrot 20 najwyżej ocenionych kart ponad medianę rynku, `top_hit_rate` = jaki odsetek z nich pobił rynek, `top_net` = ich średni zwrot netto po kosztach (prowizja 13% i wysyłka $1,5 w każdą stronę) – realny zysk, nie ponad rynek, `top_up50` = jaki odsetek z nich zdrożał o 50% lub więcej.

## Horyzont 3 mies.

Daty z wynikiem: 51. Karty, które przeszły bramki modułu A: 200 obserwacji, średni zwrot ponad rynek +1.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: gradient boosting                  |      39 |  0.29  |        3.8 | +8.6%        | 66%            | -17.2%    | 0.141026   |
| łącznie: model + ocena C                  |      39 |  0.281 |        5.7 | +12.7%       | 69%            | -16.4%    | 0.146154   |
| ranking: szansa na +50% + model zwrotu    |      39 |  0.263 |        3.3 | +9.5%        | 64%            | -18.5%    | 0.182051   |
| model: szansa na wzrost o 50%+            |      39 |  0.178 |        2.2 | +8.4%        | 61%            | -20.9%    | 0.185897   |
| ocena C: popularność + wiek + tania + dno |      51 |  0.166 |        2.8 | +13.8%       | 69%            | -14.4%    | 0.179412   |
| cecha: age_months                         |      51 |  0.148 |        1.4 | +11.2%       | 66%            | -9.5%     | 0.118627   |
| model: ridge na rangach                   |      39 |  0.143 |        1.8 | +11.1%       | 72%            | -12.7%    | 0.132051   |
| cecha: range_pos_180                      |      51 |  0.141 |        3.3 | +2.2%        | 52%            | -21.4%    | 0.169608   |
| cecha: tier_score                         |      51 |  0.133 |        2.5 | -6.7%        | 37%            | -19.7%    | 0.0921569  |
| cecha: poke_pop                           |      51 |  0.115 |        2.1 | +9.1%        | 62%            | -6.1%     | 0.154902   |
| cecha: slope_30                           |      51 |  0.111 |        2.3 | -12.7%       | 35%            | -32.0%    | 0.109804   |
| cecha: −drawdown                          |      51 |  0.105 |        1.7 | +2.3%        | 53%            | -20.3%    | 0.179412   |
| cecha: buzz_eng                           |      51 |  0.1   |        1.9 | +3.9%        | 56%            | -14.3%    | 0.120588   |
| cecha: buzz_share                         |      51 |  0.098 |        1.9 | +3.2%        | 55%            | -15.1%    | 0.116667   |
| model: gradient boosting, cel zysk netto  |      39 |  0.097 |        1.7 | +7.3%        | 67%            | -3.9%     | 0.074359   |
| cecha: weeks_since_low                    |      51 |  0.087 |        3.4 | +3.4%        | 54%            | -20.4%    | 0.151961   |
| cecha: slope_60                           |      51 |  0.084 |        1.5 | -14.6%       | 32%            | -33.1%    | 0.0990196  |
| cecha: set_trend_90                       |      51 |  0.082 |        1.2 | -0.2%        | 49%            | -24.5%    | 0.0794118  |
| cecha: −rv_z                              |      51 |  0.073 |        3.9 | +4.9%        | 53%            | -30.0%    | 0.121569   |
| reguły: moduł B1 (tania vs podobne)       |      51 |  0.073 |        3.9 | +4.9%        | 53%            | -30.0%    | 0.121569   |
| cecha: vol_ratio                          |      51 |  0.062 |        2.8 | -1.9%        | 46%            | -24.6%    | 0.0833333  |
| cecha: slope_90                           |      51 |  0.047 |        0.9 | -13.8%       | 32%            | -32.6%    | 0.104902   |
| cecha: above_low                          |      51 |  0.042 |        0.7 | -12.7%       | 35%            | -31.9%    | 0.10098    |
| cecha: buzz_growth                        |      51 |  0.041 |        3   | +3.0%        | 54%            | -21.5%    | 0.114706   |
| cecha: special                            |      51 |  0.036 |        0.9 | -9.9%        | 33%            | -29.8%    | 0.0980392  |
| reguły: moduł A (ocena bez bramek)        |      51 |  0.035 |        0.6 | +4.5%        | 53%            | -15.9%    | 0.143137   |
| cecha: sealed_slope_90                    |      51 |  0.031 |        0.6 | -2.3%        | 45%            | -25.5%    | 0.0588235  |
| cecha: slope_180                          |      51 |  0.006 |        0.1 | -10.3%       | 35%            | -29.1%    | 0.0990196  |
| cecha: new_same_poke_90                   |      51 |  0.002 |        0.1 | +0.1%        | 51%            | -19.9%    | 0.113725   |
| cecha: new_same_poke_365                  |      51 | -0.012 |       -0.8 | -6.3%        | 30%            | -27.1%    | 0.0735294  |
| cecha: set_rel                            |      51 | -0.033 |       -1   | +1.8%        | 51%            | -3.5%     | 0.0941176  |
| cecha: logp                               |      51 | -0.039 |       -1   | +0.1%        | 50%            | -5.1%     | 0.0745098  |
| cecha: −slope_90                          |      51 | -0.047 |       -0.9 | -15.7%       | 25%            | -41.4%    | 0.027451   |
| cecha: rv_z                               |      51 | -0.073 |       -3.9 | +0.5%        | 51%            | -9.0%     | 0.0803922  |
| cecha: spread                             |      51 | -0.077 |       -2.7 | -3.0%        | 46%            | -37.0%    | 0.103922   |
| cecha: drawdown                           |      51 | -0.105 |       -1.7 | -4.2%        | 41%            | -31.6%    | 0.0980392  |
| cecha: rarity_w                           |      51 | -0.108 |       -1.9 | -19.1%       | 12%            | -28.2%    | 0.00980392 |
| cecha: −range_pos_180                     |      51 | -0.141 |       -3.3 | -15.3%       | 26%            | -35.5%    | 0.0333333  |
| cecha: history_complete                   |      51 | -0.144 |       -2.2 | -18.8%       | 20%            | -38.5%    | 0.0529412  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| model: gradient boosting                  |      39 | 0.386 |        4.6 | +7.4%        | 65%            | -5.7%     |  0.0910256 |
| łącznie: model + ocena C                  |      39 | 0.362 |        5.6 | +11.7%       | 66%            | -2.3%     |  0.120513  |
| ranking: szansa na +50% + model zwrotu    |      39 | 0.348 |        4.3 | +7.8%        | 61%            | -5.4%     |  0.132051  |
| model: gradient boosting, cel zysk netto  |      39 | 0.344 |        4.5 | +6.7%        | 67%            | -3.8%     |  0.0717949 |
| model: szansa na wzrost o 50%+            |      39 | 0.203 |        2.2 | +7.9%        | 59%            | -4.9%     |  0.139744  |
| ocena C: popularność + wiek + tania + dno |      51 | 0.198 |        2.5 | +7.9%        | 60%            | -3.7%     |  0.108824  |
| reguły: moduł A (ocena bez bramek)        |      51 | 0.096 |        1.4 | +4.8%        | 53%            | -4.6%     |  0.144118  |
| reguły: moduł B1 (tania vs podobne)       |      51 | 0.013 |        0.5 | +2.5%        | 49%            | -8.7%     |  0.129412  |

Stabilność (3 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |      13 |  0.311 |        3.2 | +22.0%       | 75%            | -13.5%    |  0.203846  |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      25 |  0.242 |        3   | +23.2%       | 81%            | -7.6%     |  0.268     |
| 1. połowa (od 2024-08) | model: gradient boosting                  |      13 |  0.151 |        0.9 | -1.0%        | 46%            | -30.8%    |  0.0884615 |
| 1. połowa (od 2024-08) | ranking: szansa na +50% + model zwrotu    |      13 |  0.139 |        0.8 | +3.8%        | 49%            | -28.7%    |  0.161538  |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      25 |  0.113 |        1.1 | -5.6%        | 44%            | -28.5%    |  0.122     |
| 1. połowa (od 2024-08) | model: szansa na wzrost o 50%+            |      13 |  0.101 |        0.6 | +6.0%        | 53%            | -28.0%    |  0.176923  |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      25 |  0.088 |        4.9 | +9.2%        | 60%            | -28.8%    |  0.16      |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      25 |  0.085 |        1.9 | +1.3%        | 48%            | -23.4%    |  0.146     |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      25 |  0.079 |        0.8 | +7.9%        | 59%            | -11.4%    |  0.18      |
| 2. połowa (od 2025-07) | model: gradient boosting                  |      26 |  0.359 |        8   | +13.8%       | 75%            | -10.4%    |  0.167308  |
| 2. połowa (od 2025-07) | ranking: szansa na +50% + model zwrotu    |      26 |  0.325 |        5.4 | +12.5%       | 72%            | -13.4%    |  0.192308  |
| 2. połowa (od 2025-07) | łącznie: model + ocena C                  |      26 |  0.266 |        4.8 | +8.4%        | 66%            | -17.8%    |  0.117308  |
| 2. połowa (od 2025-07) | model: szansa na wzrost o 50%+            |      26 |  0.216 |        2.5 | +9.7%        | 64%            | -17.4%    |  0.190385  |
| 2. połowa (od 2025-07) | cecha: −drawdown                          |      26 |  0.096 |        1.4 | +10.4%       | 62%            | -12.5%    |  0.234615  |
| 2. połowa (od 2025-07) | ocena C: popularność + wiek + tania + dno |      26 |  0.093 |        1.3 | +5.5%        | 56%            | -21.0%    |  0.0942308 |
| 2. połowa (od 2025-07) | cecha: weeks_since_low                    |      26 |  0.089 |        3.7 | +5.5%        | 60%            | -17.5%    |  0.157692  |
| 2. połowa (od 2025-07) | reguły: moduł B1 (tania vs podobne)       |      26 |  0.058 |        1.9 | +1.0%        | 46%            | -31.2%    |  0.0846154 |
| 2. połowa (od 2025-07) | reguły: moduł A (ocena bez bramek)        |      26 | -0.008 |       -0.1 | +1.3%        | 48%            | -20.2%    |  0.107692  |

## Horyzont 6 mies.

Daty z wynikiem: 45. Karty, które przeszły bramki modułu A: 133 obserwacji, średni zwrot ponad rynek -2.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      27 |  0.239 |        2.8 | +11.8%       | 63%            | -5.7%     |  0.333333  |
| model: szansa na wzrost o 50%+            |      27 |  0.23  |        3   | +13.4%       | 65%            | -4.0%     |  0.353704  |
| ocena C: popularność + wiek + tania + dno |      45 |  0.226 |        2   | +28.2%       | 74%            | +11.9%    |  0.427778  |
| łącznie: model + ocena C                  |      27 |  0.221 |        1.7 | +16.4%       | 69%            | -3.0%     |  0.368519  |
| model: gradient boosting                  |      27 |  0.219 |        2.4 | +11.7%       | 64%            | -7.3%     |  0.32963   |
| cecha: tier_score                         |      45 |  0.189 |        2.2 | -11.4%       | 37%            | -13.5%    |  0.182222  |
| cecha: poke_pop                           |      45 |  0.177 |        1.9 | +18.1%       | 67%            | +14.2%    |  0.365556  |
| cecha: age_months                         |      45 |  0.175 |        1   | +22.0%       | 69%            | +13.1%    |  0.36      |
| cecha: weeks_since_low                    |      45 |  0.147 |        3   | +1.5%        | 52%            | -10.4%    |  0.302222  |
| cecha: buzz_eng                           |      45 |  0.137 |        1.7 | +4.5%        | 58%            | -4.2%     |  0.254444  |
| cecha: buzz_share                         |      45 |  0.134 |        1.7 | +3.5%        | 56%            | -5.3%     |  0.246667  |
| cecha: range_pos_180                      |      45 |  0.132 |        2.4 | -1.3%        | 50%            | -12.5%    |  0.291111  |
| model: gradient boosting, cel zysk netto  |      27 |  0.132 |        1.2 | +8.7%        | 58%            | +6.7%     |  0.25      |
| cecha: −drawdown                          |      45 |  0.1   |        1.2 | -2.7%        | 48%            | -13.4%    |  0.288889  |
| cecha: slope_180                          |      45 |  0.099 |        1.6 | -13.9%       | 39%            | -21.4%    |  0.201111  |
| model: ridge na rangach                   |      27 |  0.096 |        0.7 | +19.8%       | 72%            | +5.9%     |  0.4       |
| cecha: above_low                          |      45 |  0.084 |        1   | -17.3%       | 37%            | -23.8%    |  0.203333  |
| reguły: moduł B1 (tania vs podobne)       |      45 |  0.077 |        4   | +7.8%        | 53%            | -17.3%    |  0.294444  |
| cecha: −rv_z                              |      45 |  0.077 |        4   | +7.8%        | 53%            | -17.3%    |  0.294444  |
| cecha: special                            |      45 |  0.07  |        1   | -10.1%       | 41%            | -17.7%    |  0.28      |
| cecha: slope_30                           |      45 |  0.062 |        0.9 | -19.3%       | 33%            | -27.1%    |  0.182222  |
| cecha: set_trend_90                       |      45 |  0.051 |        0.5 | -1.3%        | 47%            | -16.5%    |  0.211111  |
| cecha: slope_60                           |      45 |  0.047 |        0.7 | -21.6%       | 32%            | -28.5%    |  0.181111  |
| cecha: vol_ratio                          |      45 |  0.047 |        1.1 | -1.2%        | 46%            | -13.5%    |  0.211111  |
| cecha: slope_90                           |      45 |  0.044 |        0.7 | -19.8%       | 32%            | -26.1%    |  0.175556  |
| reguły: moduł A (ocena bez bramek)        |      45 |  0.039 |        0.5 | +7.8%        | 58%            | -2.0%     |  0.318889  |
| cecha: buzz_growth                        |      45 |  0.027 |        1.1 | +3.7%        | 53%            | -9.2%     |  0.246667  |
| cecha: sealed_slope_90                    |      45 | -0.02  |       -0.2 | -5.2%        | 39%            | -18.5%    |  0.161111  |
| cecha: new_same_poke_90                   |      45 | -0.023 |       -0.8 | -5.3%        | 43%            | -15.1%    |  0.223333  |
| cecha: set_rel                            |      45 | -0.025 |       -0.6 | +1.6%        | 50%            | +6.1%     |  0.191111  |
| cecha: logp                               |      45 | -0.03  |       -0.4 | -0.2%        | 47%            | +5.4%     |  0.198889  |
| cecha: new_same_poke_365                  |      45 | -0.039 |       -2.2 | -11.8%       | 28%            | -22.2%    |  0.152222  |
| cecha: −slope_90                          |      45 | -0.044 |       -0.7 | -22.3%       | 28%            | -35.1%    |  0.155556  |
| cecha: spread                             |      45 | -0.058 |       -1.3 | -3.0%        | 48%            | -26.3%    |  0.231111  |
| cecha: rv_z                               |      45 | -0.077 |       -4   | +2.1%        | 54%            | +3.8%     |  0.205556  |
| cecha: drawdown                           |      45 | -0.1   |       -1.2 | -9.6%        | 39%            | -24.9%    |  0.195556  |
| cecha: −range_pos_180                     |      45 | -0.132 |       -2.4 | -21.9%       | 25%            | -31.5%    |  0.107778  |
| cecha: rarity_w                           |      45 | -0.137 |       -2   | -30.4%       | 5%             | -31.9%    |  0.0122222 |
| cecha: history_complete                   |      45 | -0.162 |       -1.4 | -27.9%       | 19%            | -37.2%    |  0.102222  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| łącznie: model + ocena C                  |      27 | 0.273 |        1.9 | +3.3%        | 51%            | +2.2%     |   0.177778 |
| ocena C: popularność + wiek + tania + dno |      45 | 0.272 |        2.1 | +15.9%       | 63%            | +16.3%    |   0.334444 |
| model: gradient boosting                  |      27 | 0.258 |        2.3 | +6.1%        | 56%            | +4.4%     |   0.214815 |
| ranking: szansa na +50% + model zwrotu    |      27 | 0.257 |        2.5 | +8.9%        | 61%            | +8.1%     |   0.248148 |
| model: gradient boosting, cel zysk netto  |      27 | 0.246 |        2.3 | +6.0%        | 56%            | +6.2%     |   0.2      |
| model: szansa na wzrost o 50%+            |      27 | 0.215 |        2.4 | +9.6%        | 62%            | +9.8%     |   0.246296 |
| reguły: moduł A (ocena bez bramek)        |      45 | 0.089 |        0.8 | +6.5%        | 56%            | +8.3%     |   0.305556 |
| reguły: moduł B1 (tania vs podobne)       |      45 | 0.017 |        0.3 | +7.0%        | 55%            | +8.0%     |   0.307778 |

Stabilność (6 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | łącznie: model + ocena C                  |       4 | 0.432 |        6   | +50.3%       | 98%            | +8.1%     |   0.55     |
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      22 | 0.371 |        3.3 | +51.3%       | 86%            | +30.6%    |   0.602273 |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      22 | 0.169 |        2.3 | -4.8%        | 42%            | -18.1%    |   0.247727 |
| 1. połowa (od 2024-08) | ranking: szansa na +50% + model zwrotu    |       4 | 0.16  |        1.6 | +11.1%       | 50%            | -25.6%    |   0.2625   |
| 1. połowa (od 2024-08) | model: gradient boosting                  |       4 | 0.159 |        1.3 | +7.9%        | 49%            | -29.6%    |   0.1875   |
| 1. połowa (od 2024-08) | model: szansa na wzrost o 50%+            |       4 | 0.156 |        1.7 | +17.8%       | 62%            | -17.8%    |   0.3125   |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      22 | 0.132 |        0.9 | -15.5%       | 33%            | -28.7%    |   0.184091 |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      22 | 0.095 |        3.4 | +16.2%       | 59%            | -13.3%    |   0.356818 |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      22 | 0.069 |        0.5 | +13.9%       | 62%            | +6.3%     |   0.393182 |
| 2. połowa (od 2025-06) | ranking: szansa na +50% + model zwrotu    |      23 | 0.252 |        2.7 | +11.9%       | 65%            | -2.3%     |   0.345652 |
| 2. połowa (od 2025-06) | model: szansa na wzrost o 50%+            |      23 | 0.242 |        2.9 | +12.6%       | 65%            | -1.5%     |   0.36087  |
| 2. połowa (od 2025-06) | model: gradient boosting                  |      23 | 0.229 |        2.2 | +12.3%       | 66%            | -3.4%     |   0.354348 |
| 2. połowa (od 2025-06) | łącznie: model + ocena C                  |      23 | 0.184 |        1.4 | +11.3%       | 65%            | -4.9%     |   0.336957 |
| 2. połowa (od 2025-06) | cecha: weeks_since_low                    |      23 | 0.126 |        2.1 | +7.9%        | 62%            | -3.1%     |   0.354348 |
| 2. połowa (od 2025-06) | ocena C: popularność + wiek + tania + dno |      23 | 0.087 |        0.7 | +9.4%        | 62%            | -6.1%     |   0.26087  |
| 2. połowa (od 2025-06) | cecha: −drawdown                          |      23 | 0.07  |        0.7 | +11.3%       | 63%            | +1.2%     |   0.38913  |
| 2. połowa (od 2025-06) | reguły: moduł B1 (tania vs podobne)       |      23 | 0.059 |        3   | +0.4%        | 48%            | -21.0%    |   0.234783 |
| 2. połowa (od 2025-06) | reguły: moduł A (ocena bez bramek)        |      23 | 0.011 |        0.1 | +2.3%        | 55%            | -9.9%     |   0.247826 |

## Horyzont 12 mies.

Daty z wynikiem: 32. Karty, które przeszły bramki modułu A: 42 obserwacji, średni zwrot ponad rynek +21.8%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      14 |  0.417 |        2.3 | +32.2%       | 76%            | +37.6%    |  0.667857  |
| model: szansa na wzrost o 50%+            |      14 |  0.417 |        2.1 | +39.0%       | 81%            | +47.4%    |  0.717857  |
| model: gradient boosting                  |      14 |  0.371 |        2.4 | +35.7%       | 78%            | +39.8%    |  0.692857  |
| ocena C: popularność + wiek + tania + dno |      32 |  0.347 |        2.2 | +57.4%       | 82%            | +66.2%    |  0.73125   |
| łącznie: model + ocena C                  |      14 |  0.337 |        2   | +41.8%       | 83%            | +46.9%    |  0.732143  |
| cecha: tier_score                         |      32 |  0.316 |        2.6 | -9.2%        | 40%            | +6.2%     |  0.304688  |
| cecha: poke_pop                           |      32 |  0.309 |        2.7 | +39.6%       | 77%            | +61.3%    |  0.657812  |
| cecha: age_months                         |      32 |  0.288 |        1.4 | +51.3%       | 86%            | +65.1%    |  0.778125  |
| model: gradient boosting, cel zysk netto  |      14 |  0.282 |        1.6 | +23.1%       | 72%            | +47.5%    |  0.614286  |
| cecha: buzz_eng                           |      32 |  0.248 |        2.5 | +14.8%       | 65%            | +24.3%    |  0.476562  |
| model: ridge na rangach                   |      14 |  0.246 |        1.1 | +37.9%       | 78%            | +51.9%    |  0.714286  |
| cecha: buzz_share                         |      32 |  0.244 |        2.5 | +13.8%       | 65%            | +22.9%    |  0.459375  |
| cecha: weeks_since_low                    |      32 |  0.2   |        2.3 | -4.4%        | 48%            | -0.5%     |  0.385937  |
| cecha: range_pos_180                      |      32 |  0.16  |        1.6 | -15.8%       | 39%            | -10.7%    |  0.285937  |
| cecha: −drawdown                          |      32 |  0.155 |        1.2 | -18.8%       | 37%            | -13.4%    |  0.278125  |
| cecha: slope_180                          |      32 |  0.125 |        1.1 | -21.9%       | 34%            | -12.3%    |  0.239062  |
| reguły: moduł A (ocena bez bramek)        |      32 |  0.105 |        0.8 | +17.9%       | 66%            | +30.3%    |  0.570312  |
| cecha: above_low                          |      32 |  0.092 |        1   | -25.5%       | 35%            | -14.2%    |  0.275     |
| reguły: moduł B1 (tania vs podobne)       |      32 |  0.092 |        3.2 | +19.4%       | 66%            | +13.0%    |  0.551562  |
| cecha: −rv_z                              |      32 |  0.092 |        3.2 | +19.4%       | 66%            | +13.0%    |  0.551562  |
| cecha: slope_30                           |      32 |  0.081 |        0.9 | -27.5%       | 32%            | -18.9%    |  0.246875  |
| cecha: slope_60                           |      32 |  0.068 |        0.8 | -30.8%       | 30%            | -20.1%    |  0.217188  |
| cecha: slope_90                           |      32 |  0.06  |        0.7 | -28.5%       | 29%            | -18.7%    |  0.209375  |
| cecha: special                            |      32 |  0.051 |        0.9 | -22.4%       | 31%            | -16.0%    |  0.223438  |
| cecha: buzz_growth                        |      32 |  0.048 |        0.7 | +7.2%        | 57%            | +12.3%    |  0.4125    |
| cecha: vol_ratio                          |      32 |  0.045 |        0.5 | -0.9%        | 46%            | +3.2%     |  0.348437  |
| cecha: set_trend_90                       |      32 |  0.045 |        0.4 | -4.8%        | 44%            | -3.4%     |  0.29375   |
| cecha: logp                               |      32 |  0.031 |        0.3 | +2.4%        | 48%            | +26.5%    |  0.351562  |
| cecha: sealed_slope_90                    |      32 | -0.008 |       -0   | -5.1%        | 44%            | -1.6%     |  0.325     |
| cecha: new_same_poke_90                   |      32 | -0.009 |       -0.2 | -13.6%       | 38%            | -6.9%     |  0.309375  |
| cecha: set_rel                            |      32 | -0.009 |       -0.2 | +1.0%        | 44%            | +22.2%    |  0.320312  |
| cecha: new_same_poke_365                  |      32 | -0.019 |       -0.4 | -16.5%       | 34%            | -1.6%     |  0.285938  |
| cecha: spread                             |      32 | -0.029 |       -0.4 | -4.5%        | 49%            | -10.6%    |  0.4       |
| cecha: −slope_90                          |      32 | -0.06  |       -0.7 | -30.9%       | 29%            | -29.0%    |  0.225     |
| cecha: rv_z                               |      32 | -0.092 |       -3.2 | -2.9%        | 47%            | +16.3%    |  0.329688  |
| cecha: drawdown                           |      32 | -0.155 |       -1.2 | -19.5%       | 36%            | -16.0%    |  0.303125  |
| cecha: −range_pos_180                     |      32 | -0.16  |       -1.6 | -36.5%       | 17%            | -33.9%    |  0.11875   |
| cecha: rarity_w                           |      32 | -0.169 |       -1.8 | -44.3%       | 1%             | -38.0%    |  0.0078125 |
| cecha: history_complete                   |      32 | -0.24  |       -2.5 | -38.6%       | 20%            | -36.1%    |  0.142187  |

Tylko karty od $20 (przy tańszych koszty zjadają zysk):

| signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| ranking: szansa na +50% + model zwrotu    |      14 | 0.409 |        2.9 | +24.0%       | 73%            | +51.9%    |   0.610714 |
| ocena C: popularność + wiek + tania + dno |      32 | 0.405 |        2.5 | +36.7%       | 79%            | +58.8%    |   0.6875   |
| model: szansa na wzrost o 50%+            |      14 | 0.383 |        2.4 | +22.0%       | 70%            | +50.1%    |   0.6      |
| model: gradient boosting                  |      14 | 0.363 |        2.8 | +19.5%       | 67%            | +45.0%    |   0.564286 |
| łącznie: model + ocena C                  |      14 | 0.344 |        2.2 | +10.3%       | 60%            | +31.1%    |   0.475    |
| model: gradient boosting, cel zysk netto  |      14 | 0.336 |        2.8 | +16.6%       | 70%            | +42.3%    |   0.571429 |
| reguły: moduł A (ocena bez bramek)        |      32 | 0.106 |        0.7 | +11.4%       | 61%            | +31.8%    |   0.4875   |
| reguły: moduł B1 (tania vs podobne)       |      32 | 0.086 |        0.8 | +15.8%       | 63%            | +39.3%    |   0.532813 |

Stabilność (12 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   | top_net   |   top_up50 |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|:----------|-----------:|
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      16 | 0.473 |        7.9 | +93.1%       | 88%            | +101.4%   |   0.846875 |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      16 | 0.256 |        2.2 | -19.4%       | 33%            | -20.2%    |   0.225    |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      16 | 0.212 |        4.2 | -9.1%        | 44%            | -7.1%     |   0.315625 |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      16 | 0.114 |        3   | +27.9%       | 68%            | +17.4%    |   0.55     |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      16 | 0.063 |        0.4 | +24.0%       | 68%            | +41.0%    |   0.5625   |
| 2. połowa (od 2025-03) | ranking: szansa na +50% + model zwrotu    |      14 | 0.417 |        2.3 | +32.2%       | 76%            | +37.6%    |   0.667857 |
| 2. połowa (od 2025-03) | model: szansa na wzrost o 50%+            |      14 | 0.417 |        2.1 | +39.0%       | 81%            | +47.4%    |   0.717857 |
| 2. połowa (od 2025-03) | model: gradient boosting                  |      14 | 0.371 |        2.4 | +35.7%       | 78%            | +39.8%    |   0.692857 |
| 2. połowa (od 2025-03) | łącznie: model + ocena C                  |      14 | 0.337 |        2   | +41.8%       | 83%            | +46.9%    |   0.732143 |
| 2. połowa (od 2025-03) | ocena C: popularność + wiek + tania + dno |      16 | 0.22  |        1.1 | +28.3%       | 75%            | +31.0%    |   0.615625 |
| 2. połowa (od 2025-03) | cecha: weeks_since_low                    |      16 | 0.187 |        1.1 | +0.5%        | 52%            | +6.1%     |   0.45625  |
| 2. połowa (od 2025-03) | reguły: moduł A (ocena bez bramek)        |      16 | 0.147 |        0.9 | +12.1%       | 65%            | +19.6%    |   0.578125 |
| 2. połowa (od 2025-03) | reguły: moduł B1 (tania vs podobne)       |      16 | 0.069 |        4.5 | +11.5%       | 64%            | +8.7%     |   0.553125 |
| 2. połowa (od 2025-03) | cecha: −drawdown                          |      16 | 0.054 |        0.3 | -18.3%       | 40%            | -6.7%     |   0.33125  |

## Bieżący ranking modelu (6 mies., karty od $20)

Stan na 2026-10-18. Kolejność wg `score` (0–1, wyżej = lepiej) = średnia rang modelu szukającego kart, które zdrożeją o 50%+ (`szansa_50`), i modelu zwrotu (`model_6m`); w teście ta para najlepiej wybierała karty na rok (sekcja 12 mies.). `szansa_50` porządkuje karty, ale nie jest prawdziwym prawdopodobieństwem – faktyczny odsetek wzrostów o 50%+ zależy głównie od stanu całego rynku. `model_6m` = przewidywany log-zwrot ponad rynek w 6 mies. (0,20 ≈ +22%), `model_net_6m` = to samo po kosztach, `spread` = log(cena rynkowa / najniższa oferta). To lista do sprawdzenia, nie rekomendacja zakupu.

| name                         | set_name                         |   price_now |   score |   szansa_50 |   model_6m |   combo |   spread |   poke_pop |   rv_z |   weeks_since_low |   buzz_share |   model_net_6m |
|:-----------------------------|:---------------------------------|------------:|--------:|------------:|-----------:|--------:|---------:|-----------:|-------:|------------------:|-------------:|---------------:|
| Eevee - 188/167              | SV06: Twilight Masquerade        |       69.06 |    1.00 |        0.81 |       0.32 |   -0.26 |     0.00 |       2.44 |  -0.05 |                 0 |         2.47 |           0.52 |
| Cresselia - 071/064          | SV: Shrouded Fable               |       27.48 |    0.99 |        0.85 |       0.25 |   -0.27 |     0.14 |     nan    |   1.15 |                25 |         0.32 |           0.38 |
| Zorua - 075/064              | SV: Shrouded Fable               |       22.75 |    0.99 |        0.85 |       0.23 |   -0.23 |     0.13 |       1.00 |   0.87 |                25 |         0.43 |           0.36 |
| Latios - 203/191             | SV08: Surging Sparks             |       28.94 |    0.98 |        0.73 |       0.29 |   -0.80 |     0.19 |     nan    |   0.49 |                 0 |         0.75 |           0.36 |
| Houndoom - 066/064           | SV: Shrouded Fable               |       56.97 |    0.98 |        0.81 |       0.23 |   -0.83 |     0.13 |      -0.51 |   2.22 |                25 |         0.54 |           0.37 |
| Metagross - 178/162          | SV05: Temporal Forces            |       31.31 |    0.98 |        0.75 |       0.24 |   -0.10 |     0.11 |     nan    |   0.60 |                25 |         0.21 |           0.37 |
| Lickitung - 180/162          | SV05: Temporal Forces            |       28.48 |    0.98 |        0.83 |       0.21 |   -0.23 |     0.16 |     nan    |   1.20 |                25 |         0.21 |           0.33 |
| Minccino - 182/162           | SV05: Temporal Forces            |       23.86 |    0.97 |        0.79 |       0.22 |   -0.62 |     0.32 |       0.51 |   0.94 |                24 |         0.00 |           0.24 |
| Persian - 078/064            | SV: Shrouded Fable               |       73.75 |    0.97 |        0.82 |       0.21 |   -0.41 |     0.29 |     nan    |   2.60 |                25 |         0.11 |           0.33 |
| Espeon V (Full Art)          | SWSH07: Evolving Skies           |       25.93 |    0.97 |        0.69 |       0.27 |    0.68 |     0.12 |       2.96 |  -0.21 |                24 |         1.39 |           0.36 |
| Ceruledge - 197/191          | SV08: Surging Sparks             |       21.85 |    0.97 |        0.76 |       0.21 |   -0.07 |     0.22 |       1.84 |   0.81 |                25 |         0.21 |           0.30 |
| Umbreon VMAX                 | SWSH07: Evolving Skies           |       27.93 |    0.97 |        0.64 |       0.27 |    0.50 |     0.22 |       3.58 |  -0.15 |                 9 |         5.79 |           0.36 |
| Hisuian Growlithe - 181/167  | SV06: Twilight Masquerade        |       26.49 |    0.97 |        0.80 |       0.20 |   -0.24 |     0.14 |     nan    |   1.09 |                25 |         0.11 |           0.31 |
| Dusknoir - 070/064           | SV: Shrouded Fable               |       31.91 |    0.97 |        0.72 |       0.22 |   -0.80 |     0.08 |     nan    |   1.37 |                10 |         0.11 |           0.32 |
| Litten - 167/162             | SV05: Temporal Forces            |       38.48 |    0.97 |        0.80 |       0.20 |   -0.31 |     0.12 |     nan    |   1.64 |                25 |         0.00 |           0.32 |
| Espeon (Master Ball Pattern) | SV: Prismatic Evolutions         |       28.04 |    0.96 |        0.71 |       0.21 |    0.42 |     0.09 |       2.96 | nan    |                25 |         1.39 |           0.31 |
| Pikachu ex - 219/191         | SV08: Surging Sparks             |       27.02 |    0.96 |        0.68 |       0.22 |   -0.42 |     0.26 |       2.34 |   0.14 |                 0 |        14.48 |           0.33 |
| Pikachu - 173/165            | SV: Scarlet & Violet 151         |       66.09 |    0.96 |        0.60 |       0.28 |   -0.17 |     0.05 |       2.51 | nan    |                 0 |        14.48 |           0.47 |
| ______'s Pikachu             | Celebrations: Classic Collection |       30.47 |    0.96 |        0.60 |       0.28 |    0.22 |     0.10 |     nan    |  -0.69 |                 9 |         0.00 |           0.26 |
| Venusaur & Snivy GX          | SM - Cosmic Eclipse              |       26.06 |    0.96 |        0.60 |       0.26 |    1.12 |     0.21 |       1.25 |  -1.57 |                25 |         1.39 |           0.28 |
| Arbok - 176/162              | SV05: Temporal Forces            |       28.91 |    0.96 |        0.78 |       0.20 |   -0.24 |     0.11 |     nan    |   1.22 |                25 |         0.00 |           0.32 |
| Shining Magikarp             | Celebrations: Classic Collection |       32.43 |    0.96 |        0.60 |       0.25 |    0.51 |     0.15 |       3.64 |  -0.66 |                 0 |         2.15 |           0.28 |
| Horsea - 067/064             | SV: Shrouded Fable               |       46.14 |    0.95 |        0.78 |       0.19 |   -0.37 |     0.25 |     nan    |   1.91 |                25 |         0.00 |           0.32 |
| Squirtle                     | SV07: Stellar Crown              |       95.51 |    0.95 |        0.68 |       0.21 |   -0.91 |     0.12 |       1.84 |   2.18 |                 0 |         0.11 |           0.35 |
| Sawsbuck - 166/162           | SV05: Temporal Forces            |       52.40 |    0.95 |        0.80 |       0.19 |   -0.40 |     0.15 |       0.88 |   2.10 |                25 |         0.00 |           0.29 |

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
