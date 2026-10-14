# PokeScout – test przewidywań na historii

Dane: 137 dni notowań, 4777 kart w katalogu; panel 77081 obserwacji (2024-08-11 – 2026-10-18, co 2 tygodnie).

**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, 0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. `top_excess` = średni zwrot 20 najwyżej ocenionych kart ponad medianę rynku, `top_hit_rate` = jaki odsetek z nich pobił rynek.

## Horyzont 3 mies.

Daty z wynikiem: 51. Karty, które przeszły bramki modułu A: 200 obserwacji, średni zwrot ponad rynek +1.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|
| model: gradient boosting                  |      39 |  0.271 |        3.8 | +5.9%        | 61%            |
| ocena C: popularność + wiek + tania + dno |      51 |  0.166 |        2.8 | +13.8%       | 69%            |
| cecha: age_months                         |      51 |  0.148 |        1.4 | +11.2%       | 66%            |
| cecha: range_pos_180                      |      51 |  0.141 |        3.3 | +2.2%        | 52%            |
| cecha: tier_score                         |      51 |  0.133 |        2.5 | -6.7%        | 37%            |
| cecha: poke_pop                           |      51 |  0.115 |        2.1 | +9.1%        | 62%            |
| cecha: slope_30                           |      51 |  0.111 |        2.3 | -12.7%       | 35%            |
| cecha: −drawdown                          |      51 |  0.105 |        1.7 | +2.3%        | 53%            |
| model: ridge na rangach                   |      39 |  0.097 |        1.2 | +8.0%        | 63%            |
| cecha: weeks_since_low                    |      51 |  0.087 |        3.4 | +3.4%        | 54%            |
| cecha: slope_60                           |      51 |  0.084 |        1.5 | -14.6%       | 32%            |
| cecha: set_trend_90                       |      51 |  0.082 |        1.2 | -0.2%        | 49%            |
| cecha: −rv_z                              |      51 |  0.073 |        3.9 | +4.9%        | 53%            |
| reguły: moduł B1 (tania vs podobne)       |      51 |  0.073 |        3.9 | +4.9%        | 53%            |
| cecha: vol_ratio                          |      51 |  0.062 |        2.8 | -1.9%        | 46%            |
| cecha: slope_90                           |      51 |  0.047 |        0.9 | -13.8%       | 32%            |
| cecha: above_low                          |      51 |  0.042 |        0.7 | -12.7%       | 35%            |
| cecha: special                            |      51 |  0.036 |        0.9 | -9.9%        | 33%            |
| reguły: moduł A (ocena bez bramek)        |      51 |  0.035 |        0.6 | +4.5%        | 53%            |
| cecha: sealed_slope_90                    |      51 |  0.031 |        0.6 | -2.3%        | 45%            |
| cecha: slope_180                          |      51 |  0.006 |        0.1 | -10.3%       | 35%            |
| cecha: set_rel                            |      51 | -0.033 |       -1   | +1.8%        | 51%            |
| cecha: logp                               |      51 | -0.039 |       -1   | +0.1%        | 50%            |
| cecha: −slope_90                          |      51 | -0.047 |       -0.9 | -15.7%       | 25%            |
| cecha: rv_z                               |      51 | -0.073 |       -3.9 | +0.5%        | 51%            |
| cecha: drawdown                           |      51 | -0.105 |       -1.7 | -4.2%        | 41%            |
| cecha: rarity_w                           |      51 | -0.108 |       -1.9 | -19.1%       | 12%            |
| cecha: −range_pos_180                     |      51 | -0.141 |       -3.3 | -15.3%       | 26%            |
| cecha: history_complete                   |      51 | -0.144 |       -2.2 | -18.8%       | 20%            |

