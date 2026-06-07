# SPF Performance Evaluation — Summary Tables

## 1. Rata-Rata Throughput (Mbps)

|                                             |    A* |   Bellman-Ford |   Widest Path |
|:--------------------------------------------|------:|---------------:|--------------:|
| ('jellyfish', 'Bandwidth Throttle')         | 95.28 |          95.28 |         94.95 |
| ('jellyfish', 'Baseline No Failure')        | 95.25 |          95.1  |         94.99 |
| ('jellyfish', 'Link Down Before Traffic')   | 95.34 |          95.08 |         94.86 |
| ('jellyfish', 'Link Down During Traffic')   | 94.88 |          94.82 |         94.97 |
| ('jellyfish', 'Link Flap')                  | 94.58 |          95.33 |         94.91 |
| ('jellyfish', 'Random Link Down Jellyfish') | 95.08 |          95.27 |         95.55 |
| ('jellyfish', 'Switch Down')                | 95.26 |          95.12 |         95.29 |
| ('ring5', 'Bandwidth Throttle')             | 52.51 |          95    |         52.51 |
| ('ring5', 'Baseline No Failure')            | 95.51 |          94.95 |         95.5  |
| ('ring5', 'Link Down Before Traffic')       | 95.5  |          95.51 |         95.5  |
| ('ring5', 'Link Down During Traffic')       | 95.18 |          93.75 |         95.15 |
| ('ring5', 'Link Flap')                      | 94.43 |          93.27 |         94.64 |
| ('ring5', 'Switch Down')                    | 95.49 |          95.51 |         95.51 |

## 2. Rata-Rata Runtime Komputasi Jalur (ms)

|                                             |     A* |   Bellman-Ford |   Widest Path |
|:--------------------------------------------|-------:|---------------:|--------------:|
| ('jellyfish', 'Bandwidth Throttle')         | 0.0548 |         0.0844 |        0.0751 |
| ('jellyfish', 'Baseline No Failure')        | 0.0602 |         0.2071 |        0.5385 |
| ('jellyfish', 'Link Down Before Traffic')   | 0.043  |         0.0667 |        0.0605 |
| ('jellyfish', 'Link Down During Traffic')   | 0.0609 |         0.0775 |        0.0659 |
| ('jellyfish', 'Link Flap')                  | 0.0439 |         0.0727 |        0.0832 |
| ('jellyfish', 'Random Link Down Jellyfish') | 0.0559 |         0.0633 |        0.2263 |
| ('jellyfish', 'Switch Down')                | 0.0984 |         0.0674 |        1.2809 |
| ('ring5', 'Bandwidth Throttle')             | 0.0377 |         0.0379 |        0.0487 |
| ('ring5', 'Baseline No Failure')            | 0.0394 |         0.0635 |        0.6899 |
| ('ring5', 'Link Down Before Traffic')       | 0.0643 |         0.0282 |        0.0575 |
| ('ring5', 'Link Down During Traffic')       | 0.0392 |         0.0273 |        0.0292 |
| ('ring5', 'Link Flap')                      | 0.0305 |         0.0285 |        0.0289 |
| ('ring5', 'Switch Down')                    | 0.0476 |         0.0888 |        0.0456 |

## 3. Rata-Rata Hop Count

|                                             |   A* |   Bellman-Ford |   Widest Path |
|:--------------------------------------------|-----:|---------------:|--------------:|
| ('jellyfish', 'Bandwidth Throttle')         |  1.5 |            1.5 |           1.5 |
| ('jellyfish', 'Baseline No Failure')        |  1.5 |            1.5 |           1.5 |
| ('jellyfish', 'Link Down Before Traffic')   |  1.5 |            1.5 |           1.5 |
| ('jellyfish', 'Link Down During Traffic')   |  1.5 |            1.5 |           1.5 |
| ('jellyfish', 'Link Flap')                  |  1.5 |            1.5 |           1.5 |
| ('jellyfish', 'Random Link Down Jellyfish') |  1.5 |            1.5 |           1.5 |
| ('jellyfish', 'Switch Down')                |  2   |            2   |           2   |
| ('ring5', 'Bandwidth Throttle')             |  1   |            1   |           1   |
| ('ring5', 'Baseline No Failure')            |  1   |            1   |           1   |
| ('ring5', 'Link Down Before Traffic')       |  1   |            1   |           1   |
| ('ring5', 'Link Down During Traffic')       |  1   |            1   |           1   |
| ('ring5', 'Link Flap')                      |  1   |            1   |           1   |
| ('ring5', 'Switch Down')                    |  1   |            1   |           1   |

## 4. Success Rate

|                                             | A*   | Bellman-Ford   | Widest Path   |
|:--------------------------------------------|:-----|:---------------|:--------------|
| ('jellyfish', 'Bandwidth Throttle')         | 2/2  | 2/2            | 2/2           |
| ('jellyfish', 'Baseline No Failure')        | 2/2  | 2/2            | 2/2           |
| ('jellyfish', 'Link Down Before Traffic')   | 2/2  | 2/2            | 2/2           |
| ('jellyfish', 'Link Down During Traffic')   | 2/2  | 2/2            | 2/2           |
| ('jellyfish', 'Link Flap')                  | 2/2  | 2/2            | 2/2           |
| ('jellyfish', 'Random Link Down Jellyfish') | 2/2  | 2/2            | 2/2           |
| ('jellyfish', 'Switch Down')                | 1/2  | 1/2            | 1/2           |
| ('ring5', 'Bandwidth Throttle')             | 2/2  | 2/2            | 2/2           |
| ('ring5', 'Baseline No Failure')            | 2/2  | 2/2            | 2/2           |
| ('ring5', 'Link Down Before Traffic')       | 2/2  | 2/2            | 2/2           |
| ('ring5', 'Link Down During Traffic')       | 2/2  | 2/2            | 2/2           |
| ('ring5', 'Link Flap')                      | 2/2  | 2/2            | 2/2           |
| ('ring5', 'Switch Down')                    | 1/2  | 1/2            | 1/2           |

## 5. Ranking Algoritma per Topologi

| topology   | algorithm    |   mean_throughput |   mean_runtime |   std_throughput |   success_rate |   composite_score |   rank |
|:-----------|:-------------|------------------:|---------------:|-----------------:|---------------:|------------------:|-------:|
| jellyfish  | bellman_ford |           95.1455 |         0.0931 |           0.2341 |         0.9286 |            0.7641 |      1 |
| jellyfish  | astar        |           95.0822 |         0.0566 |           0.3103 |         0.9286 |            0.4439 |      2 |
| jellyfish  | widest_path  |           95.0576 |         0.26   |           0.4577 |         0.9286 |            0      |      3 |
| ring5      | bellman_ford |           94.5896 |         0.0418 |           1.1182 |         0.9167 |            0.8    |      1 |
| ring5      | astar        |           87.4346 |         0.0427 |          25.8512 |         0.9167 |            0.1985 |      2 |
| ring5      | widest_path  |           87.463  |         0.1595 |          25.8581 |         0.9167 |            0.0016 |      3 |

## 6. Failure Impact: Δ Throughput vs Baseline (%)

|                         |   astar |   bellman_ford |   widest_path |
|:------------------------|--------:|---------------:|--------------:|
| ('jellyfish', 'during') |   -0.54 |          -0.03 |         -0.06 |
| ('jellyfish', 'pre')    |   -0.01 |           0.1  |          0.16 |
| ('ring5', 'during')     |   -0.74 |          -1.52 |         -0.64 |
| ('ring5', 'pre')        |  -18.01 |           0.37 |        -18    |