Stabilność (3 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   |
|:-----------------------|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      25 |  0.242 |        3   | +23.2%       | 81%            |
| 1. połowa (od 2024-08) | model: gradient boosting                  |      13 |  0.143 |        0.9 | -1.6%        | 45%            |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      25 |  0.113 |        1.1 | -5.6%        | 44%            |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      25 |  0.088 |        4.9 | +9.2%        | 60%            |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      25 |  0.085 |        1.9 | +1.3%        | 48%            |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      25 |  0.079 |        0.8 | +7.9%        | 59%            |
| 2. połowa (od 2025-07) | model: gradient boosting                  |      26 |  0.336 |        7.3 | +9.8%        | 68%            |
| 2. połowa (od 2025-07) | cecha: −drawdown                          |      26 |  0.096 |        1.4 | +10.4%       | 62%            |
| 2. połowa (od 2025-07) | ocena C: popularność + wiek + tania + dno |      26 |  0.093 |        1.3 | +5.5%        | 56%            |
| 2. połowa (od 2025-07) | cecha: weeks_since_low                    |      26 |  0.089 |        3.7 | +5.5%        | 60%            |
| 2. połowa (od 2025-07) | reguły: moduł B1 (tania vs podobne)       |      26 |  0.058 |        1.9 | +1.0%        | 46%            |
| 2. połowa (od 2025-07) | reguły: moduł A (ocena bez bramek)        |      26 | -0.008 |       -0.1 | +1.3%        | 48%            |

## Horyzont 6 mies.

Daty z wynikiem: 45. Karty, które przeszły bramki modułu A: 133 obserwacji, średni zwrot ponad rynek -2.4%.

| signal                                    |   dates |     ic |   ic_t_adj | top_excess   | top_hit_rate   |
|:------------------------------------------|--------:|-------:|-----------:|:-------------|:---------------|
| ocena C: popularność + wiek + tania + dno |      45 |  0.226 |        2   | +28.2%       | 74%            |
| model: gradient boosting                  |      27 |  0.214 |        2.5 | +8.0%        | 57%            |
| cecha: tier_score                         |      45 |  0.189 |        2.2 | -11.4%       | 37%            |
| cecha: poke_pop                           |      45 |  0.177 |        1.9 | +18.1%       | 67%            |
| cecha: age_months                         |      45 |  0.175 |        1   | +22.0%       | 69%            |
| cecha: weeks_since_low                    |      45 |  0.147 |        3   | +1.5%        | 52%            |
| cecha: range_pos_180                      |      45 |  0.132 |        2.4 | -1.3%        | 50%            |
| cecha: −drawdown                          |      45 |  0.1   |        1.2 | -2.7%        | 48%            |
| cecha: slope_180                          |      45 |  0.099 |        1.6 | -13.9%       | 39%            |
| cecha: above_low                          |      45 |  0.084 |        1   | -17.3%       | 37%            |
| reguły: moduł B1 (tania vs podobne)       |      45 |  0.077 |        4   | +7.8%        | 53%            |
| cecha: −rv_z                              |      45 |  0.077 |        4   | +7.8%        | 53%            |
| model: ridge na rangach                   |      27 |  0.072 |        0.5 | +15.1%       | 67%            |
| cecha: special                            |      45 |  0.07  |        1   | -10.1%       | 41%            |
| cecha: slope_30                           |      45 |  0.062 |        0.9 | -19.3%       | 33%            |
| cecha: set_trend_90                       |      45 |  0.051 |        0.5 | -1.3%        | 47%            |
| cecha: slope_60                           |      45 |  0.047 |        0.7 | -21.6%       | 32%            |
| cecha: vol_ratio                          |      45 |  0.047 |        1.1 | -1.2%        | 46%            |
| cecha: slope_90                           |      45 |  0.044 |        0.7 | -19.8%       | 32%            |
| reguły: moduł A (ocena bez bramek)        |      45 |  0.039 |        0.5 | +7.8%        | 58%            |
| cecha: sealed_slope_90                    |      45 | -0.02  |       -0.2 | -5.2%        | 39%            |
| cecha: set_rel                            |      45 | -0.025 |       -0.6 | +1.6%        | 50%            |
| cecha: logp                               |      45 | -0.03  |       -0.4 | -0.2%        | 47%            |
| cecha: −slope_90                          |      45 | -0.044 |       -0.7 | -22.3%       | 28%            |
| cecha: rv_z                               |      45 | -0.077 |       -4   | +2.1%        | 54%            |
| cecha: drawdown                           |      45 | -0.1   |       -1.2 | -9.6%        | 39%            |
| cecha: −range_pos_180                     |      45 | -0.132 |       -2.4 | -21.9%       | 25%            |
| cecha: rarity_w                           |      45 | -0.137 |       -2   | -30.4%       | 5%             |
| cecha: history_complete                   |      45 | -0.162 |       -1.4 | -27.9%       | 19%            |

Stabilność (6 mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.

| okres                  | signal                                    |   dates |    ic |   ic_t_adj | top_excess   | top_hit_rate   |
|:-----------------------|:------------------------------------------|--------:|------:|-----------:|:-------------|:---------------|
| 1. połowa (od 2024-08) | ocena C: popularność + wiek + tania + dno |      22 | 0.371 |        3.3 | +51.3%       | 86%            |
| 1. połowa (od 2024-08) | cecha: weeks_since_low                    |      22 | 0.169 |        2.3 | -4.8%        | 42%            |
| 1. połowa (od 2024-08) | model: gradient boosting                  |       4 | 0.15  |        1.3 | -0.9%        | 35%            |
| 1. połowa (od 2024-08) | cecha: −drawdown                          |      22 | 0.132 |        0.9 | -15.5%       | 33%            |
| 1. połowa (od 2024-08) | reguły: moduł B1 (tania vs podobne)       |      22 | 0.095 |        3.4 | +16.2%       | 59%            |
| 1. połowa (od 2024-08) | reguły: moduł A (ocena bez bramek)        |      22 | 0.069 |        0.5 | +13.9%       | 62%            |
| 2. połowa (od 2025-06) | model: gradient boosting                  |      23 | 0.225 |        2.3 | +9.6%        | 61%            |
| 2. połowa (od 2025-06) | cecha: weeks_since_low                    |      23 | 0.126 |        2.1 | +7.9%        | 62%            |
| 2. połowa (od 2025-06) | ocena C: popularność + wiek + tania + dno |      23 | 0.087 |        0.7 | +9.4%        | 62%            |
| 2. połowa (od 2025-06) | cecha: −drawdown                          |      23 | 0.07  |        0.7 | +11.3%       | 63%            |
| 2. połowa (od 2025-06) | reguły: moduł B1 (tania vs podobne)       |      23 | 0.059 |        3   | +0.4%        | 48%            |
| 2. połowa (od 2025-06) | reguły: moduł A (ocena bez bramek)        |      23 | 0.011 |        0.1 | +2.3%        | 55%            |

## Horyzont 12 mies.

Daty z wynikiem: 32. Karty, które przeszły bramki modułu A: 42 obserwacji, średni zwrot ponad rynek +21.8%.

| signal                                    |   dates |     ic | ic_t_adj   | top_excess   | top_hit_rate   |
|:------------------------------------------|--------:|-------:|:-----------|:-------------|:---------------|
| ocena C: popularność + wiek + tania + dno |      32 |  0.347 | +2.2       | +57.4%       | 82%            |
| cecha: tier_score                         |      32 |  0.316 | +2.6       | -9.2%        | 40%            |
| cecha: poke_pop                           |      32 |  0.309 | +2.7       | +39.6%       | 77%            |
| cecha: age_months                         |      32 |  0.288 | +1.4       | +51.3%       | 86%            |
| cecha: weeks_since_low                    |      32 |  0.2   | +2.3       | -4.4%        | 48%            |
| cecha: range_pos_180                      |      32 |  0.16  | +1.6       | -15.8%       | 39%            |
| cecha: −drawdown                          |      32 |  0.155 | +1.2       | -18.8%       | 37%            |
| model: gradient boosting                  |       1 |  0.148 | +nan       | +4.4%        | 65%            |
| cecha: slope_180                          |      32 |  0.125 | +1.1       | -21.9%       | 34%            |
| reguły: moduł A (ocena bez bramek)        |      32 |  0.105 | +0.8       | +17.9%       | 66%            |
| cecha: above_low                          |      32 |  0.092 | +1.0       | -25.5%       | 35%            |
| cecha: −rv_z                              |      32 |  0.092 | +3.2       | +19.4%       | 66%            |
| reguły: moduł B1 (tania vs podobne)       |      32 |  0.092 | +3.2       | +19.4%       | 66%            |
| cecha: slope_30                           |      32 |  0.081 | +0.9       | -27.5%       | 32%            |
| cecha: slope_60                           |      32 |  0.068 | +0.8       | -30.8%       | 30%            |
| cecha: slope_90                           |      32 |  0.06  | +0.7       | -28.5%       | 29%            |
| cecha: special                            |      32 |  0.051 | +0.9       | -22.4%       | 31%            |
| cecha: vol_ratio                          |      32 |  0.045 | +0.5       | -0.9%        | 46%            |
| cecha: set_trend_90                       |      32 |  0.045 | +0.4       | -4.8%        | 44%            |
| model: ridge na rangach                   |       1 |  0.034 | +nan       | +12.0%       | 65%            |
| cecha: logp                               |      32 |  0.031 | +0.3       | +2.4%        | 48%            |
| cecha: sealed_slope_90                    |      32 | -0.008 | -0.0       | -5.1%        | 44%            |
| cecha: set_rel                            |      32 | -0.009 | -0.2       | +1.0%        | 44%            |
| cecha: −slope_90                          |      32 | -0.06  | -0.7       | -30.9%       | 29%            |
| cecha: rv_z                               |      32 | -0.092 | -3.2       | -2.9%        | 47%            |
| cecha: drawdown                           |      32 | -0.155 | -1.2       | -19.5%       | 36%            |
| cecha: −range_pos_180                     |      32 | -0.16  | -1.6       | -36.5%       | 17%            |
| cecha: rarity_w                           |      32 | -0.169 | -1.8       | -44.3%       | 1%             |
| cecha: history_complete                   |      32 | -0.24  | -2.5       | -38.6%       | 20%            |

## Bieżący ranking modelu (6 mies.)

Stan na 2026-10-18. `model_6m` = przewidywany przez model log-zwrot ponad rynek w 6 mies. (0,30 ≈ +35%), `combo` = ocena C dla porównania (wyżej = lepiej). To lista do sprawdzenia, nie rekomendacja zakupu.

| name                         | set_name                               |   price_now |   age_months |   poke_pop |   rv_z |   weeks_since_low |   combo |   model_6m | rule_a_pass   |
|:-----------------------------|:---------------------------------------|------------:|-------------:|-----------:|-------:|------------------:|--------:|-----------:|:--------------|
| Mewtwo                       | Detective Pikachu                      |       10.63 |        90.44 |       1.68 |  -0.72 |                21 |    0.75 |       0.40 | False         |
| Eevee - 188/167              | SV06: Twilight Masquerade              |       69.06 |        28.81 |       2.44 |  -0.05 |                 0 |   -0.26 |       0.33 | False         |
| Gyarados                     | SM - Team Up                           |       11.23 |        92.51 |      -1.00 |  -0.64 |                25 |    0.52 |       0.33 | False         |
| Sylveon VMAX                 | SWSH07: Evolving Skies                 |       19.34 |        61.70 |       3.09 |  -0.44 |                25 |    1.06 |       0.31 | False         |
| Pikachu - 173/165            | SV: Scarlet & Violet 151               |       66.09 |        36.86 |       2.51 | nan    |                 0 |   -0.17 |       0.31 | False         |
| Greninja                     | Detective Pikachu                      |       10.67 |        90.44 |       2.63 |  -0.71 |                24 |    1.12 |       0.31 | False         |
| Greninja ex - 198/167        | SV06: Twilight Masquerade              |       14.46 |        28.81 |       2.63 |  -0.55 |                25 |    0.67 |       0.30 | False         |
| Rayquaza VMAX                | SWSH07: Evolving Skies                 |       13.11 |        61.70 |       2.92 |  -0.75 |                25 |    1.17 |       0.30 | False         |
| Sylveon V                    | SWSH07: Evolving Skies                 |        6.03 |        61.70 |       3.09 |  -1.35 |                24 |    1.08 |       0.30 | False         |
| Latios - 203/191             | SV08: Surging Sparks                   |       28.94 |        23.29 |     nan    |   0.49 |                 0 |   -0.80 |       0.29 | False         |
| Gardevoir ex (Delta Species) | Celebrations: Classic Collection       |        9.46 |        60.32 |       2.53 |  -1.28 |                23 |    0.85 |       0.29 | False         |
| Mew ex                       | Celebrations: Classic Collection       |       16.00 |        60.32 |       2.32 |  -1.01 |                 0 |    0.44 |       0.29 | False         |
| Espeon VMAX                  | SWSH07: Evolving Skies                 |       15.20 |        61.70 |       2.96 |  -0.63 |                10 |    0.63 |       0.29 | False         |
| Gyarados V (Full Art)        | SWSH07: Evolving Skies                 |       19.38 |        61.70 |      -1.00 |  -0.44 |                25 |    0.15 |       0.29 | False         |
| Metagross - 178/162          | SV05: Temporal Forces                  |       31.31 |        30.88 |     nan    |   0.60 |                25 |   -0.10 |       0.29 | False         |
| Dark Gyarados                | Celebrations: Classic Collection       |        5.46 |        60.32 |     nan    |  -1.55 |                10 |    0.43 |       0.29 | False         |
| Umbreon V                    | SWSH07: Evolving Skies                 |        8.37 |        61.70 |       3.58 |  -1.10 |                25 |    1.36 |       0.29 | False         |
| Detective Pikachu            | Detective Pikachu                      |       15.63 |        90.44 |     nan    |  -0.18 |                25 |    0.82 |       0.28 | False         |
| Gyarados VMAX                | SWSH07: Evolving Skies                 |        8.48 |        61.70 |      -1.00 |  -1.09 |                25 |    0.40 |       0.28 | False         |
| Lugia                        | SM - Team Up                           |       21.49 |        92.51 |       3.51 |   0.29 |                25 |    1.10 |       0.28 | False         |
| Charizard                    | Detective Pikachu                      |       14.29 |        90.44 |       2.57 |  -0.29 |                25 |    1.20 |       0.28 | False         |
| Gardevoir                    | SWSH12: Silver Tempest Trainer Gallery |        7.20 |        47.21 |       2.04 |  -1.10 |                25 |    0.98 |       0.28 | False         |
| M Rayquaza EX                | Celebrations: Classic Collection       |       34.98 |        60.32 |       3.96 |  -0.62 |                 0 |    0.50 |       0.28 | False         |
| Venusaur                     | Celebrations: Classic Collection       |       11.16 |        60.32 |       2.03 |  -1.19 |                10 |    0.62 |       0.28 | False         |
| Mew                          | SM - Unbroken Bonds                    |       25.37 |        89.52 |       1.87 |   0.53 |                25 |    0.71 |       0.27 | False         |
